import argparse
import os
import threading

import ss_manager.settings as settings
from ss_manager.utils.encryption import format_secret
from ss_manager.utils.manager import supervisor, reset, load
from ss_manager.utils import api


def main():
    parser = argparse.ArgumentParser(
        prog="ss-manager-controller",
        description="A simple program using for sharing shadowsocks server. Basing on ss-manager."
    )
    subprasers = parser.add_subparsers(dest="command", required=True)
    subprasers.add_parser("run", help="run main controller.")
    subprasers.add_parser("reset", help="reset users' traffic. Normally used by crontab.")
    subprasers.add_parser("list", help="print all users' info")
    add = subprasers.add_parser("add", help="add new user")
    add.add_argument("-n", "--name", type=str, required=True,
                     help="name of the user")
    add.add_argument("-P", "--port", type=int, default=0,
                     help="specific port you want to use. Left empty to use random available port.")
    add.add_argument("-p", "--password", type=str, default="",
                     help="specific password you want to use. Recommended to left empty to use uuid.")
    add.add_argument("-t", "--monthly-traffic", type=int, default=0,
                     help="monthly traffic set for this user (GB). Using --default-monthly-traffic by default.")
    delete = subprasers.add_parser("del", help="delete user from ss-manager")
    delete.add_argument("-n", "--name", type=str, required=True,
                        help="name of the user")
    subscription = subprasers.add_parser("sub", help="print user's subscription")
    subscription.add_argument("-n", "--name", type=str, required=True,
                              help="name of the user")
    parser.add_argument("-sma", "--ss-manager-address", type=str, default="127.0.0.1:7968",
                        help="address of ss-manager. Supporting net address and port or UDS. "
                             "Using 127.0.0.1:7968 by default.")
    parser.add_argument("-aa", "--api-address", type=str, default="127.0.0.1:7969",
                        help="address of controllers api service. Supporting net address and port or UDS. "
                             "Using 127.0.0.1:7969 by default.")
    parser.add_argument("-f", "--data-filename", type=str, default="/var/lib/ss-manager.csv",
                        help="name of the csv file used for persistent storage of data. "
                             "Using /var/lib/ss-manager.csv by default.")
    parser.add_argument("-ss", "--ss-server", type=str, default="localhost",
                        help="ss-server address or domain using to generate subscription url.")
    parser.add_argument("-se", "--ss-encryption", type=str, default="aes-128-gcm",
                        help="ss-server encryption using to generate subscription url. Using aes-128-gcm as default.")
    parser.add_argument("-k", "--key", type=str, default="0123456789abcdef",
                        help="the AES key of network transportation encryption.")
    parser.add_argument("-sp", "--start-port", type=int, default=8001,
                        help="users' port pool start point (included). Using 8001 by default.")
    parser.add_argument("-ep", "--end-port", type=int, default=8501,
                        help="users' port pool end point (not included). Using 8501 by default.")
    parser.add_argument("-dmt", "--default-monthly-traffic", type=int, default=100,
                        help="default monthly traffic (GB). Using 100 by default.")
    parser.add_argument("-ri", "--refresh-interval", type=int, default=30,
                        help="interval of writing data and check traffic usage. Using 30 by default.")
    parser.add_argument("-rd", "--reset-date", type=int, default=1,
                        help="traffic record refresh date. Using 1 by default.")
    parser.add_argument("-rt", "--reset-time", type=int, default=1,
                        help="traffic record refresh time. "
                             "Using 1 indicating record refreshed at 1:00 on reset date by default.")

    args = parser.parse_args()
    # Init AES key
    format_secret(args)
    # Load data and init users
    load(**args.__dict__)
    if args.command == "run":
        # Start api controller
        t = threading.Thread(target=api.handler)
        t.daemon = True
        t.start()
        # Start reset crontab in container
        if os.environ.get("CONTAINER") == "true":
            os.system(f"echo '0  {settings.reset_time}    {settings.reset_date} * *   root    "
                      f"cd /ss-manager-controller && python3 main.py reset' >> /etc/crontab")
            os.system("cron")
        supervisor()
    elif args.command == "reset":
        print(api.reset())
    elif args.command == "add":
        print(api.add(args.name, str(args.port), args.password, str(args.monthly_traffic)))
    elif args.command == "del":
        print(api.delete(args.name))
    elif args.command == "sub":
        print(api.sub(args.name))
    elif args.command == "list":
        print(api.list_all())
    else:
        pass
