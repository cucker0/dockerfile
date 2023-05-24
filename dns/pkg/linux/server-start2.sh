#!/usr/bin/dumb-init /bin/sh

## launch a process in the background
# start PostgreSQL
PGDATA=/var/lib/pgsql/11/data/
/usr/pgsql-11/bin/postgresql-11-check-db-dir ${PGDATA}
/usr/pgsql-11/bin/postmaster -D ${PGDATA}
# start url-forwarder
LOG_PATH=/data/logs/url-forwarder;
/usr/bin/bash -c "if [ ! -d ${LOG_PATH} ]; then mkdir -p ${LOG_PATH}; fi; /bin/sleep 2";
/usr/local/java/jdk/bin/java \
  -server -Xms2g -Xmx2g -XX:+UseG1GC -verbose:gc \
  -XX:+HeapDumpOnOutOfMemoryError \
  -Duser.timezone=GMT+8 \
  -Xlog:gc*=info:file=/data/logs/url-forwarder/url-forwarder-gc.log::filesize=50M,filecount=4 \
  -XX:HeapDumpPath=/data/logs/url-forwarder \
  -jar /data/software/url-forwarder/url-forwarder-0.0.1-SNAPSHOT.jar \
  --spring.config.additional-location=/data/software/url-forwarder/application.yml &
# start named (bind)
/usr/local/bind/sbin/named -n 1 -u named -c /usr/local/bind/etc/named.conf

## At the end, launch another process in the foreground
# start BindUI
/usr/local/python3.11.3/bin/python3 /data/webroot/BindUI/manage.py runserver 0.0.0.0:8000