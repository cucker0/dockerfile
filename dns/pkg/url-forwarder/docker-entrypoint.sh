#!/bin/bash
# url-forwarder docker-entrypoint.sh


LOG_PATH=/data/logs/url-forwarder

_main() {
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
    
    exec "$@"
}

_main "$@"
