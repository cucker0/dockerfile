FROM centos:8
LABEL maintainer='Web Stress Testing Image Maintainers <hanxiao2100@qq.com>'
ENV SRC=/usr/local/src
ENV PATH=$PATH:/usr/local/siege/bin
RUN yum -y install bind-utils httpd openssl openssl-devel
RUN yum -y install gcc automake autoconf libtool make gcc gcc-c++
ADD http://download.joedog.org/siege/siege-4.1.1.tar.gz $SRC
RUN cd $SRC; \
    tar -zxf siege-4.1.1.tar.gz; \
    cd siege-4.1.1; \
    ./configure --prefix=/usr/local/siege --with-ssl=/usr/include/openssl; \
    make; make install
RUN rm -rf $SRC/siege-4.1.1.tar.gz
CMD [ "bash" ]
