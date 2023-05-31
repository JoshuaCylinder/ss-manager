# SS Manager

Other languages: [en](https://github.com/JoshuaCylinder/ss-manager/blob/master/docs/en.md)

该项目是一个用于分享Shadowsocks协议专线节点的工具，基于Python编写，依赖于shadowsocks-libev的ss-manager可执行程序。

## 功能

- 监视器程序：启动ss-manager的监视器，周期性同步每个端口用户的流量使用情况到磁盘文件中，将剩余流量不为空的用户同步到ss-manager中。
- 添加用户：通过add命令添加用户，添加相同的用户名时，会覆盖已经存在的用户。
- 删除用户：通过del命令删除用户。
- 打印订阅链接：通过sub命令打印指定用户的订阅链接。
- 列出所有用户：通过list命令列出所有用户信息，包括端口，密码，总流量和剩余流量。
- 定时更新流量：设定流量更新的时间，在指定的时间帮助所有用户恢复到每个月的流量限额上。

## 安装

(略)

## 使用

1. 启动监视器：`python main.py run`
2. 添加用户：`python main.py add -t <monthly traffic>`
3. 删除用户：`python main.py del -p <port>`
4. 打印订阅链接：`python main.py sub -p <port>`
5. 列出所有用户：`python main.py list`

## 全局参数

| 参数名                       | 简写   | 作用                               | 默认值                             |
|---------------------------|------|----------------------------------|---------------------------------|
| --help                    | -h   | 显示帮助信息并退出                        |                                 |
| --ss-server               | -ss  | 用于生成订阅链接的ss-server地址或域名          | localhost                       |
| --ss-encryption           | -se  | 用于生成订阅链接的ss-server加密方式           | aes-128-gcm                     |
| --key                     | -k   | 传输加密的AES密钥(务必修改)，加密方式为AES-GCM    | 0123456789abcdef                |
| --data-filename           | -f   | 数据持久化存储的csv文件名                   | ss-manager.csv                  |
| --start-port              | -sp  | 用户端口池的起始端口（包括）                   | 8001                            |
| --end-port                | -ep  | 用户端口池的结束端口（不包括）                  | 8501                            |
| --default-monthly-traffic | -dmt | 默认的月流量限制（GB）                     | 100                             |
| --refresh-interval        | -ri  | 数据写入和流量检查的间隔时间（秒）                | 30                              |
| --ss-manager-address      | -sma | ss-manager的地址，支持网络地址和端口或Unix域套接字 | /tmp/manager.sock               |
| --api-address             | -aa  | 控制器API服务的地址，支持网络地址和端口或Unix域套接字   | /tmp/ss-manager-controller.sock |
| --reset-date              | -rd  | 流量清零的日期                          | 1                               |
| --reset-time              | -rt  | 流量清零的时间（表示在reset-date当天的几点）      | 1（表示在reset-date当天的1:00）         |

## 未来计划

- 添加网页界面，提供用户统计信息、新建删除用户等功能。
- 支持通过Web API进行操作。
- 完善日志记录。
- 更多协议 (?)

