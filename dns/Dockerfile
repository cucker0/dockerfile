FROM rockylinux:9.1
LABEL maintainer='Image Maintainers <hanxiao2100@qq.com>'

ENV DJANGO_SUPERUSER_NAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@my.com
ENV DJANGO_SUPERUSER_PASSWORD=Dns123456!
ENV PYTHON_PATH=/usr/local/python3.11.3
ENV BIND_PATH=/usr/local/bind_9.16.39
COPY pkg/linux/CentOS-Stream9-CRB.repo /etc/yum.repos.d/
COPY pkg/linux/RPM-GPG-KEY-centosofficial /etc/pki/rpm-gpg/
ADD pkg/BindUI.tar.gz /data/webroot/
COPY pkg/url-forwarder/* /data/software/url-forwarder/
COPY pkg/BIND/config/dlz-mysql/systemctl/named.service /usr/lib/systemd/system/
COPY pkg/BIND/config/dlz-mysql/etc/named/ ${BIND_PATH}/etc/
COPY pkg/MySQL/* /pkg/MySQL/
COPY pkg/linux/bindui.service /etc/systemd/system/
#COPY pkg/linux/docker-entrypoint.sh /usr/local/bin/
#ADD https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz /usr/local/src/
#ADD https://downloads.isc.org/isc/bind9/9.16.39/bind-9.16.39.tar.xz /usr/local/src/
#ADD https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tar.xz /usr/local/src/
#COPY pkg/JDK/jdk-17_linux-x64_bin.tar.gz /usr/local/src/
#COPY pkg/python/Python-3.11.3.tar.xz /usr/local/src/
#COPY pkg/BIND/bind-9.16.39.tar.xz /usr/local/src/

RUN set -eux; \
    yum clean all; \
    yum makecache; \
    dnf -y install systemd; \
    # 关联动态库; \
    echo -e "/usr/local/lib\n\
/usr/local/lib64\n\
/lib\n\
/lib64\n\
/usr/lib\n\
/usr/lib64\n\
" >> /etc/ld.so.conf; \
    ldconfig; \
    # Install MySQL; \
    dnf -y install https://repo.mysql.com/mysql80-community-release-el9-1.noarch.rpm; \
    # 安装最新版本MySQL; \
    #dnf -y install mysql-server mysql mysql-devel; \
    # 如果是安装指定版本的 MySQL; \
    dnf -y install mysql-community-server-8.0.32 mysql-community-client-8.0.32 mysql-community-devel-8.0.32; \
    bash /usr/bin/mysqld_pre_systemd; \
    /usr/sbin/mysqld --user=mysql -D ; \
    bash /pkg/MySQL/update_root_password.sh; \
    # Install Python; \
    dnf -y install zlib zlib-devel; \
    dnf -y install bzip2 bzip2-devel; \
    dnf -y install ncurses ncurses-devel; \
    dnf -y install readline readline-devel; \
    dnf -y install openssl openssl-devel; \
    dnf -y --skip-broken install openssl-static; \
    dnf -y install xz lzma xz-devel; \
    dnf -y install sqlite sqlite-devel; \
    dnf -y install gdbm gdbm-devel --nobest; \
    dnf -y install tk tk-devel; \
    dnf -y install libffi libffi-devel; \
    dnf -y install gcc automake autoconf libtool make gcc gcc-c++ wget ; \
    cd /usr/local/src; \
    wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tar.xz; \
    tar -Jxvf Python-3.11.3.tar.xz; \
    cd Python-3.11.3/; \
    ./configure --prefix=/usr/local/python3.11.3 --enable-shared CFLAGS=-fPIC; \
    make; \
    make install; \
    echo "/usr/local/python3.11.3/lib/" >> /etc/ld.so.conf; \
    ldconfig; \
    ${PYTHON_PATH}/bin/python3 -m pip install --upgrade pip; \
    ${PYTHON_PATH}/bin/pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r /data/webroot/BindUI/requirements.txt; \
    # Deploy BindUI; \
    cd /data/webroot/BindUI; \
    ${PYTHON_PATH}/bin/python3 manage.py migrate; \
    ${PYTHON_PATH}/bin/python3 manage.py makemigrations; \
    ${PYTHON_PATH}/bin/python3 manage.py migrate; \
    cd /data/webroot/BindUI; \
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_SUPERUSER_NAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | ${PYTHON_PATH}/bin/python3 ./manage.py shell; \
    systemctl enable bindui; \
    # Install JDK; \
    cd /usr/local/src; \
    #wget https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz; \
    wget https://download.oracle.com/java/17/archive/jdk-17.0.6_linux-x64_bin.tar.gz; \
    mkdir -p /usr/local/java; \
    tar -xvf jdk-17.0.6_linux-x64_bin.tar.gz -C /usr/local/java/; \  
    ln -s /usr/local/java/jdk-17.0.6 /usr/local/java/jdk; \
    # 设置JDK系统环境变量; \
    echo -e '\n\
## JAVA\n\
export JAVA_HOME=/usr/local/java/jdk\n\
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar\n\
\n\
## PATH\n\
export PATH=$PATH:$JAVA_HOME/bin\n\
'>> /etc/profile; \
    # Deploy url-forwarder; \
    cd /data/software/url-forwarder; \
    bash ./install.sh; \
    # Install BIND; \
    dnf -y install python3-ply perl-diagnostics epel-release diffutils; \
    dnf -y install libuv libuv-devel libnghttp2-devel libcap libcap-devel jemalloc jemalloc-devel --nobest; \
    dnf -y install bind-utils; \
    cd /usr/local/src/; \
    wget https://downloads.isc.org/isc/bind9/9.16.39/bind-9.16.39.tar.xz; \
    tar -Jxvf bind-9.16.39.tar.xz; \
    cd bind-9.16.39; \
    export LDFLAGS=-L/usr/lib64/mysql; \
    ./configure --prefix=/usr/local/bind_9.16.39 --with-dlz-mysql=yes --enable-epoll --enable-largefile; \
    make; \
    make install; \
    ln -s /usr/local/bind_9.16.39 /usr/local/bind; \
    ln -s /usr/local/bind/etc /etc/named; \
    groupadd -g 25 named; \
    useradd named -M -u 25 -g 25 -s /sbin/nologin; \
    mkdir -p /usr/local/bind/var; chown -R named:named /usr/local/bind/var; \
    mkdir -p /var/log/named /usr/local/bind/etc/conf.d; chown -R named.named /var/log/named; \
    systemctl enable named; \
    # Clear work; \
    rm -rf /usr/local/src/*; \
    yum -y remove gcc automake autoconf libtool make gcc gcc-c++; \
    yum clean all;

VOLUME ["/var/lib/mysql", "/var/log/named", "/data/logs/url-forwarder", "/var/log/django"]
EXPOSE 53/udp 53/tcp 953/tcp 80/tcp 8000/tcp 3306/tcp

ENTRYPOINT [ "/usr/sbin/init" ]
