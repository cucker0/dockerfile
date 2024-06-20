# DNS


## What's this
这是一款基于BIND和WEB的智能DNS域名管理系。使用BIND + DLZ + MySQL/PostgreSQL + Django + Spring Boot技术进行开发，支持常用的DNS记录类型，并额外扩展了支持HTTP URL转发的显性URL、隐性URL记录。系统降低了域名管理的管理和使用成本，成为一款易用的企业级域名管理系统。

## Supported tags and respective `Dockerfile` links
* All in One
    * [`all-1.0`, `latest`, `BIND_9.12.1, PostgreSQL 11.3`, `Multiple Service Base on dumb-init`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_all_1.0)
    * [`all-1.1`, `BIND_9.12.4, PostgreSQL 11.3`, `Multiple Service Base on dumb-init`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_all_1.1) 
    * [`all-2.2`, `BIND_9.16.39, MySQL 8+`, `Multiple Service Base on dumb-init`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_2.2)
    * [`all-2.1`, `BIND_9.16.39, MySQL 8+`, `Multiple Service Base on Systemd`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_2.1)
    * [`all-2.0`, `BIND_9.16.39, MySQL 8+`, `Multiple Service Base on Systemd`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile)

* Muilt components
    * [`bind_dlz-mysql_2.0`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_BIND_dlz-mysql)
    * [`bind_dlz-postgres_2.0`, `BIND_9.16.39, PostgreSQL 15.2`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_BIND_dlz-postgres)
    * [`BindUI_2.0`, `MySQL 8+`, `PostgreSQL 12-15`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_BindUI)
    * [`url-forwarder_2.0`, `MySQL 8+`, `PostgreSQL 11-15`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_url-forwarder)
    * [`dns_nginx_proxy_2.0`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_DNS_nginx_proxy)
    * [`bind_dlz-postgres_1.0`, `BIND_9.12.1, <= PostgreSQL 11`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_BIND_dlz-postgres_1.0)
    * [`BindUI_1.0`, `<= PostgreSQL 11`, `Django 3.2.18`](https://github.com/cucker0/dockerfile/blob/main/dns/Dockerfile_BindUI_1.0)

## Manuals
https://www.yuque.com/cucker/udwka0/emk0i5bcgfrcv4m9?singleDoc# 《BindUI 智能 DNS 域名管理系使用文档》

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
 cucker/dns:all-1.0

# or
docker run -d --name dns \
 --restart=always \
 -p 53:53/udp \
 -p 53:53/tcp \
 -p 127.0.0.1:953:953/tcp \
 -p 80:80/tcp \
 -p 8000:8000/tcp \
 cucker/dns:all-1.0
 
# or
docker run -d --name dns \
 --restart=always \
 -p 53:53/udp \
 -p 53:53/tcp \
 -p 127.0.0.1:953:953/tcp \
 -p 80:80/tcp \
 -p 8000:8000/tcp \
 cucker/dns:all-1.1

# or
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

### Muilt Components

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
    新建数据库 dns，新建用户该库的超级用户 dns_wr，密码为 Ww123456!
    
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

* BIND
    ```bash
    docker run -d --name bind  \
     --restart=always \
     -p 53:53/udp \
     -p 53:53/tcp \
     -p 127.0.0.1:953:953/tcp \
     -v /etc/dns/named:/etc/named \
     cucker/dns:bind_dlz-mysql_2.0
     
    # /etc/dns/named/docker_init_info.sh 文件中，修改正确数据库连接信息，不正确的数据库连接信息将导致容器启动失败。
    # 可配置只读用户

    # 重启容器
    docker restart --time 0 bind
    ```
#### Storage Backend with PostgreSQL 15
* PostgreSQL
    ```bash
    docker run -d --name postgresql \
     -e POSTGRES_DB=dns \
     -e POSTGRES_USER=dns_wr \
     -e POSTGRES_PASSWORD=Ww123456! \
     -e POSTGRES_HOST_AUTH_METHOD=scram-sha-256 \
     -v /data/postgresql/data:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:15.2
    ```
    新建数据库 dns，新建用户该库的超级用户(OWNER) dns_wr，密码为 Ww123456!
    
    如果需要创建只读用户，等 BindUI 初始化数据库后，再创建。
    ```bash
    docker exec -it postgresql bash
    # 在容器中执行下列命令
    psql -h 127.0.0.1 -p 5432 -U dns_wr -d dns
    // 创建只读用
    CREATE USER dns_r WITH ENCRYPTED PASSWORD 'Rr123456!';

    // 如果 Django migrate 生成表后，没有 select 权限，请再次执行下面的几条授权语句。
    -- 设置默认事务只读
    ALTER USER dns_r SET default_transaction_read_only=on;
    -- 赋予用户连接数据库bind_ui的权限
    GRANT CONNECT ON DATABASE dns TO dns_r;
    -- 切换到指定库bind_ui
    \c dns

    --schema public 所有表的指定权限授权给指定的用户
    GRANT USAGE ON SCHEMA public TO dns_r;
    -- schema public 以后新建的表的指定权限赋予给指定的用户
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO dns_r;
    -- schema public 的所有SEQUENCES(序列)的指定权限授权给指定的用户
    GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO dns_r;
    -- schema public 下的表的select权限授权给指定用户 
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO dns_r; 
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
    docker restart --time 0 bind
    ```

#### Storage Backend with PostgreSQL 11
* PostgreSQL
    ```bash
    docker run -d --name postgresql \
     -e POSTGRES_DB=dns \
     -e POSTGRES_USER=dns_wr \
     -e POSTGRES_PASSWORD=Ww123456! \
     -e POSTGRES_HOST_AUTH_METHOD=scram-sha-256 \
     -v /data/postgresql11/data:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:11.3
    ```
    新建数据库 dns，新建用户该库的超级用户(OWNER) dns_wr，密码为 Ww123456!
    
    如果需要创建只读用户，等 BindUI 初始化数据库后，再创建。
    ```bash
    docker exec -it postgresql bash
    # 在容器中执行下列命令
    psql -h 127.0.0.1 -p 5432 -U dns_wr -d dns
    // 创建只读用
    CREATE USER dns_r WITH ENCRYPTED PASSWORD 'Rr123456!';

    // 如果 Django migrate 生成表后，没有 select 权限，请再次执行下面的几条授权语句。
    -- 设置默认事务只读
    ALTER USER dns_r SET default_transaction_read_only=on;
    -- 赋予用户连接数据库bind_ui的权限
    GRANT CONNECT ON DATABASE dns TO dns_r;
    -- 切换到指定库bind_ui
    \c dns

    --schema public 所有表的指定权限授权给指定的用户
    GRANT USAGE ON SCHEMA public TO dns_r;
    -- schema public 以后新建的表的指定权限赋予给指定的用户
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO dns_r;
    -- schema public 的所有SEQUENCES(序列)的指定权限授权给指定的用户
    GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO dns_r;
    -- schema public 下的表的select权限授权给指定用户 
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO dns_r; 
    ```
    
* BIND
    ```bash
    docker run -d --name bind  \
     --restart=always \
     -p 53:53/udp \
     -p 53:53/tcp \
     -p 127.0.0.1:953:953/tcp \
     -v /etc/dns/named:/etc/named \
     cucker/dns:bind_dlz-postgres_1.0
     
    # /etc/dns/named/docker_init_info.sh.sh 文件中，修改正确数据库连接信息，不正确的数据库连接信息将导致容器启动失败。

    # 重启容器
    docker restart --time 0 bind
    ```

#### Common Components (MySQL and PostgreSQL Storage Backend)

* BindUI

    * Support >= PostgreSQL 12, and MySQL 8+
    ```bash
    docker run -d --name BindUI \
     --restart=always \
     -p 8000:8000 \
     -v /etc/dns/BindUI:/etc/BindUI \
     cucker/dns:BindUI_2.0
     
    # /etc/dns/BindUI/docker_init_info.sh 文件中，修改正确数据库连接等信息。需要配置可读写的用户

    # 重启容器
    docker restart --time 0 BindUI
    ```
    
    * Support <= PostgreSQL 11, and MySQL 8+
    ```bash
    docker run -d --name BindUI \
     --restart=always \
     -p 8000:8000 \
     -v /etc/dns/BindUI:/etc/BindUI \
     cucker/dns:BindUI_1.0
     
    # /etc/dns/BindUI/docker_init_info.sh 文件中，修改正确数据库连接等信息。需要配置可读写的用户

    # 重启容器
    docker restart --time 0 BindUI
    ```
    
* url-forwarder
    ```bash
    # 1. run url-forwarder container
    docker run -d --name url-forwarder -p 80:80 -v /etc/dns/url-forwarder:/etc/url-forwarder cucker/dns:url-forwarder_2.0
        
    # 2. modify /etc/url-forwarder/application.yml, include connection database info.
    # 可配置只读用户
    
    # 3. restart url-forwarder container
    docker restart --time 0 url-forwarder
    ```
    
* DNS nginx proxy
    ```bash
    docker run -d --name dns-proxy \
     --restart=always \
     -p 53:53/udp \
     -p 53:53/tcp \
     -v /etc/dns/nginx:/etc/nginx \
     cucker/dns:dns_nginx_proxy_2.0
     
    # 修改 /etc/nginx/stream.d/dns.conf
    # 添加 或 删除 upstream 中的 server 节点
    # 示例：
    upstream dns_upstream {
        zone dns_du 64k;
        least_conn;
        server 10.100.240.133:53 weight=10 max_fails=2 fail_timeout=30s;
        server 10.100.240.134:53 weight=10 max_fails=2 fail_timeout=30s;
        server 10.100.240.134:54 weight=10 max_fails=2 fail_timeout=30s;
        server 10.100.240.134:55 weight=10 max_fails=2 fail_timeout=30s;
        #check interval=3000 rise=2 fall=3 timeout=3000 default_down=true type=udp;
    }
    ...

    # 重启容器
    docker restart dns-proxy
    ```

## Performance
`BIND 9.12.1/BIND 9.12.4 + PostgreSQL 11` QPS up to 40000+.

`BIND 9.16.36 + MySQL 8` QPS up to 1000+.

`BIND 9.16.36 + PostgreSQL 15` QPS up to 1250+.

**Proposal：**  
* `postgres:11.3` + `cucker/dns:bind_dlz-postgres_1.0` + `cucker/dns:BindUI_1.0` + `cucker/dns:url-forwarder_2.0` [+ `cucker/dns:dns_nginx_proxy_2.0`]
* `cucker/dns:all-1.0` (All in One)
* `cucker/dns:all-1.1` (All in One)

## All in One System Information
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

* PostgreSQL
    ```
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
    5432/tcp -> PostgreSQL
    ```

## Project
[dns](https://github.com/cucker0/dockerfile/blob/main/dns/)

## Docker build
```bash
cd <Dockerfile_root_path>
docker build -f ./Dockerfile -t cucker/dns:all-2.0 .

// or
docker build --no-cache -f ./Dockerfile -t cucker/dns:all-2.0 .

// or 
docker build -f ./Dockerfile_2.1 -t cucker/dns:all-2.1 .

docker build -f ./Dockerfile_BindUI -t cucker/dns:BindUI_2.0 .

docker build -f ./Dockerfile_DNS_nginx_proxy -t cucker/dns:dns_nginx_proxy_2.0 .
```