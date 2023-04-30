from ss_manager.utils.controller import SSManagerController

data_filename = "/var/lib/ss-manager.csv"
default_monthly_traffic = 100
start_port = 8001
end_port = 8501
refresh_interval = 30
ss_manager_address = "127.0.0.1:7968"
api_address = "127.0.0.1:7969"
key = b"0123456789abcdef"
ss_server = "localhost"
ss_encryption = "aes-128-gcm"
reset_date = 1
reset_time = 0

controller = SSManagerController(ss_manager_address)
port_pool = list(range(start_port, end_port))
