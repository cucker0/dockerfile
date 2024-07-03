## nginx_make_install

Make and install Nginx，expanded of luajit2-2, openssl, ngx_devel_kit, lua-nginx-module, lua-resty-core, lua-resty-lrucache, ngx_healthcheck_module, ngx_dynamic_upstream

## Supported tags and respective `Dockerfile` links
* [`cucker/nginx_make_install:1.0`, `latest`, `nginx-1.26.1`](https://github.com/cucker0/dockerfile/blob/main/nginx_make_install/Dockerfile_1.0)

## How to use
```bash
mkdir -p /data/docker-volume/nginx-xx /data/docker-volume/nginx-xx-log

docker run --name waf \
 -d \
 -p 80:80/tcp \
 -p 443:443/tcp \
 -v /docker-volume/nginx-xx:/etc/nginx \
 -v /data/docker-volume/nginx-xx-log:/usr/local/nginx/logs/ \
 cucker/nginx_make_install:latest
```
