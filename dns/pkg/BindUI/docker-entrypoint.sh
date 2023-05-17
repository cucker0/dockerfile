#!/bin/sh
# BindUI docker-entrypoint.sh

CONFIG_PATH=/etc/BindUI/
BindUI_SETTINGS=/data/webroot/BindUI/bindUI/settings.py
PYTHON_PATH=/usr/local/python3.11.3

# 如果 docker run -v 映射卷时，主机目录为空，则复制原始的配置到主机上
copyConfigFile2Host() {
    if [ -d ${CONFIG_PATH} ]; then
        if [ "$(ls -A ${CONFIG_PATH})" == "" ]; then
            cp -a /dns/origin/BindUI/* ${CONFIG_PATH}
        fi
    fi
}

copyConfigFile2Host
# 引入 连接数据库的信息 变量
. /etc/BindUI/docker_init_info.sh

# 更新 BindUI 的数据库连接信息
updateBindUiConfig() {
    if [ ${UPDATE_CONFIG} != 0 ]; then
        # update database connection
        if [ "${DB_TYPE}" == "MySQL" ]; then            
            sed -i "/^#[ ]*import pymysql/s/^#[ ]*//" ${BindUI_SETTINGS}
            sed -i "/^#[ ]*pymysql.version_info/s/^#[ ]*//" ${BindUI_SETTINGS}
            sed -i "/^#[ ]*pymysql.install_as_MySQLdb/s/^#[ ]*//" ${BindUI_SETTINGS}

            sed -i "s#^[ ]*'ENGINE':.*#        'ENGINE': 'django.db.backends.mysql',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'HOST':.*#        'HOST': '${DB_HOST}',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'PORT':.*#        'PORT': '${DB_PORT}',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'NAME':.*#        'NAME': '${DB_NAME}',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'USER':.*#        'USER': '${DB_USER}',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'PASSWORD':.*#        'PASSWORD': '${DB_PASSWORD}',#" ${BindUI_SETTINGS}           
        elif [ "${DB_TYPE}" == "PostgreSQL" ]; then
            sed -i "s/^import pymysql/#&/" ${BindUI_SETTINGS}
            sed -i "s/^pymysql.version_info/#&/" ${BindUI_SETTINGS}
            sed -i "s/^pymysql.install_as_MySQLdb/#&/" ${BindUI_SETTINGS}
            
            sed -i "s#^[ ]*'ENGINE':.*#        'ENGINE': 'django.db.backends.postgresql',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'HOST':.*#        'HOST': '${DB_HOST}',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'PORT':.*#        'PORT': '${DB_PORT}',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'NAME':.*#        'NAME': '${DB_NAME}',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'USER':.*#        'USER': '${DB_USER}',#" ${BindUI_SETTINGS}
            sed -i "s#^[ ]*'PASSWORD':.*#        'PASSWORD': '${DB_PASSWORD}',#" ${BindUI_SETTINGS}
            
        fi
    
        # update URL_FORWARDER_DOMAIN
        sed -i "s#URL_FORWARDER_DOMAIN = .*#URL_FORWARDER_DOMAIN = '${URL_FORWARDER_DOMAIN}'#" /data/webroot/BindUI/bindUI/dns_conf.py
        
        # 重置为不更新配置
        sed -i s'#UPDATE_CONFIG.*#UPDATE_CONFIG=0#' /etc/BindUI/docker_init_info.sh
    fi
}

# init database
initDatabase() {
    if [ ${INIT_DATABASE} != 0 ]; then
        cd /data/webroot/BindUI
        ${PYTHON_PATH}/bin/python3 manage.py migrate
        ${PYTHON_PATH}/bin/python3 manage.py makemigrations
        ${PYTHON_PATH}/bin/python3 manage.py migrate
        echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_SUPERUSER_NAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | ${PYTHON_PATH}/bin/python3 ./manage.py shell
        
        # 重置为禁止初始化
        sed -i s'#INIT_DATABASE.*#INIT_DATABASE=0#' /etc/BindUI/docker_init_info.sh
    fi   
}

_main() {
    copyConfigFile2Host
    updateBindUiConfig
    initDatabase
    
    # start service
    ${PYTHON_PATH}/bin/python3 /data/webroot/BindUI/manage.py runserver 0.0.0.0:8000
    
    # 如果用户传了参数，则执行用户传的参数命令
    exec "$@"
}

_main "$@"
