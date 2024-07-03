## WAF

A WAF extend with Nginx.

## Supported tags and respective `Dockerfile` links
* [`cucker/waf:1.0`, `latest`, `nginx-1.26.1`](https://github.com/cucker0/dockerfile/blob/main/WAF/Dockerfile_1.0)

## How to use
```bash
mkdir -p /data/docker-volume/nginx-xx /data/docker-volume/nginx-xx-log

docker run --name nginx-xx \
 -d \
 -p 80:80/tcp \
 -p 443:443/tcp \
 -p 17818:17818/tcp \
 -v /docker-volume/nginx-xx:/etc/nginx \
 -v /data/docker-volume/nginx-xx-log:/usr/local/nginx/logs \
 cucker/waf:latest
```
