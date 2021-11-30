# httpd

## Environment
* OS  
    debian 11.1

* Tools  
    iproute2, net-tools, curl, dnsutils

## Supported tags and respective `Dockerfile` links
* [`2.4`, `2.4-debian-httpd`](https://github.com/cucker0/dockerfile/blob/main/httpd/Dockerfile)

## How to use this image
```
docker run -d --name myhttpd -p 8080:80 cucker/httpd
```