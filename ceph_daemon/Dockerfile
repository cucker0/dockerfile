# the "ceph/daemon:latest" DIGEST is 261bbe628f4b
FROM ceph/daemon:latest
LABEL maintainer='Image Maintainers <hanxiao2100@qq.com>'

COPY ./bin_scripts/* /opt/ceph-container/bin/
WORKDIR /
ENTRYPOINT ["/opt/ceph-container/bin/entrypoint.sh"]