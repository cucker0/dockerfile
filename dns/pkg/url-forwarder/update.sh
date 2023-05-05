#/bin/bash
#

# 服务名
SERVICENAME=url-forwarder.service

systemctl stop $SERVICENAME
rz -y
systemctl start $SERVICENAME
