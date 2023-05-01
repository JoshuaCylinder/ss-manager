#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

echo "Running as root"

if [[ "$(cat /etc/issue | grep Debian)" == "" ]] && [[ "$(cat /etc/issue | grep Ubuntu)" == "" ]]
then
  echo "This script can only be used on Debian or Ubuntu"
  exit 1
fi

# Install shadowsocks-libev if not exists
apt update && apt install -y python3 python3-pip shadowsocks-libev

# Disable default ss-server service to prevent port conflict
systemctl stop ss-server
systemctl disable ss-server

# Initiate ss-manager service
rm -f /usr/lib/systemd/system/ss-manager.service
cat << EOF >> /usr/lib/systemd/system/ss-manager.service
[Unit]
Description=Shadowsocks Manager Service
After=network-online.target
Wants=network-online.target

[Service]
DynamicUser=true
Type=simple
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
EnvironmentFile=/etc/default/shadowsocks-libev
LimitNOFILE=32768
ExecStart=/usr/bin/ss-manager -D /tmp/ss-manager --manager-address 127.0.0.1:7968 --executable /usr/bin/ss-server -c /etc/shadowsocks-libev/config.json

[Install]
WantedBy=multi-user.target
EOF

# start ss-manager service
systemctl daemon-reload
systemctl stop ss-manager
systemctl enable ss-manager
systemctl start ss-manager

# Install package
pip3 install dist/ss-manager-1.0.0.tar.gz

# Initiate ss-managerd service
rm -f /usr/lib/systemd/system/ss-managerd.service
cat << EOF >> /usr/lib/systemd/system/ss-managerd.service
[Unit]
Description=Shadowsocks Manager Service Daemon
After=ss-manager.service
Wants=ss-manager.service

[Service]
User=root
Type=simple
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
EnvironmentFile=/etc/default/shadowsocks-libev
LimitNOFILE=32768
ExecStart=ss-managerd -ss \$SS_ENTRANCE run
ExecStopPost=sleep 2

[Install]
WantedBy=multi-user.target
EOF

# start ss-manager service
systemctl daemon-reload
systemctl stop ss-managerd
systemctl enable ss-managerd
systemctl start ss-managerd

echo "Successfully installed ss-manager"
