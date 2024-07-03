#!/bin/bash

# 开启基于Basic的认证

# 创建用户、密码，并保存到指定文件。密码为 Waf.123
touch /etc/nginx/auth_basic

htpasswd -c /etc/nginx/auth_basic admin <<EOF
Waf.123
Waf.123
EOF
