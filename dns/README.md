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

* url-forwarder
    ```bash
    # 1. run url-forwarder container
    docker run -d --name url-forwarder -p 80:80 -v /etc/dns/url-forwarder:/etc/url-forwarder cucker/dns:url-forwarder_2.0
        
    # 2.  modify /etc/url-forwarder/application.yml, include connection database info.
    # 可配置只读用户
    
    # 3. restart url-forwarder container
    docker restart --time 0 url-forwarder
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
    docker restart --time 0 BindUI
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
    docker restart --time 0 bind
    ```

#### Storage Backend with PostgreSQL
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

* url-forwarder
    ```bash
    # 1. run url-forwarder container
    docker run -d --name url-forwarder -p 80:80 -v /etc/dns/url-forwarder:/etc/url-forwarder cucker/dns:url-forwarder_2.0
        
    # 2.  modify /etc/url-forwarder/application.yml, include connection database info.
    
    # 3. restart url-forwarder container
    docker restart --time 0 url-forwarder
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
    docker restart --time 0 BindUI
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


docker build -f ./Dockerfile_BindUI -t cucker/dns:BindUI_2.0 .
```