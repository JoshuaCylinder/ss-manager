import json
import socket
import re

ip_re = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")


class SSManagerController:
    def __init__(self, addrport_or_sock: str):
        if ":" in addrport_or_sock:
            self.type = socket.AF_INET
            self.address = (addrport_or_sock.split(":")[0], int(addrport_or_sock.split(":")[1]))
        else:
            self.type = socket.AF_UNIX
            self.address = addrport_or_sock

    def _call(self, to_send: str):
        sock = socket.socket(self.type, socket.SOCK_DGRAM)
        sock.sendto((to_send + "\n").encode(), self.address)
        return sock.recvfrom(1024 * 1024)[0].decode()

    def ping(self):
        return json.loads(self._call("ping")[6:])

    def add(self, port: int, password: str):
        return self._call('add: {"server_port": '+str(port)+', "password": "'+password+'"}')

    def remove(self, port: int):
        return self._call('remove: {"server_port": '+str(port)+'}')


if __name__ == '__main__':
    print(SSManagerController("113.31.102.202:10001").ping())
    # print(add(8388, "3de30458-ecb7-4607-b84b-4a72e81ab3cf"))
