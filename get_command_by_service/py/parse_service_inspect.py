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

import os
from sys import argv

import docker
from docker.errors import APIError


def unit_converter(size: int) -> str or int:
    """存储单位转换

    byte 转换 GB、MB、KB

    :param size: 字节数
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
    ss = "".join(s_list).lower()
    if ss.endswith("s"):
        ss = ss[:-1]

    return ss

def file_mode_converter(num: int):
    """

    十进制mode 转 user:group:other mode
    0444  <-->  292
    444 --> 100 100 100(2) --> 292(10)

    :param num: 十进制数字
    :return: ser:group:other mode
        格式：0ugo
    """

    # 数字转二进制字符串
    user = (num & 0b111000000) >> 6
    group = (num & 0b111000) >> 3
    other = num & 0b111
    return f"0{user}{group}{other}"

def list_or_dict_to_ini(o, key: str):
    """list或dict对象转 initialization file 格式

    :return:
    """
    ini = ""
    try:
        if type(o) == list:
            if o :
                for i in o:
                    ini += f"{camel2connector(key)}={i},"
        elif type(o) == dict:
            for k in o:
                ini += f"{camel2connector(key)}={k}={o[k]},"
        # 去掉最后一个","
        if ini and ini.endswith(","):
            ini = ini[:-1]
    except:
        pass

    return ini


class MYDOCKER(object):
    def __init__(self, service=None):
        super(MYDOCKER, self).__init__()
        if not os.path.exists("/var/run/docker.sock"):
            self.help_msg()
            exit(1)
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

        # service name or service id. type is str
        self.service = service
        self.inspect:dict = {}
        self.docker_service_create = ""
        self.options = {"kv": [], "k": []}
        self.image = None  # str
        self.args = []
        self.entity_info = {'type': None, 'name': None}  # Options: container, service, stack

    def get_services(self) -> list:
        return self.api_client.services()

    def _print_command(self):
        """

        Usage:  docker service create [OPTIONS] IMAGE [COMMAND] [ARG...]

        :return: str
            运行容器的完整命令
        """
        if self.entity_info['type'] == "stack":
            print(f"This is a docker stack: {self.entity_info['name']}.")
            print("Reverse stack to a compose file reference `https://hub.docker.com/repository/docker/cucker/stack2compose`")
            print("docker service create command: ")

        if not self.inspect:
            return

        options_key = ""
        # if self.options['k']:
        #     options_key = "-"

        #  key 型options
        for k in self.options['k']:
            options_key += f"{k} "
        options_key = options_key.strip(" ")

        # key-value 型options
        options_kv = ""
        is_pretty = len(self.options['kv']) > 2
        if is_pretty:
            for dic in self.options['kv']:
                _k = list(dic.keys())[0]
                if _k.endswith('='):
                    options_kv += f" {_k}{dic[_k]} \\\n"
                else:
                    options_kv += f" {_k} {dic[_k]} \\\n"
            if options_key:
                options = f"{options_key} \\\n {options_kv}".lstrip(" ")
            else:
                options = f"{options_kv}".lstrip(" ")
        else:
            for dic in self.options['kv']:
                _k = list(dic.keys())[0]
                if _k.endswith('='):
                    options_kv += f"{_k}{dic[_k]} "
                else:
                    options_kv += f"{_k} {dic[_k]} "

            options = f"{options_key} {options_kv}".strip()

        command = ""
        if self.args:
            # _args = " ".join(self.args[0])
            _args = ""
            for i in self.args[0]:
                # sh -c “xxx” 命令中，-c 后的子命令需要引号包裹的情况
                if i.__contains__(' "'):
                    i = f"'{i}'"
                elif i.__contains__(" '"):
                    i = f'"{i}"'
                elif i.__contains__(" "):
                    i = f'"{i}"'
                _args += f"{i} "

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

        # if self.entity_info['type'] != "service":
        #     return
        if not self.inspect:
            return

        # image
        self.image: str = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Image'].split('@')[0]
        if self.image.startswith('sha256:'):
            self.image = self.image.split(':')[1]

        # # name of service
        # self.options['kv'].append(
        #     {'--name': self.inspect['Spec']['Name']}
        # )

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
## For all services
get_command_service {all}

## For one or more services
get_command_service <SERVICE> [SERVICE...]
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
    # 方法名前缀为_，可以在dir(类型) 时排前
    def _name(self):
        self.options['kv'].append(
            {'--name': self.inspect['Spec']['Name']}
        )

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
                    if port['Protocol'] == "tcp":
                        p = f"{port['PublishedPort']}:{port['TargetPort']}"
                    else:
                        p = f"{port['PublishedPort']}:{port['TargetPort']}/{port['Protocol']}"
                else:
                    p = f"published={port['PublishedPort']},target={port['TargetPort']},protocol={port['Protocol']},mode=host"

                self.options['kv'].append(
                    {'--publish': p}
                )

    # --mount
    def mount(self):
        mounts: list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Mounts']
        for m in mounts:
            try:
                readonly = ""
                keys_m = list(m.keys())
                if "ReadOnly" in keys_m:
                    if m['ReadOnly']:
                        readonly = f",readonly=true"
                    else:
                        readonly = f",readonly=false"
                v = ""
                if "VolumeOptions" in keys_m:
                    if "DriverConfig" in list(m['VolumeOptions'].keys()) and m['VolumeOptions']['DriverConfig']:
                        v = f"type={m['Type']}{readonly},volume-driver={m['VolumeOptions']['DriverConfig']['Name']},source={m['Source']},destination={m['Target']}"
                    elif "Labels" in list(m['VolumeOptions'].keys()):
                        labels: dict = m['VolumeOptions']['Labels']
                        lab = ""
                        for _k in labels:
                            lab += f'volume-label="{_k}={labels[_k]}",'
                        if lab.endswith(","):
                            lab = lab[:-1]
                        v = f"type={m['Type']}{readonly},source={m['Source']},destination={m['Target']},{lab}"
                else:
                    v = f"type={m['Type']}{readonly},source={m['Source']},destination={m['Target']}"

                if v:
                    self.options['kv'].append(
                        {'--mount': v}
                    )
            except:
                pass

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
                {'--env': e}
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
    def container_label(self):
        labels: dict = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Labels']
        for k in labels:
            self.options['kv'].append(
                {'--container-label': f"{k}={labels[k]}"}
            )

    # --health-cmd
    # --health-interval
    # --health-retries
    # --health-start-period
    # --health-timeout
    # --no-healthcheck
    def health_check(self):
        hc: dict = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Healthcheck']
        # --health-cmd
        try:
            if hc['Test'][0] == "CMD-SHELL":
                self.options['kv'].append(
                    {'--health-cmd': f'"{hc["Test"][1]}"'}
                )
            # --no-healthcheck
            elif hc['Test'][0] == "NONE":
                self.options['k'].append("--no-healthcheck")
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
            v = ""
            if sec['File']['UID'] == "0" and sec['File']['GID'] == "0":
                if sec['File']['Mode'] == 292:
                    v = f"source={sec['SecretName']},target={sec['File']['Name']}"
                else:
                    v = f"source={sec['SecretName']},target={sec['File']['Name']},mode={file_mode_converter(sec['File']['Mode'])}"
            else:
                if sec['File']['Mode'] == 292:
                    v = f"source={sec['SecretName']},target={sec['File']['Name']},uid={sec['File']['UID']}," \
                        f"gid={sec['File']['GID']}"
                else:
                    v = f"source={sec['SecretName']},target={sec['File']['Name']},uid={sec['File']['UID']}," \
                        f"gid={sec['File']['GID']},mode={file_mode_converter(sec['File']['Mode'])}"

            self.options['kv'].append(
                {'--secret': v}
            )

    # --tty , -t
    def tty(self):
        tty = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['TTY']
        if tty:
            self.options['k'].append('-t')

    # --cap-add
    def cap_add(self):
        caps: list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['CapabilityAdd']
        for cap in caps:
            self.options['kv'].append(
                {'--cap-add': cap}
            )

    # --cap-drop
    def cap_drop(self):
        caps = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['CapabilityDrop']
        for cap in caps:
            self.options['kv'].append(
                {'--cap-drop': cap}
            )

    # --config
    def config(self):
        cs: list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Configs']
        for c in cs:
            v = ""
            if c['File']['UID'] == "0" and c['File']['GID'] == "0":
                if c['File']['Mode'] == 292:  # 292  --> mode=0444
                    if c['ConfigName'] == c['ConfigName']['File']['Name']:
                        v = c['ConfigName']
                    else:
                        v = f"source={c['ConfigName']},target={c['File']['Name']}"
                else:
                    v = f"source={c['ConfigName']},target={c['File']['Name']},mode={file_mode_converter(c['File']['Mode'])}"
                    print(v)
            else:
                if c['File']['Mode'] == 292:
                    v = f"source={c['ConfigName']},target={c['File']['Name']},uid={c['File']['UID']},gid={c['File']['GID']}"
                else:
                    v = f"source={c['ConfigName']},target={c['File']['Name']},uid={c['File']['UID']}," \
                        f"gid={c['File']['GID']},mode={file_mode_converter(c['File']['Mode'])}"

            self.options['kv'].append(
                {'--config': v}
            )

    # --detach , -d

    # --dns
    # --dns-option
    # --dns-search
    def dns_config(self):
        dnsconfig: dict = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['DNSConfig']
        if not dnsconfig:
            return

        keys = list(dnsconfig.keys())
        ## --dns
        if "Nameservers" in keys:
            for ns in dnsconfig['Nameservers']:
                self.options['kv'].append(
                    {'--dns': f'"{ns}"'}
                )
        ## --dns-search
        if "Search" in keys:
            for s in dnsconfig['Search']:
                self.options['kv'].append(
                    {'--dns-search': s}
                )

        ## --dns-option
        if "Options" in keys:
            for op in dnsconfig['Options']:
                self.options['kv'].append(
                    {'--dns-option': op}
                )


    # --endpoint-mode, default is vip (vip or dnsrr)
    def endpoint_mode(self):
        if self.inspect['Spec']['EndpointSpec']['Mode'] != "vip":
            self.options['kv'].append(
                {'--endpoint-mode': self.inspect['Spec']['EndpointSpec']['Mode']}
            )


    # --entrypoint
    def entrypoint(self):
        containerSpec: dict = self.inspect['Spec']['TaskTemplate']['ContainerSpec']
        if "Command" in list(containerSpec.keys()):
            c = ""
            for i in containerSpec['Command']:
                c += f"{i} "
            if c:
                c = c[:-1]
            self.options['kv'].append(
                {'--entrypoint': f'"{c}"'}
            )

    # --generic-resource
    def generic_resource(self):
        grs: list = self.inspect['Spec']['TaskTemplate']['Resources']['Reservations']['GenericResources']
        for gr in grs:
            self.options['kv'].append(
                {'--generic-resource': f'"{gr["DiscreteResourceSpec"]["Kind"]}={gr["DiscreteResourceSpec"]["Value"]}"'}
            )

    # --group, 该用户组，要在主机中存在.
    def group(self):
        gs: list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Groups']
        for g in gs:
            self.options['kv'].append(
                {'--group': g}
            )

    # --host, Set one or more custom host-to-IP mappings (host:ip)
    def host(self):
        hosts = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Hosts']
        for h in hosts:
            h_split = h.split(" ")
            self.options['kv'].append(
                {'--host': f"{h_split[1]}:{h_split[0]}"}
            )

    # --hostname
    def hostname(self):
        if "Hostname" not in list(self.inspect['Spec']['TaskTemplate']['ContainerSpec'].keys()):
            return
        self.options['kv'].append(
            {'--hostname': self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Hostname']}
        )


    # --init, Use an init inside each service container to forward signals and reap processes
    def init(self):
        if self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Init']:
            self.options['k'].append("--init")

    # --isolation
    def isolation(self):
        if self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Isolation'] != "default":
            self.options['kv'].append(
                {'--isolation': self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Isolation']}
            )

    # --label , -l
    def label(self):
        labels = self.inspect['Spec']['Labels']
        if labels:
            for k in labels:
                self.options['kv'].append(
                    {'--label': f"{k}={labels[k]}"}
                )

    # --limit-cpu
    # --limit-memory
    # --limit-pids, Limit maximum number of processes (default 0 = unlimited)
    def resources_limits(self):
        rl: dict = self.inspect['Spec']['TaskTemplate']['Resources']['Limits']
        ## --limit-memory
        keys = list(rl.keys())
        if "MemoryBytes" in keys:
            self.options['kv'].append(
                {'--limit-memory': unit_converter(rl['MemoryBytes'])}
            )
        ## --limit-cpu
        if "NanoCPUs" in keys:
            self.options['kv'].append(
                {'--limit-cpu': rl['NanoCPUs'] / 10**9}
            )
        ## --limit-pids
        if "Pids" in keys:
            self.options['kv'].append(
                {'--limit-pids': rl['Pids']}
            )

    # --log-driver
    # --log-opt
    def log_driver(self):
        logdriver: dict = self.inspect['Spec']['TaskTemplate']['LogDriver']
        ## --log-driver
        if "Name" in list(logdriver.keys()):
            self.options['kv'].append(
                {'--log-driver': logdriver['Name']}
            )
        ## --log-opt
        if "Options" in list(logdriver.keys()):
            for k in logdriver['Options']:
                self.options['kv'].append(
                    {'--log-opt': f"{k}={logdriver['Options'][k]}"}
                )

    # --no-resolve-image
    def no_resolve_image(self):
        image = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Image']
        if not image.__contains__("sha256:"):
            self.options['k'].append("--no-resolve-image")


    # --placement-pref
    def placement_pref(self):
        preferences: list = self.inspect['Spec']['TaskTemplate']['Placement']['Preferences']

        for p in preferences:
            v = ""
            for k in p:
                # p[k] 的第一个kv对应的key
                pk = list(p[k].keys())[0]
                v += f"{camel2connector(k)}={p[k][pk]},"
            if v.endswith(","):
                v = v[:-1]
            if not v:
                continue

            self.options['kv'].append(
                {'--placement-pref': f'"{v}"'}
            )


    # -quiet, -q

    # --read-only
    def read_only(self):
        if "ReadOnly" in list(self.inspect['Spec']['TaskTemplate']['ContainerSpec'].keys()):
            self.options['k'].append("--read-only")

    # --replicas-max-per-node, Maximum number of tasks per node (default 0 = unlimited)
    def replicas_max_per_node(self):
        if self.inspect['Spec']['TaskTemplate']['Placement']['MaxReplicas']:
            self.options['kv'].append(
                {'--replicas-max-per-node': self.inspect['Spec']['TaskTemplate']['Placement']['MaxReplicas']}
            )


    # --reserve-cpu
    def reserve_cpu(self):
        nc = self.inspect['Spec']['TaskTemplate']['Resources']['Reservations']['NanoCPUs']
        self.options['kv'].append(
            {'--reserve-cpu': nc / 10**9}
        )

    # --reserve-memory
    def reserve_memory(self):
        mb = self.inspect['Spec']['TaskTemplate']['Resources']['Reservations']['MemoryBytes']
        self.options['kv'].append(
            {'--reserve-memory': unit_converter(mb)}
        )

    # --restart-condition, Restart when condition is met ("none"|"on-failure"|"any") (default "any")
    # --restart-delay, Delay between restart attempts (ns|us|ms|s|m|h) (default 5s)
    # --restart-max-attempts, Maximum number of restarts before giving up
    def restart_policy(self):
        rp: dict = self.inspect['Spec']['TaskTemplate']['RestartPolicy']
        ## --restart-condition
        if rp['Condition'] != "any":
            self.options['kv'].append(
                {'--restart-condition': rp['Condition']}
            )

        ## --restart-delay
        if rp['Delay'] != 5000000000:
            self.options['kv'].append(
                {'--restart-delay': f"{int(rp['Delay'] / 10**9)}s"}
            )

        ## --restart-max-attempts
        if rp['MaxAttempts'] != 0:
            self.options['kv'].append(
                {'--restart-max-attempts': rp['MaxAttempts']}
            )

    # --rollback-delay, Delay between task rollbacks (ns|us|ms|s|m|h) (default 0s)
    # --rollback-failure-action, Action on rollback failure ("pause"|"continue") (default "pause")
    # --rollback-max-failure-ratio
    # --rollback-monitor, Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h) (default 5s)
    # --rollback-order, Rollback order ("start-first"|"stop-first") (default "stop-first")
    # --rollback-parallelism, Maximum number of tasks rolled back simultaneously (0 to roll back all at once), The default value is 1
    def rollback_config(self):
        rc: dict = self.inspect['Spec']['RollbackConfig']
        ## --rollback-parallelism
        if rc['Parallelism'] != 1:
            self.options['kv'].append(
                {'--rollback-parallelism': rc['Parallelism']}
            )

        ## --rollback-failure-action
        if rc['FailureAction'] != "pause":
            self.options['kv'].append(
                {'--rollback-failure-action': rc['FailureAction']}
            )

        ## --rollback-monitor
        if rc['Monitor'] != 5000000000:
            self.options['kv'].append(
                {'--rollback-monitor': f"{int(rc['Monitor'] / 10**9)}s"}
            )

        ## --rollback-max-failure-ratio
        if rc['MaxFailureRatio'] != 0:
            self.options['kv'].append(
                {'--rollback-max-failure-ratio': rc['MaxFailureRatio']}
            )

        ## --rollback-order
        if rc['Order'] != "stop-first":
            self.options['kv'].append(
                {'--rollback-order': rc['Order']}
            )

        ## --rollback-delay
        try:
            if rc['Delay']:
                self.options['kv'].append(
                    {'--rollback-delay': f"{int(rc['Delay'] / 10 ** 9)}s"}
                )
        except:
            pass

    # --stop-grace-period, Time to wait before force killing a container (ns|us|ms|s|m|h) (default 10s)
    def stop_grace_period(self):
        sgp = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['StopGracePeriod']
        if sgp != 10000000000:
            self.options['kv'].append(
                {'--stop-grace-period': f"{int(sgp / 10**6)}ms"}
            )

    # --stop-signal
    def stop_signal(self):
        self.options['kv'].append(
            {'--stop-signal': self.inspect['Spec']['TaskTemplate']['ContainerSpec']['StopSignal']}
        )

    # --sysctl
    def sysctl(self):
        sysctls: dict = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Sysctls']
        for k in sysctls:
            self.options['kv'].append(
                {'--sysctl': f"{k}={sysctls[k]}"}
            )

    # --ulimit
    def ulimit(self):
        ulimits: list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Ulimits']
        for u in ulimits:
            if u['Hard'] != u['Soft']:
                v = f"{u['Soft']}:{u['Hard']}"
            else:
                v = u['Soft']
            self.options['kv'].append(
                {'--ulimit': f"{u['Name']}={v}"}
            )

    # --update-delay
    # --update-parallelism, Maximum number of tasks updated simultaneously (0 to update all at once)
    # --update-failure-action, Action on update failure ("pause"|"continue"|"rollback") (default "pause")
    # --update-monitor
    # --update-max-failure-ratio, Failure rate to tolerate during an update (default 0)
    # --update-order, Update order ("start-first"|"stop-first") (default "stop-first")
    def update_config(self):
        uc: dict = self.inspect['Spec']['UpdateConfig']
        ## --update-parallelism
        if uc['Parallelism'] != 1:
            self.options['kv'].append(
                {'--update-parallelism': uc['Parallelism']}
            )

        ## --update-failure-action
        if uc['FailureAction'] != "pause":
            self.options['kv'].append(
                {'--update-failure-action': uc['FailureAction']}
            )

        ## --update-monitor
        if uc['Monitor'] != 5000000000:
            self.options['kv'].append(
                {'--rollback-monitor': f"{int(uc['Monitor'] / 10 ** 9)}s"}
            )

        ## --update-max-failure-ratio
        if uc['MaxFailureRatio'] != 0:
            self.options['kv'].append(
                {'--update-max-failure-ratio': uc['MaxFailureRatio']}
            )

        ## --update-order
        if uc['Order'] != "stop-first":
            self.options['kv'].append(
                {'--update-order': uc['Order']}
            )

        ## --update-delay
        try:
            if uc['Delay']:
                self.options['kv'].append(
                    {'--update-delay': f"{int(uc['Delay'] / 10 ** 9)}s"}
                )
        except:
            pass

    # --user, -u, Username or UID (format: <name|uid>[:<group|gid>])
    def user(self):
        u = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['User']
        self.options['kv'].append(
            {'--user': u}
        )

    # --with-registry-auth



    # Args, docker service create command args
    def arguments(self):
        li: list = self.inspect['Spec']['TaskTemplate']['ContainerSpec']['Args']
        if li:
            self.args.append(li)

if __name__ == '__main__':
    if len(argv) < 2 or argv[1] == "--help":
        MYDOCKER.help_msg()
        exit(1)

    # 查看所有service的docker service create命令
    elif argv[1] == "{all}":
        for serv in MYDOCKER().get_services():
            print(f"=== service: {serv['Spec']['Name']} ===")
            try:
                MYDOCKER(serv['Spec']['Name']).start()
            except:
                pass
            print("\n")
    elif len(argv) > 2:
        for s in argv[1:]:
            print(f"=== service: {s} ===")
            try:
                MYDOCKER(s).start()
            except:
                pass
            print("\n")
    else:
        mydocker = MYDOCKER(argv[1])
        ret = mydocker.start()