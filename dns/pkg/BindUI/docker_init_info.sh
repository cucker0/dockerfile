# BindUI 连接数据库的信息

# 是否更新配置，0：不更新配置，1或其他值：更新配置
UPDATE_CONFIG=0
# 是否初始化数据库。0：禁止初始化，1或其他值：进行初始化
INIT_DATABASE=0

# 数据类型，可选值：MySQL、PostgreSQL
DB_TYPE=MySQL

DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=dns
DB_USER=dns_wr
DB_PASSWORD=Ww123456!

# 负责响应 显性URL、隐性URL转发的主机名(域名)，使用FQDN A 记录
URL_FORWARDER_DOMAIN=free.zz.com

# Django Super User
DJANGO_SUPERUSER_NAME=admin
DJANGO_SUPERUSER_EMAIL=admin@my.com
DJANGO_SUPERUSER_PASSWORD=Dns123456!