import argparse
import random
import socket
import subprocess
import threading

from utils.encryption import format_secret
from utils.manager import supervisor, reset, load
from utils.api import api_controller


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
    add.add_argument("--monthly-traffic", type=str, default=100,
                     help="monthly traffic set for this user (GB). Using 100 by default.")
    delete = subprasers.add_parser("del", help="delete user from ss-manager")
    delete.add_argument("--port", type=str, required=True,
                        help="indicate the port of user to remove")
    parser.add_argument("--key", type=str,
                        default=lambda: "".join([random.choice("01234567890abcdef") for _ in range(16)]).encode(),
                        help="the AES key of network transportation encryption.")
    parser.add_argument("--filename", type=str, default="/var/lib/ss-manager.csv",
                        help="name of the csv file used for persistent storage of data. "
                             "Using /var/lib/ss-manager.csv by default.")
    parser.add_argument("--start-port", type=int, default=8001,
                        help="users' port pool start point (included). Using 8001 by default.")
    parser.add_argument("--end-port", type=int, default=8501,
                        help="users' port pool end point (not included). Using 8501 by default.")
    parser.add_argument("--default-monthly-traffic", type=int, default=100,
                        help="default monthly traffic (GB). Using 100 by default.")
    parser.add_argument("--refresh-interval", type=int, default=30,
                        help="interval of writing data and check traffic usage. Using 30 by default.")
    parser.add_argument("--addrport-or-sock", type=str, default="/tmp/manager.sock",
                        help="address of ss-manager. Supporting net address and port or UDS. "
                             "Using /tmp/manager.sock by default.")
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
        subprocess.Popen(["/usr/bin/ss-manager",
                          "--manager-address", "/tmp/manager.sock",
                          "--executable", "/usr/bin/ss-server",
                          "-c", "/etc/shadowsocks-libev/config.json"])
        threading.Thread(target=api_controller).start()
        supervisor()
    elif args.command == "reset":
        reset()
    elif args.command == "add":
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        sock.sendto(f"add:{args.monthly_traffic * 1024 * 1024 * 1024}".encode(), "/tmp/ss-manager-controller.sock")
        print(sock.recvfrom(1024 * 1024)[0].decode())
    elif args.command == "add":
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        sock.sendto(f"del:{args.port}".encode(), "/tmp/ss-manager-controller.sock")
        print(sock.recvfrom(1024 * 1024)[0].decode())
    elif args.command == "list":
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        sock.sendto("list".encode(), "/tmp/ss-manager-controller.sock")
        print(sock.recvfrom(1024 * 1024)[0].decode())
    else:
        pass
