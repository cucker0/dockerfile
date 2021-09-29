# weave

## What's this
From weaveworks/weave image,  switch iptables-legacy to nf_tables.

To adapt to CentOS 8. Because centos 8 iptables (v1.8.4) just support nf_tables.

## Supported tags and respective `Dockerfile` links
* [`weave 2.8.1`, `latest`](https://github.com/cucker0/dockerfile/blob/main/weave//Dockerfile_2.8.1)

## How to use this image
1. First setp.

    ```bash
    curl -L git.io/weave -o /usr/local/bin/weave
    chmod a+x /usr/local/bin/weave

    export weaver_version=`weave version |tail -n 1 |awk '{print $2}'`
    docker pull cucker/weave:${weaver_version}
    docker tag cucker/weave:${weaver_version} weaveworks/weave:${weaver_version}
    ```

2.  launch weave
Then launch weave as normally as usual.