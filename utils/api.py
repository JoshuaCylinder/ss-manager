import socket

from utils.manager import add_user, del_user, list_users


def api_controller():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.bind("/tmp/ss-manager-controller.sock")
    while True:
        data = sock.recvfrom(1024)
        if not data:
            continue
        data = data[0].decode().strip()
        if data.startswith("add") and ":" in data:
            # add user
            add_user(int(data.split(":")[1]))
            sock.sendto(b"ok", data[1])
        elif data == "list":
            sock.sendto(list_users().encode(), data[1])
        elif data.startswith("del"):
            del_user(int(data.split(":")[1]))
            sock.sendto(b"ok", data[1])
        else:
            sock.sendto(b"", data[1])
