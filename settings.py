from utils.controller import SSManagerController

data_filename = "/var/lib/ss-manager.csv"
sock = "/tmp/ss-manager-controller.sock"
default_monthly_traffic = 100
start_port = 8001
end_port = 8501
refresh_interval = 30
addrport_or_sock = "/tmp/manager.sock"
key = b"0123456789abcdef"
reset_date = 1
reset_time = 0

controller = SSManagerController(addrport_or_sock)
port_pool = list(range(start_port, end_port))
