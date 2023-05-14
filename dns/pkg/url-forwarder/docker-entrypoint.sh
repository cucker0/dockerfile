#!/bin/bash
# url-forwarder docker-entrypoint.sh


LOG_PATH=/data/logs/url-forwarder

# 如果 docker run -v 映射卷时，主机目录为空，则复制原始的配置到主机上
copyConfigFile2Host() {
    local TAG_PATH=/etc/url-forwarder/
    if [ -d ${CONFIG_PATH} ]; then
        if [ "$(ls -A ${TAG_PATH})" == "" ]; then
            cp -a /dns/origin/url-forwarder/application.yml  /etc/url-forwarder
        fi
    fi
    

}

_main() {
    copyConfigFile2Host
    
    # mkdir LOG DIR
    /usr/bin/bash -c "if [ ! -d ${LOG_PATH} ]; then mkdir -p ${LOG_PATH}; fi; /bin/sleep 2"
    # start service
    /usr/local/java/jdk/bin/java \
      -server -Xms2g -Xmx2g -XX:+UseG1GC -verbose:gc \
      -XX:+HeapDumpOnOutOfMemoryError \
      -Duser.timezone=GMT+8 \
      -Xlog:gc*=info:file=/data/logs/url-forwarder/url-forwarder-gc.log::filesize=50M,filecount=4 \
      -XX:HeapDumpPath=/data/logs/url-forwarder \
      -jar /data/software/url-forwarder/url-forwarder-0.0.1-SNAPSHOT.jar \
      --spring.config.additional-location=/data/software/url-forwarder/application.yml
    # 如果用户传了参数，则执行用户传的参数命令
    exec "$@"
}

_main "$@"
