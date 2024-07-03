## WAF

A WAF extend with Nginx.

## Supported tags and respective `Dockerfile` links
* [`cucker/waf:1.0`, `latest`, `nginx-1.26.1`](https://github.com/cucker0/dockerfile/blob/main/WAF/Dockerfile_1.0)

## How to use
```bash
docker run --name waf \
 -d \
 -p 80:80/tcp \
 -p 443:443/tcp \
 -p 17818:17818/tcp \
 cucker/waf:latest


// 或
mkdir -p /data/docker-volume/waf /data/docker-volume/waf-log

docker run --name waf \
 -d \
 -p 80:80/tcp \
 -p 443:443/tcp \
 -p 17818:17818/tcp \
 -v /data/docker-volume/waf:/etc/nginx \
 -v /data/docker-volume/waf-log:/usr/local/nginx/logs \
 cucker/waf:latest
```

* WAF admin Web

http://<IP>:17818/man

User：admin  
Password：Waf.123

## /etc/nginx directory structure
```bash
$  tree -L 2 /etc/nginx
/data/docker-volume/waf/
├── auth_basic
├── conf.d  // nginx Web Server 配置文件
│   ├── default.conf
│   └── wafman.conf
├── fastcgi.conf
├── fastcgi.conf.default
├── fastcgi_params
├── fastcgi_params.default
├── httpGuard
│   ├── captcha
│   ├── configBackup
│   ├── config.lua  // httpGuard 主要配置文件
│   ├── guard_dynamic.lua
│   ├── guard_static.lua
│   ├── html  // httpGuard 管理后台 API
│   ├── init.lua
│   ├── logs  // httpGuard 调试日志
│   ├── README.md
│   ├── runtime.lua
│   └── url-protect  // httpGuard IP黑名单、IP白名单等模块的ACL
├── koi-utf
├── koi-win
├── man  // http://<IP>:17818/man 管理后台
│   ├── index.html
│   └── src
├── mime.types
├── mime.types.default
├── nginx.conf  // 入口配置文件
├── nginx.conf.default
├── scgi_params
├── scgi_params.default
├── stream.d
│   └── README.md
├── uwsgi_params
├── uwsgi_params.default
└── win-utf
```