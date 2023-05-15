#!/bin/bash
# BIND docker-entrypoint.sh

# 引入 BIND 连接数据库的信息 变量
. /etc/named/bind_db_connection_info.sh

LOG_PATH=/data/logs/url-forwarder
CONFIG_PATH=/etc/named/


# 如果 docker run -v 映射卷时，主机目录为空，则复制原始的配置到主机上
copyConfigFile2Host() {
    if [ -d ${CONFIG_PATH} ]; then
        if [ "$(ls -A ${CONFIG_PATH})" == "" ]; then
            cp -a /dns/origin/bind/etc/* ${CONFIG_PATH}
        fi
    fi
}

# 更新 /etc/named/conf/*.conf 的数据库连接信息
updateBindConfig() {
    set -eux
    if [ ${UPDATE_CONFIG} != 0 ]; then
        sed -i 's#{host=.*$#{host='"${DB_HOST}"' dbname='"${DB_NAME}"' ssl=false port='"${DB_PORT}"' user='"${DB_USER}"' pass='"${DB_PASS}"'}#' /etc/named/conf.d/*.conf
        
        # 重置为不更新配置
        sed -i s'#UPDATE_CONFIG.*#UPDATE_CONFIG=0#' /etc/named/bind_db_connection_info.sh
    fi
}

_main() {
    copyConfigFile2Host
    updateBindConfig
    
    # start service
    /usr/local/bind/sbin/named -f -n 1 -u named -c /usr/local/bind/etc/named.conf 
    # 如果用户传了参数，则执行用户传的参数命令
    exec "$@"
}

_main "$@"