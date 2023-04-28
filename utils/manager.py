import base64
import os.path
import csv
import random
import time
import uuid
from prettytable import PrettyTable

import settings
from utils.controller import SSManagerController
from utils.exceptions import ConflictPortException, UserNotFoundError

users = []


class User:
    def __init__(self, name: str, port: int, password: str, last_traffic: int, monthly_traffic: int):
        self.name = name
        if not port:
            port = random.choice(settings.port_pool)
            settings.port_pool.remove(port)
        else:
            for user in users:
                if user.port == port:
                    raise ConflictPortException(port)
        self.port = port
        self.password = password or str(uuid.uuid4())
        self.total_traffic = self.current_traffic = last_traffic
        self.monthly_traffic = monthly_traffic
        settings.controller.remove(self.port)
        if self.current_traffic:
            settings.controller.add(self.port, self.password)

    @property
    def row_data(self):
        return [self.name, str(self.port), self.password, str(self.monthly_traffic), str(self.current_traffic)]

    def refresh_last_traffic(self, traffic_used: int):
        """
        Refresh traffic usage
        :param traffic_used:
        :return:
        """
        self.current_traffic = self.total_traffic - traffic_used
        if self.current_traffic <= 0:
            self.current_traffic = 0
            settings.controller.remove(self.port)

    def reset(self):
        """
        Reset traffic usage, then reset user on ss-manager
        :return:
        """
        self.total_traffic = self.current_traffic = self.monthly_traffic
        settings.controller.remove(self.port)
        settings.controller.add(self.port, self.password)


def _refresh():
    """
    Sync usage statistics from ss-manager and save to disk file
    :return:
    """
    # Collect users who do not exceed traffic limit to write in data file
    traffic_data = settings.controller.ping()
    with open(settings.data_filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        for index, user in enumerate(users):
            user.refresh_last_traffic(traffic_data[str(user.port)])
            writer.writerow(user.row_data)


def load(**kwargs):
    """
    Load user info and usage statistics from disk file
    :return:
    """
    # Load custom args
    for key, value in kwargs.items():
        setattr(settings, key, value)
    # Load controller and port_pool
    settings.controller = SSManagerController(settings.ss_manager_address)
    settings.port_pool = list(range(settings.start_port, settings.end_port))
    # Load users from file
    if os.path.exists(settings.data_filename) and kwargs["command"] == "run":
        with open(settings.data_filename) as csvfile:
            reader = csv.reader(csvfile)
            for index, row in enumerate(reader):
                # name, port, password, monthly_traffic, last_traffic
                users.append(User(row[0], int(row[1]), row[2], int(row[4]), int(row[3])))
                if int(row[1]) not in settings.port_pool:
                    raise RuntimeError(
                        f"User of line {index + 1} with port {row[0]} is not in current port pool. "
                        f"This issue maybe caused by the modification of user port range. "
                        f"You must edit data file by yourself or use other appropriate port range."
                    )
                settings.port_pool.remove(int(row[1]))


def supervisor():
    # Start service
    while True:
        try:
            time.sleep(settings.refresh_interval)
            _refresh()
        except KeyboardInterrupt:
            for user in users:
                settings.controller.remove(user.port)
            break


def add_user(name: str, port: int, password: str, monthly_traffic: int):
    try:
        del_user(name)
    except UserNotFoundError:
        pass
    traffic = (monthly_traffic or settings.default_monthly_traffic) * 1024 ** 3
    users.append(User(name, port, password, traffic, traffic))
    _refresh()


def list_users():
    table = PrettyTable(['name', 'port', 'password', 'monthly_traffic', 'last_traffic'])
    for user in users:
        table.add_row([
            user.name, str(user.port), user.password,
            str(round(user.monthly_traffic / 1024 / 1024 / 1024, 2)) + "GB",
            str(round(user.current_traffic / 1024 / 1024 / 1024, 2)) + "GB"
        ])
    return str(table)


def _get_user(name: str):
    for user in users:
        if user.name == name:
            return user
    raise UserNotFoundError(name)


def del_user(name: str):
    user = _get_user(name)
    settings.controller.remove(user.port)
    users.remove(user)
    _refresh()


def generate_shadowsocks_subscription_url(server, port, method, password):
    """
    生成Shadowsocks订阅地址
    :param server: 服务器地址
    :param port: 端口号
    :param method: 加密方式
    :param password: 密码
    :return: Shadowsocks订阅地址
    """
    return f"ss://" + base64.urlsafe_b64encode(f"{method}:{password}@{server}:{port}".encode()).decode()


def get_sub(name: str):
    user = _get_user(name)
    return generate_shadowsocks_subscription_url(
        settings.ss_server, user.port, settings.ss_encryption, user.password
    ) + "#" + name


def reset():
    for user in users:
        user.reset()


__all__ = ["load", "supervisor", "reset", "add_user", "del_user", "list_users", "get_sub"]
