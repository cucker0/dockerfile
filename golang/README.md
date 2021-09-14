# Golang with CentOS


## Soft environment
* golang
* glibc-2.28 with static

## Supported tags and respective `Dockerfile` links
* [`1.15.14_glibc-static`, `latest`, `centos 8`](https://github.com/cucker0/dockerfile/blob/main/golang/df/Dockerfile_2.0)
* [`1.17.1_glibc-static_v2`, `centos 8`](https://github.com/cucker0/dockerfile/blob/main/golang/df/Dockerfile_1.1)
* [`go1.17.1-glibc-static`, `centos 8`](https://github.com/cucker0/dockerfile/blob/main/golang/df/Dockerfile)

## How to use this image
```bash
docker run -e CGO_ENABLED=1 -e GOARCH=amd64 -e GOCACHE=/go \
  -u 0:0 \
  -v /usr/local/src/flannel/dist/qemu-amd64-static:/usr/bin/qemu-amd64-static \
  -v /usr/local/src/flannel:/go/src/github.com/flannel-io/flannel:ro \
  -v /usr/local/src/flannel/dist:/go/src/github.com/flannel-io/flannel/dist \
  golang:1.15.5 /bin/bash -c '\
  cd /go/src/github.com/flannel-io/flannel && \
  make -e dist/flanneld && \
  mv dist/flanneld dist/flanneld-amd64'
```