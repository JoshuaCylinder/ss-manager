import argparse
import subprocess
import threading

from utils.manager import supervisor, add_user, reset, load


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="ss-manager-controller",
        description="A simple program using for sharing shadowsocks server. Basing on ss-manager."
    )
    subprasers = parser.add_subparsers(dest="command", required=True)
    subprasers.add_parser("run", help="run main controller.")
    subprasers.add_parser("reset", help="reset users' traffic. Normally used by crontab.")
    parser.add_argument("--filename", type=str, default="ss-manager.csv",
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
    parser.add_argument("--addrport-or-sock", type=str, default="/tmp/manager.sock",
                        help="address of ss-manager. Supporting net address and port or UDS. "
                             "Using /tmp/manager.sock by default.")
    parser.add_argument("--reset-date", type=int, default=1,
                        help="traffic record refresh date. Using 1 by default.")
    parser.add_argument("--reset-time", type=int, default=1,
                        help="traffic record refresh time. "
                             "Using 1 indicating record refreshed at 1:00 on reset date by default.")

    args = parser.parse_args()
    # Start ss-manager
    subprocess.Popen(["/usr/bin/ss-manager",
                      "--manager-address", "/tmp/manager.sock",
                      "--executable", "/usr/bin/ss-server",
                      "-c", "/etc/shadowsocks-libev/config.json"])
    # Load data and init users
    load(**args.__dict__)
    if args.command == "run":
        t = threading.Thread(target=supervisor)
        t.start()
        t.join()
    elif args.command == "reset":
        reset()
    else:
        pass
