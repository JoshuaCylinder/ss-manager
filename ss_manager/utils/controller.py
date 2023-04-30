import json
import re
from ss_manager.utils.transporter import UDPTransporter

ip_re = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")


class SSManagerController:
    def __init__(self, addrport_or_sock: str):
        self.transporter = UDPTransporter(addrport_or_sock)

    def ping(self):
        return json.loads(self.transporter.send("ping")[6:])

    def add(self, port: int, password: str):
        return self.transporter.send('add: {"server_port": '+str(port)+', "password": "'+password+'"}')

    def remove(self, port: int):
        return self.transporter.send('remove: {"server_port": '+str(port)+'}')


if __name__ == '__main__':
    print(SSManagerController("/tmp/manager.sock").remove(8389))
