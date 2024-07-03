# nginx-install
nginx install package and install script


## How to Install
```
# 可选版本 1.12.1、1.12.2、1.14.2、1.18.0、1.24.0、1.26.1
nginx_version=1.26.1

yum -y install git; \
 mkdir -p /usr/local/src/nginx-${nginx_version}_v0; \
 cd /usr/local/src/nginx-${nginx_version}_v0; \
 git clone https://github.com/cucker0/nginx-install.git; \
 cd nginx-install/nginx-${nginx_version}; \
 bash ./nginx_install.sh; \
 . /etc/profile;

```

## Others
```bash
# nginx upstream check 项目
https://github.com/zhouchangxun/ngx_healthcheck_module

# 阿里nginx_upstream_check_module
https://github.com/yaoweibin/nginx_upstream_check_module
```