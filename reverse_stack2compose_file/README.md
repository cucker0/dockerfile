# stack2compose


## What's this
Reverse stack to compose file.


## Supported tags and respective `Dockerfile` links
* [`1.0`, `latest`](https://github.com/cucker0/dockerfile/blob/main/reverse_stack2compose_file/df/Dockerfile)

## How to use this image
```bash
Usage:
# Command alias
echo "alias stack2compose='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker cucker/stack2compose'" >> ~/.bashrc
. ~/.bashrc

# Excute command
## For all stacks
stack2compose {all}

## For one or more stacks
get_command_service <STACK> [STACK...]
```
<STACK> is `stack id` or `stack name`


* See help
    ```bash
    docker run --rm cucker/stack2compose --help
    
    # or
    docker run --rm cucker/stack2compose
    ```

* For example

    ```bash    

    ```
## Project
[get_command_by_service](https://github.com/cucker0/dockerfile/tree/main/reverse_stack2compose_file)