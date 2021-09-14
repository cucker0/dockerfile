FROM centos:8
LABEL maintainer='Golang Image Maintainers <hanxiao2100@qq.com>'
ENV SRC=/usr/local/src
ENV GO_VERSION=go1.17.1.linux-amd64
ENV PATH $PATH:/usr/local/go/bin
RUN yum -y update glibc glibc-devel glibc-headers glibc-common
RUN yum -y install automake autoconf libtool make gcc gcc-c++ glibc glibc-devel git wget bison
RUN yum clean all
ADD https://golang.google.cn/dl/${GO_VERSION}.tar.gz ${SRC}
RUN cd $SRC; \
    rm -rf /usr/local/go; \
    tar -C /usr/local -xzf ${GO_VERSION}.tar.gz; \
    rm -rf ${GO_VERSION}.tar.gz
    
ENV GLIBC_VERSION=glibc-2.28
ENV GLIBC_SRC=${SRC}/${GLIBC_VERSION}
# glibc-static
RUN mkdir -p ${GLIBC_SRC}; \
    cd ${GLIBC_SRC}; \
    wget https://ftp.gnu.org/pub/gnu/glibc/${GLIBC_VERSION}.tar.gz; \
    tar -xf ${GLIBC_VERSION}.tar.gz; \
    ./glibc-2.28/configure --prefix=/usr/local/glibc; \
    make -j2; \
    cp libc.a libc_pic.a ./nptl/libpthread.a ./dlfcn/libdl.a /usr/lib64
CMD [ "bash" ]
