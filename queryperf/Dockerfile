## queryperf
# copy the queryperf to the host 

FROM alpine:3.18
LABEL maintainer='Image Maintainers <hanxiao2100@qq.com>'
COPY pkg/queryperf /usr/bin/

RUN chmod +x /usr/bin/queryperf

VOLUME ["/pkg"]
CMD ["cp", "/usr/bin/queryperf", "/pkg/"]
