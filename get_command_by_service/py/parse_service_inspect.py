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

def camel2connector(s: str):
    """驼峰字符转连接字符格式。

    DriverOpts -> driver-opt

    :param s:
    :return:
    """
    if len(s) <= 1:
        return s.lower()

    s_list = list(s)
    for i in range(len(s_list)):
        if i != 0 and ('A' <= s_list[i] <= 'Z'):
            s_list[i] = s_list[i].lower()
            s_list.insert(i, '-')

    return "".join(s_list).lower()

def list_or_dict_to_ini(o, key: str):
    """list或dict对象转 initialization file 格式

    :return:
    """
    ini = ""
    if type(o) == list:
        if o :
            for i in o:
                ini += f"{camel2connector(key)}={i},"
            ini = ini[:-1]  # 去掉最后一个","
    elif type(o) == dict:
        ini = f"{camel2connector(key)}="
        for k in o:
            ini += f"{k}={o[k]}"

    return ini


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
        self.entity_info = {'type': None, 'name': None}  # Options: container, service, stack

    def _print_command(self):
        """

        Usage:  docker service create [OPTIONS] IMAGE [COMMAND] [ARG...]

        :return: str
            运行容器的完整命令
        """
        if self.entity_info['type'] == "stack":
            print(f"This is a docker stack: {self.entity_info['name']}.")
            return
        elif self.entity_info['type'] != "service":
            return

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
            command = f"docker service creat {options_key} {options} {self.image} {_args}"
        else:
            command = f"docker service creat {options_key} {options} {self.image}"
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
                self.entity_info['type'] = "stack"
                self.entity_info['name'] = self.inspect['Spec']['Labels']['com.docker.stack.namespace']
            else:
                self.entity_info['type'] = "service"

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
        if not self.entity_info['type']:
            self.check_entity_type()

        if self.entity_info['type'] != "service":
            return
        if not self.inspect:
            return

        # image
        self.image: str = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Image'].split('@')[0]
        if self.image.startswith('sha256:'):
            self.image = self.image.split(':')[1]

        # name of service
        self.options['kv'].append(
            {'--name': self.inspect['Spec']['Name']}
        )

        # parse options
        obj = PARSE_OPTIONS(self.inspect, self.options, self.args)
        for m in get_user_methods_by_class_(obj):
            try:
                m()
            except:
                pass

    def get_network_name_by_id(self, network_id: str):
        return self.api_client.inspect_network(network_id)['Name']


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
    dock = MYDOCKER()

    def __init__(self, inspect: dict, options: dict, args: list):
        self.inspect = inspect
        self.options = options
        self.args = args

    # --name
    # def name(self):
    #     self.options['kv'].append(
    #         {'--name': self.inspect['Spec']['Name']}
    #     )

    # --replicas, Number of tasks
    def replicas(self):
        if "Replicated" in list(self.inspect['Spec']['Mode'].keys()):
            if self.inspect['Spec']['Mode']['Replicated']['Replicas'] !=1:
                self.options['kv'].append(
                    {'--replicas': self.inspect['Spec']['Mode']['Replicated']['Replicas']}
                )

    # --mode, options: replicated, global, replicated-job, or global-job. replicated is the default.
    # --max-concurrent
    def mode(self):
        mode: list = list(self.inspect['Spec']['Mode'].keys())
        # global
        if "Global" in mode:
            self.options['kv'].append(
                {'--mode': 'global'}
            )

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
            self.options['kv'].append(
                {'--mode': 'replicated-job'}
            )
            # --max-concurrent
            if self.inspect['Spec']['Mode']['ReplicatedJob']['MaxConcurrent'] != 1:
                self.options['kv'].append({
                    '--max-concurrent': self.inspect['Spec']['Mode']['ReplicatedJob']['MaxConcurrent']
                })
            if self.inspect['Spec']['Mode']['ReplicatedJob']['TotalCompletions'] != 1:
                self.options['kv'].append(
                    {'--replicas': self.inspect['Spec']['Mode']['ReplicatedJob']['TotalCompletions']}
                )
        # global-job
        if "GlobalJob" in mode:
            self.options['kv'].append({
                '--mode': 'global-job'
            })

    # --publish, -p
    def publish(self):
        ports:list = self.inspect['Spec']['EndpointSpec']['Ports']
        if ports:
            for port in ports:
                if port['PublishMode'] == "ingress":
                    p = f"{port['PublishedPort']}:{port['TargetPort']}/{port['Protocol']}"
                else:
                    p = f"published={port['PublishedPort']},target={port['TargetPort']},protocol={port['Protocol']},mode=host"

                self.options['kv'].append(
                    {'--publish': p}
                )

    # --mount
    def mount(self):
        mounts:list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Mounts']
        for m in mounts:
            if "VolumeOptions" in list(m.keys()):
                v = f"type={m['Type']},volume-driver={m['VolumeOptions']['DriverConfig']['Name']},source={m['Source']},destination={m['Target']}"
            else:
                v = f"type={m['Type']},source={m['Source']},destination={m['Target']}"
            self.options['kv'].append(
                {'--mount': v}
            )

    # --network
    def network(self):
        networks: list = self.inspect['Spec']['TaskTemplate']['Networks']
        for net in networks:
            if len(net.keys()) == 1:
                v = PARSE_OPTIONS.dock.get_network_name_by_id(net['Target'])
            else:
                v = f"name={PARSE_OPTIONS.dock.get_network_name_by_id(net['Target'])}"
                for k in net:
                    if k == "Target":
                        continue
                    v += f",{list_or_dict_to_ini(net[k], k)}"

            self.options['kv'].append(
                {'--network': v}
            )

    # --env , -e
    # --env-file
    def environment(self):
        env: list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Env']
        for e in env:
            self.options['kv'].append(
                {'-e': e}
            )

    # --workdir, -w
    def workdir(self):
        dir: str = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Dir']
        if dir:
            self.options['kv'].append(
                {'--workdir': dir}
            )

    # --constraint
    def constraint(self):
        constraints = self.inspect['Spec']['TaskTemplate']['Placement']['Constraints']
        if not constraints:
            return

        for c in constraints:
            self.options['kv'].append(
                {'--constraint': c}
            )

    # --container-label

    # --health-cmd
    # --health-interval
    # --health-retries
    # --health-start-period
    # --health-timeout
    # --no-healthcheck
    def health_cmd(self):
        hc: dict = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Healthcheck']
        # --health-cmd
        try:
            if hc['Test'][0] == "CMD-SHELL":
                self.options['kv'].append(
                    {'--health-cmd': hc['Test'][1]}
                )
            # --no-healthcheck
            elif hc['Test'][0] == "NONE":
                self.options['kv'].append(
                    {'--no-healthcheck': ""}
                )
        except:
            pass

        # --health-interval
        try:
            if hc['Interval']:
                self.options['kv'].append(
                   {'--health-interval': f"{int(hc['Interval'] / 10**9)}s"}
                )
        except:
            pass

        # --health-retries
        try:
            if hc['Retries']:
                self.options['kv'].append(
                    {'--health-retries': hc['Retries']}
                )
        except:
            pass

        # --health-start-period
        try:
            if hc['StartPeriod']:
                self.options['kv'].append(
                    {'--health-start-period': f"{int(hc['StartPeriod'] / 10**9)}s"}
                )
        except:
            pass

        # --health-timeout
        if hc['Timeout']:
            self.options['kv'].append(
                {'--health-timeout': f"{int(hc['Timeout'] / 10**9)}s"}
            )

    # --secret
    def secret(self):
        secrets: list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Secrets']
        for sec in secrets:
            if sec['File']['UID'] == "0" and sec['File']['GID'] == "0" and sec['File']['Mode'] == 292:
                v = f"source={sec['SecretName']},target={sec['File']['Name']}"
            else:
                v = f"source={sec['SecretName']},target={sec['File']['Name']},uid={sec['File']['UID']}," \
                    f"gid={sec['File']['GID']},mode={sec['File']['Mode']}"

            self.options['kv'].append(
                {'--secret': v}
            )

    # --tty , -t
    def tty(self):
        tty = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['TTY']
        if tty:
            self.options['k'].append('t')

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

    # -quiet, -q

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



    # Args, docker service create command args
    def argument(self):
        li: list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Args']
        for arg in li:
            self.args.append(arg)

if __name__ == '__main__':
    if len(argv) < 2 or argv[1] == "--help":
        MYDOCKER.help_msg()
        exit(1)

    mydocker = MYDOCKER()
    ret = mydocker.start()