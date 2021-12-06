# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

"""
解析docker 容器的启动参数

require: python 3

author: Song yanlin
mail: hanxiao2100@qq.com
date: 2021-12-26
"""

import docker
from docker.errors import ImageNotFound, APIError

from sys import argv
import re, os


def unit_converter(size: int) -> str or int:
    """存储单位转换

    byte 转换 GB、MB、KB

    :param size:
    :return:
    """
    if size <= 0:
        return 0

    if (size >> 30) > 0:
        return f"{size >> 30}GB"
    elif (size >> 20) > 0:
        return f"{size >> 20}MB"
    elif (size >> 10) > 0:
        return f"{size >> 10}KB"
    else:
        return size

class MYDOCKER(object):
    def __init__(self):
        super(MYDOCKER, self).__init__()
        if not os.path.exists("/var/run/docker.sock"):
            self.help_msg()
            exit(1)
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

        # container name or container id. type is str
        self.service = argv[1]
        self.inspect:dict = {}
        self.docker_service_create = ""
        self.options = {"kv": [], "k": []}
        self.image = None  # str
        self.args = []
        self.inspect_image:dict = {}
        self.entityType = ""  # Options: container, service, stack

    def _print_command(self):
        """

        Usage:  docker service create [OPTIONS] IMAGE [COMMAND] [ARG...]

        :return: str
            运行容器的完整命令
        """
        print(self.inspect)

    def entity_type(self):
        """判断传入的实体类型

        :return:
        """
        if not self.inspect:
            return
        if 'Spec' in list(self.inspect.keys()):
            is_stack = False
            try:
                if self.inspect['Spec']['Labels']['com.docker.stack.namespace']:
                    is_stack = True
            except:
                pass
            if is_stack:
                self.entityType = "stack"
            else:
                self.entityType = "service"

    def _get_inspect(self):

        """get service inspect

        :return:
        """

        try:
            self.inspect = self.api_client.inspect_service(self.service)

        except APIError as e:
            print(e)
            exit(-1)

    def _get_inspect_image(self):
        if not self.inspect:
            self._get_inspect()

        # image
        image = self.inspect['Config']['Image']
        try:
            self.inspect_image = self.api_client.inspect_image(image)
        except Exception as e:
            print(e)

    def _parse_service_inspect(self):
        if not self.inspect:
            return
        if self.entityType != "self.entityType":
            return

        # image
        self.image: str = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Image'].split(':')[0]



    @staticmethod
    def help_msg():
        _MSG = """Usage:
# Command alias
echo "alias get_command_service='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock cucker/get_command_by_service'" >> ~/.bashrc
. ~/.bashrc

# Excute command
get_command_service <SERVICE>
"""
        print(_MSG)

    def start(self):
        pass

if __name__ == '__main__':
    if len(argv) < 2 or argv[1] == "--help":
        MYDOCKER.help_msg()
        exit(1)

    mydocker = MYDOCKER()
    ret = mydocker.start()
