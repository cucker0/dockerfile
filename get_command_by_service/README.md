# get_command_by_service


## What's this
Get the command for `docker service create` from a service.

include service create options and arguments.

## Supported tags and respective `Dockerfile` links
* [`1.0`, `latest`](https://github.com/cucker0/dockerfile/blob/main/get_command_by_service/df/Dockerfile)

## How to use this image
```bash
Usage:
# Command alias
echo "alias get_command_service='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock cucker/get_command_by_service'" >> ~/.bashrc
. ~/.bashrc

# Excute command
## For all services
get_command_service {all}

## For one or more services
get_command_service <SERVICE> [SERVICE...]
```
<SERVICE> is `service id` or `service name`


* See help
    ```bash
    docker run --rm cucker/get_command_by_service --help
    
    # or
    docker run --rm cucker/get_command_by_service
    ```

* For example

    ```bash    
    ## Command alias
    echo "alias get_command_service='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock cucker/get_command_by_service'" >> ~/.bashrc
    . ~/.bashrc
    
    ## Excute command
    $ get_command_service {all}
    === service: too-big2 ===
    docker service creat --name too-big2 --reserve-memory 4GB nginx:alpine
    
    === service: my_web10 ===
    docker service creat --name my_web10 \
     --constraint node.labels.env==prod \
     --publish 6000:80/tcp \
     --replicas 3 \
     httpd:latest

    === service: wordpress_mysql ===
    docker service creat --name wordpress_mysql \
     --env MYSQL_ROOT_PASSWORD_FILE=/run/secrets/mysql_root_password \
     --env MYSQL_PASSWORD_FILE=/run/secrets/workpress_password \
     --env MYSQL_USER=wordpress \
     --env MYSQL_DATABASE=wordpress \
     --network mysql_private \
     --secret source=mysql_root_password,target=mysql_root_password \
     --secret source=workpress_db_password,target=workpress_password \
     mysql:latest

    ```
## Project
[get_command_by_service](https://github.com/cucker0/dockerfile/tree/main/get_command_by_service)