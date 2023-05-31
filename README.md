# SS Manager

Other languages: [en](https://github.com/JoshuaCylinder/ss-manager/blob/master/docs/en.md)

����Ŀ��һ�����ڷ���ShadowsocksЭ��ר�߽ڵ�Ĺ��ߣ�����Python��д��������shadowsocks-libev��ss-manager��ִ�г���

## ����

- ��������������ss-manager�ļ�������������ͬ��ÿ���˿��û�������ʹ������������ļ��У���ʣ��������Ϊ�յ��û�ͬ����ss-manager�С�
- ����û���ͨ��add��������û��������ͬ���û���ʱ���Ḳ���Ѿ����ڵ��û���
- ɾ���û���ͨ��del����ɾ���û���
- ��ӡ�������ӣ�ͨ��sub�����ӡָ���û��Ķ������ӡ�
- �г������û���ͨ��list�����г������û���Ϣ�������˿ڣ����룬��������ʣ��������
- ��ʱ�����������趨�������µ�ʱ�䣬��ָ����ʱ����������û��ָ���ÿ���µ������޶��ϡ�

## ��װ

(��)

## ʹ��

1. ������������`python main.py run`
2. ����û���`python main.py add -t <monthly traffic>`
3. ɾ���û���`python main.py del -p <port>`
4. ��ӡ�������ӣ�`python main.py sub -p <port>`
5. �г������û���`python main.py list`

## ȫ�ֲ���

| ������                       | ��д   | ����                               | Ĭ��ֵ                             |
|---------------------------|------|----------------------------------|---------------------------------|
| --help                    | -h   | ��ʾ������Ϣ���˳�                        |                                 |
| --ss-server               | -ss  | �������ɶ������ӵ�ss-server��ַ������          | localhost                       |
| --ss-encryption           | -se  | �������ɶ������ӵ�ss-server���ܷ�ʽ           | aes-128-gcm                     |
| --key                     | -k   | ������ܵ�AES��Կ(����޸�)�����ܷ�ʽΪAES-GCM    | 0123456789abcdef                |
| --data-filename           | -f   | ���ݳ־û��洢��csv�ļ���                   | ss-manager.csv                  |
| --start-port              | -sp  | �û��˿ڳص���ʼ�˿ڣ�������                   | 8001                            |
| --end-port                | -ep  | �û��˿ڳصĽ����˿ڣ���������                  | 8501                            |
| --default-monthly-traffic | -dmt | Ĭ�ϵ����������ƣ�GB��                     | 100                             |
| --refresh-interval        | -ri  | ����д����������ļ��ʱ�䣨�룩                | 30                              |
| --ss-manager-address      | -sma | ss-manager�ĵ�ַ��֧�������ַ�Ͷ˿ڻ�Unix���׽��� | /tmp/manager.sock               |
| --api-address             | -aa  | ������API����ĵ�ַ��֧�������ַ�Ͷ˿ڻ�Unix���׽���   | /tmp/ss-manager-controller.sock |
| --reset-date              | -rd  | �������������                          | 1                               |
| --reset-time              | -rt  | ���������ʱ�䣨��ʾ��reset-date����ļ��㣩      | 1����ʾ��reset-date�����1:00��         |

## δ���ƻ�

- �����ҳ���棬�ṩ�û�ͳ����Ϣ���½�ɾ���û��ȹ��ܡ�
- ֧��ͨ��Web API���в�����
- ������־��¼��
- ����Э�� (?)

