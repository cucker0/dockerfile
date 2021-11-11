# get_container_run_command


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
    docker run -d --name mysql01 --restart=always -p 13306:3306/tcp --env MYSQL_ROOT_PASSWORD=py123456 mysql
    
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