import argparse
import random
import threading

import settings
from utils.encryption import format_secret
from utils.manager import supervisor, reset, load
from utils.api import api_handler
from utils.transporter import TCPTransporter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="ss-manager-controller",
        description="A simple program using for sharing shadowsocks server. Basing on ss-manager."
    )
    subprasers = parser.add_subparsers(dest="command", required=True)
    subprasers.add_parser("run", help="run main controller.")
    subprasers.add_parser("reset", help="reset users' traffic. Normally used by crontab.")
    subprasers.add_parser("list", help="print all users' info")
    add = subprasers.add_parser("add", help="add new user")
    add.add_argument("--monthly-traffic", type=int, default=100,
                     help="monthly traffic set for this user (GB). Using 100 by default.")
    delete = subprasers.add_parser("del", help="delete user from ss-manager")
    delete.add_argument("--port", type=str, required=True,
                        help="indicate the port of user to remove")
    parser.add_argument("--key", type=str, default="0123456789abcdef",
                        help="the AES key of network transportation encryption.")
    parser.add_argument("--data-filename", type=str, default="ss-manager.csv",
                        help="name of the csv file used for persistent storage of data. "
                             "Using ss-manager.csv by default.")
    parser.add_argument("--start-port", type=int, default=8001,
                        help="users' port pool start point (included). Using 8001 by default.")
    parser.add_argument("--end-port", type=int, default=8501,
                        help="users' port pool end point (not included). Using 8501 by default.")
    parser.add_argument("--default-monthly-traffic", type=int, default=100,
                        help="default monthly traffic (GB). Using 100 by default.")
    parser.add_argument("--refresh-interval", type=int, default=30,
                        help="interval of writing data and check traffic usage. Using 30 by default.")
    parser.add_argument("--ss-manager-address", type=str, default="/tmp/manager.sock",
                        help="address of ss-manager. Supporting net address and port or UDS. "
                             "Using /tmp/manager.sock by default.")
    parser.add_argument("--api-address", type=str, default="/tmp/ss-manager-controller.sock",
                        help="address of controllers api service. Supporting net address and port or UDS. "
                             "Using /tmp/ss-manager-controller.sock by default.")
    parser.add_argument("--reset-date", type=int, default=1,
                        help="traffic record refresh date. Using 1 by default.")
    parser.add_argument("--reset-time", type=int, default=1,
                        help="traffic record refresh time. "
                             "Using 1 indicating record refreshed at 1:00 on reset date by default.")

    args = parser.parse_args()
    # Init AES key
    format_secret(args)
    # Load data and init users
    load(**args.__dict__)
    if args.command == "run":
        # Start ss-manager
        # subprocess.Popen(["/usr/bin/ss-manager",
        #                   "--manager-address", "/tmp/manager.sock",
        #                   "--executable", "/usr/bin/ss-server",
        #                   "-c", "/etc/shadowsocks-libev/config.json"])
        # /usr/bin/ss-manager --manager-address /tmp/manager.sock --executable /usr/bin/ss-server -c /etc/shadowsocks-libev/config.json

        # Start api controller
        t = threading.Thread(target=TCPTransporter(settings.api_address, settings.key).recv, args=(api_handler, ))
        t.daemon = True
        t.start()
        # Start reset crontab
        # os.system(f"echo '0  {settings.reset_time}    {settings.reset_date} * *   root    "
        #           f"cd /ss-manager-controller && python3 main.py reset' >> /etc/crontab")
        # os.system("cron")
        supervisor()
    elif args.command == "reset":
        reset()
    elif args.command == "add":
        TCPTransporter(settings.api_address, settings.key).send(f"add:{args.monthly_traffic * 1024 * 1024 * 1024}")
    elif args.command == "del":
        TCPTransporter(settings.api_address, settings.key).send(f"del:{args.port}")
    elif args.command == "list":
        TCPTransporter(settings.api_address, settings.key).send("list")
    else:
        pass
