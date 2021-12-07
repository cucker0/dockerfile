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

def get_user_methods_by_class_(cls) ->list:
    """获取指定类的用户自定义方法

    :param cls: class
        类实例
    :return: list
       用户定义的方法名列表.
       返回的list元素为方法(fundtion)，而非str型的方法名，是可以调用的方法对象。
    """
    methds = []
    for method in dir(cls):
        if method.startswith('__'):
            continue
        if method.endswith('__'):
            continue
        if callable(getattr(cls, method)):
            methds.append(getattr(cls, method))

    return methds

class MYDOCKER(object):
    def __init__(self):
        super(MYDOCKER, self).__init__()
        if not os.path.exists("/var/run/docker.sock"):
            self.help_msg()
            exit(1)
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

        # service name or container id. type is str
        self.service = argv[1]
        self.inspect:dict = {}
        self.docker_service_create = ""
        self.options = {"kv": [], "k": []}
        self.image = None  # str
        self.args = []
        self.entityType = ""  # Options: container, service, stack

    def _print_command(self):
        """

        Usage:  docker service create [OPTIONS] IMAGE [COMMAND] [ARG...]

        :return: str
            运行容器的完整命令
        """
        if not self.inspect:
            return

        options_key = ""
        if self.options['k']:
            options_key = "-"
        #  key 型options
        for k in self.options['k']:
            options_key += k

        # key-value 型options
        options_kv = ""
        for kv in self.options['kv']:
            _k = list(kv.keys())[0]
            if _k.endswith('='):
                options_kv += f"{_k}{kv[_k]} "
            else:
                options_kv += f"{_k} {kv[_k]} "

        options = f"{options_key} {options_kv}".strip()

        command = ""
        if self.args:
            _args = ""
            for i in self.args:
                _args += f"{i} "
            _args = _args.strip()
            command = f"docker service creat {options} {self.image} {_args}"
        else:
            command = f"docker service creat {options} {self.image}"
        print(command)


    def check_entity_type(self):
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

    def _parse_service_inspect(self):
        if not self.entityType:
            self.check_entity_type()

        if self.entityType != "service":
            return
        if not self.inspect:
            return

        # image
        self.image: str = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Image'].split(':')[0]

        # parse options
        obj = PARSE_OPTIONS(self.inspect, self.options)
        for m in get_user_methods_by_class_(obj):
            try:
                m()
            except:
                pass

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
        self._get_inspect()
        self._parse_service_inspect()
        self._print_command()

class PARSE_OPTIONS(object):
    """从service inspect信息中解析docker service create命令的options

    """

    def __init__(self, inspect: dict, options: dict):
        self.inspect = inspect
        self.options = options

    ## --name
    def name(self):
        self.options['kv'].append({
            '--name': self.inspect['Spec']['Name']
        })

    ## --replicas, Number of tasks
    def replicas(self):
        if "Replicated" in list(self.inspect['Spec']['Mode'].keys()):
            self.options['kv'].append({
                '--replicas', self.inspect['Spec']['Mode']['Replicated']['Replicas']
            })

    # --mode, options: replicated, global, replicated-job, or global-job. replicated is the default.
    def mode(self):
        mode: list = list(self.inspect['Spec']['Mode'].keys())
        # global
        if "Global" in mode:
            self.options['kv'].append({
                '--mode': 'global'
            })

        # replicated-job
        """
            "Mode": {
                "ReplicatedJob": {
                    "MaxConcurrent": 2,
                    "TotalCompletions": 10
                }
            },
        """
        if "ReplicatedJob" in mode:
            self.options['kv'].append({
                '--mode': 'replicated-job'
            })
            # --max-concurrent
            if self.inspect['Spec']['Mode']['ReplicatedJob']['MaxConcurrent'] > 1:
                self.options['kv'].append({
                    '--max-concurrent': self.inspect['Spec']['Mode']['ReplicatedJob']['MaxConcurrent']
                })
            if self.inspect['Spec']['Mode']['ReplicatedJob']['TotalCompletions'] > 1:
                self.options['kv'].append({
                    '--replicas': self.inspect['Spec']['Mode']['ReplicatedJob']['TotalCompletions']
                })
        # global-job
        if "GlobalJob" in mode:
            self.options['kv'].append({
                '--mode': 'global-job'
            })

    # --publish, -p

    # --mount

    # --network

    # --env , -e

    # --env-file

    # --workdir, -w

    # --constraint

    # --container-label

    # --health-cmd

    # --health-interval

    # --health-retries

    # --health-start-period

    # --health-timeout

    # --no-healthcheck

    # --secret

    # --tty , -t

    # --cap-add

    # --cap-drop

    # --config

    # --detach , -d

    # --dns

    # --dns-option

    # --dns-option

    # --dns-search

    # --endpoint-mode, default is vip (vip or dnsrr)

    # --entrypoint

    # --generic-resource

    # --group

    # --host

    # --hostname

    # --init

    # --isolation

    # --label , -l

    # --limit-cpu

    # --limit-memory

    # --limit-pids, Limit maximum number of processes (default 0 = unlimited)

    # --log-driver

    # --log-opt



    # --no-resolve-image

    # --placement-pref

    # -quiet , -q

    # --read-only

    # --replicas-max-per-node, Maximum number of tasks per node (default 0 = unlimited)

    # --reserve-cpu

    # --reserve-memory

    # --restart-condition, Restart when condition is met ("none"|"on-failure"|"any") (default "any")

    # --restart-delay, Delay between restart attempts (ns|us|ms|s|m|h) (default 5s)

    # --restart-max-attempts, Maximum number of restarts before giving up

    # --rollback-delay, Delay between task rollbacks (ns|us|ms|s|m|h) (default 0s)

    # --rollback-failure-action, Action on rollback failure ("pause"|"continue") (default "pause")

    # --rollback-max-failure-ratio

    # --rollback-monitor, Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h) (default 5s)

    # --rollback-order, Rollback order ("start-first"|"stop-first") (default "stop-first")

    # --rollback-parallelism, Maximum number of tasks rolled back simultaneously (0 to roll back all at once), The default value is 1

    # --stop-grace-period

    # --stop-signal

    # --sysctl

    # --ulimit

    # --update-delay

    # --update-failure-action, Action on update failure ("pause"|"continue"|"rollback") (default "pause")

    # --update-max-failure-ratio, Failure rate to tolerate during an update (default 0)

    # --update-order, Update order ("start-first"|"stop-first") (default "stop-first")

    # --update-order, Update order ("start-first"|"stop-first") (default "stop-first")

    # -user, -u, Username or UID (format: <name|uid>[:<group|gid>])

    # --with-registry-auth


if __name__ == '__main__':
    if len(argv) < 2 or argv[1] == "--help":
        MYDOCKER.help_msg()
        exit(1)

    mydocker = MYDOCKER()
    ret = mydocker.start()
