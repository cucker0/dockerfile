#!/bin/bash

# 服务名
SERVICENAME=url-forwarder.service

cp $SERVICENAME /etc/systemd/system/
systemctl enable $SERVICENAME