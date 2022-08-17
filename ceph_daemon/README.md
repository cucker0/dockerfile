# ceph_daemon


## What's ceph_daemon image
Based on image `ceph/daemon`, fixed some shell scripts bug.

## Supported tags and respective `Dockerfile` links
* [`latest`](https://github.com/cucker0/dockerfile/blob/main/ceph_daemon/Dockerfile)

## How to use this image
[Reference ceph/daemon](https://hub.docker.com/r/ceph/daemon)



* For example

    * OSD_TYPE=directory

        First, in the host make the disk partion or vg/lv mount on `/ceph-rbd`

        ```
        docker run -d --privileged --restart=always --name osd \
         --net host \
         --pid=host \
         -v /etc/ceph:/etc/ceph \
         -v /var/lib/ceph:/var/lib/ceph \
         -v /dev/:/dev/ \
         -v /ceph-rbd:/var/lib/ceph/osd \
         -e OSD_TYPE=directory \
         cucker/ceph_daemon osd
        ```

    * OSD_TYPE=disk

        ```
        docker run -d --name osd \
         --restart=always \
         --net=host \
         --privileged=true \
         --pid=host \
         -v /etc/ceph:/etc/ceph \
         -v /var/lib/ceph/:/var/lib/ceph/ \
         -v /dev/:/dev/ \
         -v /run/udev/:/run/udev/ \
         -e OSD_DEVICE=/dev/sdb \
         -e OSD_TYPE=disk \
         -e OSD_BLUESTORE=1 \
         cucker/ceph_daemon osd
        ```

## Fixed bugs
* when OSD_TYPE=directory or ceph/daemon osd_directory, the OSD size max is 100GiB.

    there is a case like this. ref [ceph osd df size shows wrong, smaller number](https://lists.ceph.io/hyperkitty/list/ceph-users@ceph.io/thread/OAZLU6WBCN54NOBWSAGKH45BRV5GBI4Q/)
    ```bash
    docker run -d --privileged --restart=always --name osd \
     --net host \
     --pid=host \
     -v /etc/ceph:/etc/ceph \
     -v /var/lib/ceph:/var/lib/ceph \
     -v /dev/:/dev/ \
     -v /ceph-rbd:/var/lib/ceph/osd \
     -e OSD_TYPE=directory \
     ceph/daemon osd
    ```

    ```bash
    docker create --privileged --restart=always --name osd_04 \
     --net host \
     --pid=host \
     -v /etc/ceph:/etc/ceph \
     -v /var/lib/ceph:/var/lib/ceph \
     -v /dev/:/dev/ \
     -v /osd/sdc/:/var/lib/ceph/osd \
     -e OSD_TYPE=directory \
     ceph/daemon osd
    ```

* fixed `ceph-disk: command not found`
  
    `OSD_TYPE=disk` and `OSD_BLUESTORE=1`
    
    ```bash
    docker run --name osd \
     --restart=always \
     --net=host \
     --privileged=true \
     --pid=host \
     -v /etc/ceph:/etc/ceph \
     -v /var/lib/ceph/:/var/lib/ceph/ \
     -v /dev/:/dev/ \
     -v /run/udev/:/run/udev/ \
     -e OSD_DEVICE=/dev/sdb \
     -e OSD_TYPE=disk \
     -e OSD_BLUESTORE=1 \
     ceph/daemon osd
    ```
    
    
    
    ```
    /opt/ceph-container/bin/osd_disk_prepare.sh: line 46: ceph-disk: command not found
    ```
    
    use `ceph-volume` instead of `ceph-disk`
    
* fixed other BLUESTORE bugs



## Others

*   How to debug `ceph/daemon` 

    ```bash
    docker run -dit --privileged --restart=always --name osd_test \
     --net host \
     --pid=host \
     -v /etc/ceph:/etc/ceph \
     -v /var/lib/ceph:/var/lib/ceph \
     -v /dev/:/dev/ \
     -v /osd/sdc/:/var/lib/ceph/osd \
     -e OSD_TYPE=directory \
     --entrypoint /usr/bin/bash \
     ceph/daemon read
     
     // Enter container
     docker exec -it osd_test bash
    ```

    