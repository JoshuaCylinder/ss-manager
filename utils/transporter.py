import abc
import os.path
import socket
from utils.encryption import encrypt as e, decrypt as d

SENDER = 0
RECEIVER = 1


class TransporterBase:
    """
    Simple data transporter. Only for ask and answer.
    """
    def __init__(self, addrport_or_sock: str):
        if ":" in addrport_or_sock:
            self.conn_type = socket.AF_INET
            self.address = (addrport_or_sock.split(":")[0], int(addrport_or_sock.split(":")[1]))
        else:
            if os.path.exists(addrport_or_sock):
                os.remove(addrport_or_sock)
            self.conn_type = socket.AF_UNIX
            self.address = addrport_or_sock
        self.protocol = 0
        self.sock = None

    def init_sock(self, character) -> socket.socket:
        """
        Init sock item
        """
        sock = socket.socket(self.conn_type, self.protocol)
        if character == RECEIVER:
            # receiver
            sock.bind(self.address)
        else:
            # sender
            sock.connect(self.address)
        return sock

    @abc.abstractmethod
    def send(self, data):
        """
        simple send data
        """
        pass

    @abc.abstractmethod
    def recv(self, handler):
        """
        eternally recv data with handler
        """
        pass


class TCPTransporter(TransporterBase):
    def init_sock(self, character) -> socket.socket:
        self.protocol = socket.SOCK_STREAM
        sock = super().init_sock(character)
        if character == RECEIVER:
            # Set connection stack
            sock.listen(5)
        return sock

    def send(self, data):
        self.sock = self.init_sock(SENDER)
        self.sock.sendall((e(data) + "\n").encode())
        return d(self._real_recv(self.sock))

    def _real_recv(self, sock):
        response = b''
        try:
            while data := sock.recv(1024):
                response += data.strip()
                if data.endswith(b"\n"):
                    break
            return response.decode()
        except (ConnectionResetError, ConnectionAbortedError):
            self.sock.close()

    def recv(self, handler):
        self.sock = self.init_sock(RECEIVER)
        while True:
            try:
                sock, address = self.sock.accept()
                data = e(handler(d(self._real_recv(sock)))).encode()
                sock.sendall(data)
                sock.close()
            except KeyboardInterrupt:
                break


class UDPTransporter(TransporterBase):
    def init_sock(self, character) -> socket.socket:
        self.protocol = socket.SOCK_DGRAM
        return super().init_sock(character)

    def send(self, data):
        self.sock = self.init_sock(SENDER)
        data = e(data)
        if len(data) > 1024:
            raise RuntimeError("Data size is too big for UDP transporter (more than 1024 bytes). Use TCP instead.")
        self.sock.send(data.encode())
        data, _ = self.sock.recvfrom(1024)
        return d(data.decode())

    def recv(self, handler):
        self.sock = self.init_sock(RECEIVER)
        while True:
            try:
                data, address = self.sock.recvfrom(1024)
                self.sock.sendto(e(handler(d(data.decode()))).encode(), address)
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    r = TCPTransporter("/tmp/receiver.sock")
