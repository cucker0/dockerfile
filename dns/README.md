# DNS


## What's this
这是一款基于BIND和WEB的智能DNS域名管理系。使用BIND + DLZ + MySQL/PostgreSQL + Django + Spring Boot技术进行开发，支持常用的DNS记录类型，并额外扩展了支持HTTP URL转发的显性URL、隐性URL记录。系统降低了域名管理的管理和使用成本，成为一款易用的企业级域名管理系统。

## Supported tags and respective `Dockerfile` links
* [`all-2.2`, `latest`, `Multiple Service Base on dumb-init`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_2.2)
* [`all-2.1`, `Multiple Service Base on Systemd`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_2.1)
* [`all-2.0`, `Multiple Service Base on Systemd`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile)

## How to use this image

### All in One
```bash
docker run -d --name dns --restart=always -p 53:53/udp -p 53:53/tcp -p 80:80/tcp -p 8000:8000/tcp -p 3306:3306/tcp cucker/dns:all-2.2

# or
docker run -d --privileged --name dns --restart=always -p 53:53/udp -p 53:53/tcp -p 80:80/tcp -p 8000:8000/tcp -p 3306:3306/tcp cucker/dns:all-2.1

# or
docker run -d --privileged --name dns --restart=always -p 53:53/udp -p 53:53/tcp -p 80:80/tcp -p 8000:8000/tcp -p 3306:3306/tcp cucker/dns:all-2.0
```

## System Information
* BindUI Account Info
    ```
    url：http://<IP_MAP>:8000
    user：admin
    password：Dns123456!
    ```
* MySQL
    ```
    user1：root
    password：Py123456!

    ## database：dns
    user2：'dns_wr'@'%'
    password：Ww123456!

    user3：'dns_r'@'%'
    password：Rr123456!
    ```

* Port Info
    ```
    EXPOSE 53/udp 53/tcp 80/tcp 8000/tcp 3306/tcp
    53/udp -> bind
    53/tcp -> bind
    80/tcp -> url-forwarder
    8000/tcp -> BindUI
    3306/tcp -> MySQL
    ```

## Project
[dns](https://github.com/cucker0/dockerfile/blob/main/dns/)

## Docker build
```bash
cd <Dockerfile_root_path>
chmod +x  pkg/linux/docker-entrypoint.sh
docker build -f ./Dockerfile -t cucker/dns:all-2.0 .
// or
docker build --no-cache -f ./Dockerfile -t cucker/dns:all-2.0 .

# or 
docker build -f ./Dockerfile_2.1 -t cucker/dns:all-2.1 .
```