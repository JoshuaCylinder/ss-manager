from utils.controller import SSManagerController

data_filename = "/var/lib/ss-manager.csv"
sock = "/tmp/ss-manager-controller.sock"
default_monthly_traffic = 100
start_port = 8001
end_port = 8501
refresh_interval = 30
ss_manager_address = "/tmp/manager.sock"
api_address = "/tmp/ss-manager-controller.sock"
key = b"0123456789abcdef"
reset_date = 1
reset_time = 0

controller = SSManagerController(ss_manager_address)
port_pool = list(range(start_port, end_port))
