from utils.controller import SSManagerController

data_filename = "ss-manager.csv"
default_monthly_traffic = 100 * 1024 * 1024 * 1024
start_port = 8001
end_port = 8501
refresh_interval = 30
addrport_or_sock = "/tmp/manager.sock"
reset_date = 1
reset_time = 0

controller = SSManagerController(addrport_or_sock)
port_pool = list(range(start_port, end_port))
