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
docker run -d --name dns \
 --restart=always \
 -p 53:53/udp \
 -p 53:53/tcp \
 -p 127.0.0.1:953:953/tcp \
 -p 80:80/tcp \
 -p 8000:8000/tcp \
 cucker/dns:all-2.2

# or
docker run -d --privileged --name dns \
 --restart=always \
 -p 53:53/udp -p 53:53/tcp \
 -p 127.0.0.1:953:953/tcp \
 -p 80:80/tcp \
 -p 8000:8000/tcp \
 cucker/dns:all-2.1

# or
docker run -d --privileged --name dns \
 --restart=always \
 -p 53:53/udp \
 -p 53:53/tcp \
 -p 127.0.0.1:953:953/tcp \
 -p 80:80/tcp \
 -p 8000:8000/tcp \
 cucker/dns:all-2.0
```

### Muilt component
#### Storage Backend with MySQL
* MySQL
    ```bash
    docker run -d --name mysql \
     -e MYSQL_ROOT_PASSWORD=Py123456! \
     -e MYSQL_DATABASE=dns \
     -e MYSQL_USER=dns_wr \
     -e MYSQL_PASSWORD=Ww123456! \
     -p 3306:3306 \
     mysql:8.0.32 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    ```
    
    创建数据库只读用户（如果需要）
    ```bash
    $docker exec -it mysql bash
    // 在容器中执行下列命令
    mysql -uroot -p
    CREATE USER 'dns_r'@'%' IDENTIFIED BY 'Rr123456!';
    GRANT select ON dns.* TO 'dns_r'@'%';

    // 刷新权限
    flush privileges;
    ```

* url-forwarder
    ```bash
    # 1. run url-forwarder container
    docker run -d --name url-forwarder -p 80:80 -v /etc/dns/url-forwarder:/etc/url-forwarder cucker/dns:url-forwarder_2.0
        
    # 2.  modify /etc/url-forwarder/application.yml, include connection database info.
    # 可配置只读用户
    
    # 3. restart url-forwarder container
    docker restart url-forwarder
    ```

* BindUI
    ```bash
    docker run -d --name BindUI \
     --restart=always \
     -p 8000:8000 \
     -v /etc/dns/BindUI:/etc/BindUI \
     cucker/dns:BindUI_2.0
     
    # /etc/dns/BindUI/docker_init_info.sh 文件中，修改正确数据库连接等信息。需要配置可读写的用户

    # 重启容器
    docker restart BindUI
    ```

* BIND
```bash
    docker run -d --name bind  \
     --restart=always \
     -p 53:53/udp \
     -p 53:53/tcp \
     -p 127.0.0.1:953:953/tcp \
     -v /etc/dns/named:/etc/named \
     cucker/dns:bind_dlz-mysql_2.0
     
    # /etc/dns/named/docker_init_info.sh.sh 文件中，修改正确数据库连接信息，不正确的数据库连接信息将导致容器启动失败。
    # 可配置只读用户

    # 重启容器
    docker restart bind
    ```

#### Storage Backend with PostgreSQL
* PostgreSQL
    ```bash
    docker run -d --name mysql \
     -e MYSQL_ROOT_PASSWORD=Py123456! \
     -e MYSQL_DATABASE=dns \
     -e MYSQL_USER=dns_wr \
     -e MYSQL_PASSWORD=Ww123456! \
     -p 3306:3306 \
     mysql:8.0.32 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    ```

* url-forwarder
    ```bash
    # 1. run url-forwarder container
    docker run -d --name url-forwarder -p 80:80 -v /etc/dns/url-forwarder:/etc/url-forwarder cucker/dns:url-forwarder_2.0
        
    # 2.  modify /etc/url-forwarder/application.yml, include connection database info.
    
    # 3. restart url-forwarder container
    docker restart url-forwarder
    ```

* BindUI
    ```bash
    docker run -d --name BindUI \
     --restart=always \
     -p 8000:8000 \
     -v /etc/dns/BindUI:/etc/BindUI \
     cucker/dns:BindUI_2.0
     
    # /etc/dns/BindUI/docker_init_info.sh 文件中，修改正确数据库连接等信息

    # 重启容器
    docker restart BindUI
    ```

* BIND
```bash
    docker run -d --name bind  \
     --restart=always \
     -p 53:53/udp \
     -p 53:53/tcp \
     -p 127.0.0.1:953:953/tcp \
     -v /etc/dns/named:/etc/named \
     cucker/dns:bind_dlz-postgres_2.0
     
    # /etc/dns/named/docker_init_info.sh.sh 文件中，修改正确数据库连接信息，不正确的数据库连接信息将导致容器启动失败。

    # 重启容器
    docker restart bind
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
    EXPOSE 53/udp 53/tcp 953/tcp 80/tcp 8000/tcp 3306/tcp
    53/udp -> bind
    53/tcp -> bind
    953/tcp -> bind
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