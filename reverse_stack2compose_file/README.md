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
    $ stack2compose mywp
    --- compose.yaml ---
    # docker stack deploy --compose-file ./compose.yaml mywp
    version: '3.9'
    services:
      db:
        image: mysql:latest
        environment:
          MYSQL_DATABASE: wordpress
          MYSQL_PASSWORD_FILE: /run/secrets/wordpress_db_password
          MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
          MYSQL_USER: wordpress
        volumes:
        - mywp_db_data:/var/lib/mysql
        networks:
        - mysql_private
        secrets:
        - db_root_password
        - wordpress_db_password
      wordpress:
        image: wordpress:latest
        environment:
          WORDPRESS_DB_HOST: db:3306
          WORDPRESS_DB_NAME: wordpress
          WORDPRESS_DB_PASSWORD_FILE: /run/secrets/wordpress_db_password
          WORDPRESS_DB_USER: wordpress
        volumes:
        - mywp_wordpress_data:/var/www/html
        networks:
        - mysql_private
        ports:
        - 5600:80
        secrets:
        - wordpress_db_password
    secrets:
      db_root_password:
        file: ./db_root_password.txt
      wordpress_db_password:
        file: ./wordpress_db_password.txt
    volumes:
      mywp_db_data: {}
      mywp_wordpress_data: {}
    networks:
      mysql_private: {} 
    ```
## Project
[get_command_by_service](https://github.com/cucker0/dockerfile/tree/main/reverse_stack2compose_file)