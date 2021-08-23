FROM centos:8
LABEL maintainer="hanxiao<hanxiao2100@qq.com>" \
    environment="JDK 16, Tomcat 10"

# 从宿主机复制jdk、tomcat包到镜像中，并自动解压tar压缩包
ADD jdk-16.0.1_linux-x64_bin.tar.gz /usr/local/
ADD apache-tomcat-10.0.6.tar.gz /usr/local/
RUN ln -s /usr/local/jdk-16.0.1 /usr/local/jdk; \
        ln -s /usr/local/apache-tomcat-10.0.6 /usr/local/tomcat;

# 设置java、tomcat环境变量
ENV JAVA_HOME /usr/local/jdk
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV CATALINA_HOME /usr/local/tomcat
ENV CATALINA_BASE $CATALINA_HOME
ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/bin:$CATALINA_HOME/lib

# 设置工作目录
WORKDIR $CATALINA_HOME

# 暴露的端口
EXPOSE 8080/tcp

# 容器启动时执行的命令
CMD ["catalina.sh", "run"]

