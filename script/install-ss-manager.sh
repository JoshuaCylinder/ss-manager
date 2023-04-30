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
ExecStart=/usr/bin/ss-manager -D /tmp/ss-manager --manager-address 127.0.0.1:7968 --executable $(which ss-server) -c /etc/shadowsocks-libev/config.json

[Install]
WantedBy=multi-user.target
EOF

# start ss-manager service
systemctl daemon-reload
systemctl stop ss-manager
systemctl enable ss-manager
systemctl start ss-manager

echo "Successfully installed ss-manager"
