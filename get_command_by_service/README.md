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
    ## create a service for httpd
    docker service creat --name web1 --health-cmd "curl --fail http://localhost:80/ || exit 1" cucker/httpd
    
    ## Command alias
    echo "alias get_command_service='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock cucker/get_command_by_service'" >> ~/.bashrc
    . ~/.bashrc
    
    ## Excute command
    get_command_service web1
    # Output results
    docker service creat --name web1 --health-cmd "curl --fail http://localhost:80/ || exit 1" cucker/httpd:latest
    ```
## Project
[get_command_by_service](https://github.com/cucker0/dockerfile/tree/main/get_command_by_service)