#!/bin/bash
# nginx install script
# author: song yanlin
# email: hanxiao2100@qq.com

# 软件包
# nginx-1.24.0.tar.gz luajit2-2.1-20230410.tar.gz openssl-3.1.0.tar.gz pcre2-10.42.tar.gz ngx_devel_kit-0.3.2.tar.gz lua-nginx-module-0.10.24.tar.gz ngx_healthcheck_module_1.19+.tar.gz ngx_dynamic_upstream-0.1.6.tar.gz init.d.nginx nginx_install.sh
# nginx: http://nginx.org/en/download.html
# LuaJIT: http://luajit.org
# luajit2: https://github.com/openresty/luajit2
# openssl: https://www.openssl.org/source
# pcre: http://www.pcre.org
# ngx_devel_kit: https://github.com/simplresty/ngx_devel_kit/releases
# lua-nginx-module: https://github.com/openresty/lua-nginx-module/tags
# ngx_healthcheck_module: https://github.com/zhouchangxun/ngx_healthcheck_module
# ngx_dynamic_upstream: https://github.com/cubicdaiya/ngx_dynamic_upstream/tags
# lua-resty-core: https://github.com/openresty/lua-resty-core/tags
# lua-resty-lrucache: https://github.com/openresty/lua-resty-lrucache/tags

# pcre 使用 nginx 集成的


# workdir path_exist_status
workdir=`pwd`

# 软件版本号
#NGINX_VERSION=`ls nginx-1.*.tar.gz |awk -F '-|.tar' '{print $2}' | head -n 1`
NGINX_VERSION="1.24.0"
OPENSSL_VERSION="3.1.0"
PCRE_VERSION="10.42"
LUAJIT_VERSION="2.1-20230410"
LUA_NGINX_MODULE_VERSION="0.10.24"
LUA_RESTY_CORE_VERSION="0.1.28"
LUA_RESTY_LRUCACHE="0.13"

function system_path_config() {
    # 系统环境变量配置与重载
    grep "^export PATH=" /etc/profile
    if [ $? != 0 ]; then # 不存在添加默认系统环境变量
        echo "## PATH" >> /etc/profile
        echo export PATH=$PATH >> /etc/profile
    fi
    . /etc/profile # 重启系统环境变量
}

function library_dynamic_config() {
    # ld.so动态链接库配置与重载
    cat <<ENDOF > /etc/ld.so.conf
include ld.so.conf.d/*.conf
/usr/local/lib
/usr/local/lib64
/lib
/lib64
/usr/lib
/usr/lib64

ENDOF

# 重载ld.so配置
ldconfig
}

function install_dependent_components() {
    # 安装依赖组件
    yum -y install zlib zlib-devel gd gd-devel perl
    yum -y install bind-utils traceroute wget man sudo ntp ntpdate screen patch make gcc gcc-c++ flex bison zip unzip ftp net-tools --skip-broken
    if [ $? != 0 ]; then
        echo "依赖组件安装有错!"
    fi
}

function rpm_install() {
    # rpm包安装器
    # $1: rpm包名
    if [ -n "$1" ]; then
        yum -y install $1
    else
        echo "没有传入rpm包名，使用方法：rpm_install 包名"
    fi
}

function check_dependent_components_install_status() {
    # 检查依赖组件安装是否成功
    rpm -qa |grep zlib-
    if [ $? != 0 ]; then
        rpm_install zlib
    fi
    rpm -qa |grep zlib-devel-
    if [ $? != 0 ]; then
        rpm_install zlib-devel
    fi
    rpm -qa |grep gd-
    if [ $? != 0 ]; then
        rpm_install gd
    fi
    rpm -qa |grep gd-devel-
    if [ $? != 0 ]; then
        rpm_install gd-devel
    fi
    rpm -qa |grep perl-
    if [ $? != 0 ]; then
        rpm_install perl
    fi

     install_dependent_components
}

function openssl_install() {
    # 安装openssl
    openssl version |grep ${OPENSSL_VERSION}
    if [ $? == 0 ]; then # opensll已经安装
        echo "OpenSSL ${OPENSSL_VERSION} already install"
        return
    fi
    
    yum -y install perl-FindBin perl-IPC-Cmd perl-File-Compare perl-File-Copy
    cd ${workdir}
    tar -zxvf openssl-${OPENSSL_VERSION}.tar.gz; cd openssl-${OPENSSL_VERSION}
    ./config --prefix=/usr/local/openssl_${OPENSSL_VERSION}; 
    make; 
    #make install
    #mv /usr/bin/openssl /usr/bin/openssl_1.0.1e-fips
    #ln -s /usr/local/ssl/bin/openssl /usr/bin/openssl
    cd ../

    ldconfig
    if [ $? != 0 ]; then
        echo "install openssl failed!"
        exit 1
    fi
}

function pcre_install() {
    # 安装pcre
    pcretest -C |grep ${PCRE_VERSION}
    if [ $? == 0 ]; then # pcre已经安装
        echo "pcre2-${PCRE_VERSION} already install"
        return
    fi

    cd ${workdir}
    tar -zxvf pcre2-${PCRE_VERSION}.tar.gz; cd pcre2-${PCRE_VERSION}
    ./configure --enable-jit; make; 
    #make install
    cd ../

    if [ $? != 0 ]; then
        echo "install pcre failed!"
        exit 1
    else
        echo "install pcre success."
    fi
    ldconfig
}

function lua_install() {
    # 安装Lua,nginx_lua_module模块依赖lua环境
    luajit -v |grep -i luajit
    if [ $? == 0 ]; then
        echo "LuaJIT 2 already install"
        return
    fi

    cd ${workdir}
    tar -zxvf luajit2-${LUAJIT_VERSION}.tar.gz
    cd luajit2-${LUAJIT_VERSION}
    #make PREFIX=/usr/local/luajit
    #make install PREFIX=/usr/local/luajit
    make; 
    make install
    cd ../

    ldconfig
    # 添加lua lib
    if [ ! $LUAJIT_LIB ]; then
        cat >> /etc/profile <<ENDOF
## Luajit
export LUAJIT_LIB=/usr/local/lib
export LUAJIT_INC=/usr/local/include/luajit-2.1
ENDOF

    fi
    source /etc/profile
}

function before_nginx_install() {
    # nginx安装前准备工作
    # 解压相关tar包
    cd ${workdir}
    tar -zxvf lua-nginx-module-${LUA_NGINX_MODULE_VERSION}.tar.gz
    tar -zxvf ngx_devel_kit-0.3.2.tar.gz
    tar -zxvf ngx_dynamic_upstream-0.1.6.tar.gz

    # 打上nginx_upstream_check_module 补丁
    tar -zxvf ngx_healthcheck_module_1.19+.tar.gz
    tar -zxvf nginx-${NGINX_VERSION}.tar.gz
    cd nginx-${NGINX_VERSION}
    patch -p1 < ${workdir}/ngx_healthcheck_module_1.19+/nginx_healthcheck_for_nginx_1.19+.patch

    # 创建nginx用户和组
    groupadd -g 901 nginx
    useradd nginx -M -u 901 -g 901 -s /sbin/nologin
}

function nginx_install() {
    # 编译安装nginx
    # 依赖步骤：library_dynamic_config、install_dependent_components、openssl_install、pcre_install、lua_install、before_nginx_install

    nginx -v |grep ${NGINX_VERSION}
    if [ $? == 0 ]; then # nginx已经安装
        echo "nginx-${NGINX_VERSION} already install."
        exit 0
    fi

    # nginx安装环境配置
    NGINX_INSTALL_PACKAGE_DECOMPRESSION_DIR=${workdir}/nginx-${NGINX_VERSION}
    if [ -d "${NGINX_INSTALL_PACKAGE_DECOMPRESSION_DIR}" ]; then
        echo "nginx package decompression directory is exist"
        cd ${NGINX_INSTALL_PACKAGE_DECOMPRESSION_DIR}
    else
        echo "nginx安装包未解压!"
        exit 1
    fi
    # Since nginx 1.21.5, Change: now nginx is built with the PCRE2 library by default. 
    # use --with-ld-opt='-lpcre'
    ./configure --prefix=/usr/local/nginx_${NGINX_VERSION} --user=nginx --group=nginx --with-http_stub_status_module --with-http_ssl_module --with-ld-opt='-lpcre' --with-http_realip_module --with-http_image_filter_module --with-http_gzip_static_module --with-openssl=${workdir}/openssl-3.1.0 --add-module=${workdir}/ngx_devel_kit-0.3.2 --add-module=${workdir}/lua-nginx-module-${LUA_NGINX_MODULE_VERSION} --add-module=${workdir}/ngx_healthcheck_module_1.19+ --add-module=${workdir}/ngx_dynamic_upstream-0.1.6 --with-stream --with-stream_ssl_module --with-http_v2_module
    
    if [ $? != 0 ]; then
        echo "configure nginx failed!"
        exit 1
    fi

    # 编译
    make;
    if [ $? != 0 ]; then
        echo "make nginx failed!"
        exit 1
    fi

    # 执行安装
    make install
    if [ $? != 0 ]; then
        echo "make install nginx failed!"
        exit 1
    else
        ln -s /usr/local/nginx_${NGINX_VERSION} /usr/local/nginx
    fi
    cd ../
}

function nginx_system_path_config() {
    # 添加nginx环境变量
    . /etc/profile
    echo ${PATH} |grep "/usr/local/nginx/sbin"
    if [ $? == 0 ]; then
        echo "nginx path is exist"
    else
        sed -i 's/^export PATH=.*$/&:\/usr\/local\/nginx\/sbin/g' /etc/profile
    fi
    . /etc/profile
}

function after_nginx_install() {
    # nginx安装后设置
    if [ ! -d "/etc/nginx" ]; then
        cp -a /usr/local/nginx_${NGINX_VERSION}/conf /etc/nginx
        mkdir /etc/nginx/conf.d
    fi

    mv /usr/local/nginx_${NGINX_VERSION}/conf /usr/local/nginx_${NGINX_VERSION}/conf_yl
    ln -s /etc/nginx /usr/local/nginx_${NGINX_VERSION}/conf  

}

function nginx_auto_start_script() {
    # 设置nignx自动启动脚本
    ## CentOS 6
    uname -r| grep '^2.6.'
    if [ $? == 0 ]; then
        \cp -f init.d.nginx /etc/init.d/nginx
        chmod +x /etc/init.d/nginx
        chkconfig nginx on #　开启自动启动

        ldconfig
        sleep 1
        service nginx start
    else
        cat <<ENDOF > /usr/lib/systemd/system/nginx.service
[Unit]
Description=nginx - high performance web server
Documentation=http://nginx.org/en/docs/
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/usr/local/nginx/logs/nginx.pid
ExecStartPre=/usr/local/nginx/sbin/nginx -t -c /etc/nginx/nginx.conf
ExecStart=/usr/local/nginx/sbin/nginx -c /etc/nginx/nginx.conf
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s QUIT \$MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
ENDOF
        systemctl daemon-reload
        systemctl enable nginx
        ldconfig
        sleep 1
        systemctl start nginx.service
    fi

}

function check_nginx_is_ok() {
    # 检查nginx安装正常
    ldconfig
    . /etc/profile
    nginx -t
    if [ $? == 0 ]; then
        echo "nginx install success."
    else
        echo "nginx install failed!"
    fi
}

# fix that `nginx: [alert] failed to load the 'resty.core' module` 
fix_lua_resty_core() {
    cd ${workdir}
    tar -zxvf lua-resty-core-${LUA_RESTY_CORE_VERSION}.tar.gz
    cd lua-resty-core-${LUA_RESTY_CORE_VERSION}
    # Why LUA_LIB_DIR is `/usr/local/share/lua/5.1`, because nginx load default LUA_LIB_DIR is `/usr/local/share/lua/5.1`.
    # Reference https://github.com/openresty/lua-resty-core?tab=readme-ov-file#installation
    make install LUA_LIB_DIR=/usr/local/share/lua/5.1
    
    # fix that `reason: /usr/local/share/lua/5.1/resty/core/regex.lua:14: module 'resty.lrucache' not found`
    cd ${workdir}
    tar -zxvf lua-resty-lrucache-${LUA_RESTY_LRUCACHE}.tar.gz
    cd lua-resty-lrucache-${LUA_RESTY_LRUCACHE}
    make install LUA_LIB_DIR=/usr/local/share/lua/5.1
}

function main() {
    # 入口函数
    echo "begin install nginx..."
    # 依赖的步骤顺序要正确
    system_path_config
    library_dynamic_config
    install_dependent_components
    check_dependent_components_install_status
    openssl_install
    #pcre_install
    lua_install
    fix_lua_resty_core
    before_nginx_install
    nginx_install
    nginx_system_path_config
    after_nginx_install
    nginx_auto_start_script
    check_nginx_is_ok
}

main
