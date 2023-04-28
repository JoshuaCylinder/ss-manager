# SS Manager

This project is a tool for sharing Shadowsocks protocol dedicated line nodes, written in Python and relying on the
ss-manager executable program of shadowsocks-libev.

## Features

- Monitor program: start ss-manager monitor, periodically synchronize the traffic usage of each port user to the disk
  file, and synchronize the users with non-empty remaining traffic to ss-manager.
- Add user: add users through the add command.
- Delete user: delete users through the del command.
- Print subscription link: print the subscription link of the specified user through the sub command.
- List all users: list all users through the list command.
- Update traffic regularly: set the time for traffic update and help all users to restore to the monthly traffic limit
  at the specified time.

## Installation

(null)

## Usage

1. Start the monitor: `python main.py run`
2. Add user: `python main.py add -t <monthly traffic>`
3. Delete user: `python main.py del -p <port>`
4. Print subscription link: `python main.py sub -p <port>`
5. List all users: `python main.py list`

## Global parameters

| Parameter Name            | Short | Function                                                                                     | Default Value                     |
|---------------------------|-------|----------------------------------------------------------------------------------------------|-----------------------------------|
| --help                    | -h    | Display help information and exit                                                            |                                   |
| --ss-server               | -ss   | ss-server address or domain name used to generate subscription links                         | localhost                         |
| --ss-encryption           | -se   | ss-server encryption method used to generate subscription links                              | aes-128-gcm                       |
| --key                     | -k    | AES key for network transmission encryption (be sure to modify)                              | 0123456789abcdef                  |
| --data-filename           | -f    | CSV file name for data persistence storage                                                   | ss-manager.csv                    |
| --start-port              | -sp   | Starting port of user port pool (inclusive)                                                  | 8001                              |
| --end-port                | -ep   | End port of user port pool (exclusive)                                                       | 8501                              |
| --default-monthly-traffic | -dmt  | Default monthly traffic limit (GB)                                                           | 100                               |
| --refresh-interval        | -ri   | Interval time for data writing and traffic checking (seconds)                                | 30                                |
| --ss-manager-address      | -sma  | Address of ss-manager, supporting network address and port or Unix domain socket             | /tmp/manager.sock                 |
| --api-address             | -aa   | Address of controller API service, supporting network address and port or Unix domain socket | /tmp/ss-manager-controller.sock   |
| --reset-date              | -rd   | Date for traffic reset                                                                       | 1                                 |
| --reset-time              | -rt   | Time for traffic reset (indicating at what time on reset-date)                               | 1 (indicating 1:00 on reset-date) |

## Future Plans

- Add a web interface to provide user statistics, create and delete users and other functions.
- Add the nickname property for users for easier user management.
- Support operations through Web API.
- Add more logs.
- More protocols (?)
