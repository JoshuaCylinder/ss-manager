import os.path
import csv
import random
import time
import uuid
from prettytable import PrettyTable

import settings
from utils.controller import SSManagerController

users = []


class User:
    def __init__(self, port: int = None, password: str = None, last_traffic: int = None,
                 monthly_traffic: int = settings.default_monthly_traffic):
        if not port:
            # Create user
            port = random.choice(settings.port_pool)
            settings.port_pool.remove(port)
        self.port = port
        self.password = password or str(uuid.uuid4())
        self.total_traffic = self.current_traffic = last_traffic or monthly_traffic
        self.monthly_traffic = monthly_traffic
        if self.current_traffic:
            settings.controller.add(self.port, self.password)

    @property
    def row_data(self):
        return [str(self.port), self.password, str(self.monthly_traffic), str(self.current_traffic)]

    def refresh(self, traffic_used: int):
        """
        Refresh traffic usage return whether this user is still valid
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
            user.refresh(traffic_data[str(user.port)])
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
                # port, password, monthly_traffic, last_traffic
                users.append(User(int(row[0]), row[1], int(row[3]), int(row[2])))
                if int(row[0]) not in settings.port_pool:
                    raise RuntimeError(
                        f"User of line {index + 1} with port {row[0]} is not in current port pool. "
                        f"This issue maybe caused by the modification of user port range. "
                        f"You must edit data file by yourself or use other appropriate port range."
                    )
                settings.port_pool.remove(int(row[0]))


def supervisor():
    # Start service
    while True:
        try:
            time.sleep(settings.refresh_interval)
            _refresh()
        except KeyboardInterrupt:
            break


def add_user(monthly_traffic: int):
    users.append(User(monthly_traffic=monthly_traffic))
    _refresh()


def del_user(port: int):
    settings.controller.remove(port)
    for user in users:
        if user.port == port:
            users.remove(user)
            break
    _refresh()


def list_users():
    table = PrettyTable(['port', 'password', 'monthly_traffic', 'last_traffic'])
    for user in users:
        table.add_row([
            str(user.port), user.password,
            str(round(user.monthly_traffic / 1024 / 1024 / 1024, 2)) + "GB",
            str(round(user.current_traffic / 1024 / 1024 / 1024, 2)) + "GB"
        ])
    return str(table)


def reset():
    for user in users:
        user.reset()


__all__ = ["load", "supervisor", "reset", "add_user", "del_user", "list_users"]
