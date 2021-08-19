FROM centos:8
LABEL maintainer="NGINX Docker Maintainers <hanxiao2100@qq.com>"
RUN yum install -y nginx
RUN yum install -y curl telnet net-tools
RUN echo "Nginx Web: docker test." > /usr/share/nginx/html/index.html
EXPOSE 80
ENTRYPOINT ["/usr/sbin/nginx"]
CMD ["-g", "daemon off;"]