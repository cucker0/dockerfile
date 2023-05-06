# dns


## What's this
Get the command for run container from a container.

include docker run options and arguments.

## Supported tags and respective `Dockerfile` links
* [`1.1`, `latest`](https://github.com/cucker0/dockerfile/blob/main/get_command_4_run_container/df/Dockerfile)
* [`1.0`](https://github.com/cucker0/dockerfile/blob/main/get_command_4_run_container/df/Dockerfile)

## How to use this image
```bash
Usage:
# Command alias
echo "alias get_run_command='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock cucker/get_command_4_run_container'" >> ~/.bashrc
. ~/.bashrc

# Excute command
get_run_command <CONTAINER>
```
<CONTAINER> is `container id` or `container name`


* See help
    ```bash
    docker run --rm cucker/get_command_4_run_container --help
    
    # or
    docker run --rm cucker/get_command_4_run_container
    ```

* For example

    ```bash
    ## run a container for mysql
    docker run -d --privileged --name dns --restart=always -p 80:80/tcp -p 8000:8000/tcp -p 3306:3306/tcp -p 53:53/udp cucker/dns:all-2.0
    docker run -dit --privileged --name dns --restart=always -p 80:80/tcp -p 8000:8000/tcp -p 3306:3306/tcp -p 53:53/udp --entrypoint /usr/sbin/init cucker/dns:all-2.0
    docker run -dit --privileged --name dns --restart=always -p 80:80/tcp -p 8000:8000/tcp -p 3306:3306/tcp -p 53:53/udp --entrypoint /usr/bin/bash cucker/dns:all-2.0 /usr/local/bin/docker-entrypoint.sh
    docker run -d --privileged --name dns --restart=always -p 80:80/tcp -p 8000:8000/tcp -p 3306:3306/tcp -p 53:53/udp --entrypoint /usr/sbin/init cucker/dns:all-2.0 & /usr/local/python3.11.3/bin/python3 /data/webroot/BindUI/manage.py runserver 0.0.0.0:8000
    
    ## Command alias
    echo "alias get_run_command='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock cucker/get_command_4_run_container'" >> ~/.bashrc
    . ~/.bashrc
    
    ## Excute command
    get_run_command mysql01
    # Output results
    docker run -d --name mysql01 --restart=always -p 13306:3306/tcp --env MYSQL_ROOT_PASSWORD=py123456 mysql
    ```
## Project
[get_command_4_run_container](https://github.com/cucker0/dockerfile/blob/main/get_command_4_run_container)

## docker build
```bash
cd <Dockerfile_root_path>
chmod +x  pkg/linux/docker-entrypoint.sh
docker build -f ./Dockerfile -t cucker/dns:all-2.0 .
// or
docker build --no-cache -f ./Dockerfile -t cucker/dns:all-2.0 .

docker build -f ./Dockerfile_2.1 -t cucker/dns:all-2.1 .
```