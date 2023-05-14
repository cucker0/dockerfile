# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

"""
解析docker 容器的启动参数

require: python 3

author: Song yanlin
mail: hanxiao2100@qq.com
date: 2021-09-24
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
    """驼峰字符串转连接字符格式。

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

def key_in_dict(key, dic: dict, val=None) -> bool:
    """判断一个key是否存在于指定的字典中

    :param key:
    :param dic:
    :param val: object
        当key不存在时，新建的key对应的值
    :return:
    """
    try:
        if not (val is None):
            if key not in list(dic):
                dic[key] = val
        return (key in list(dic))
    except:
        return False

def remve_prefix(s: str, prefix = "/"):
    """去掉字符串指定的前缀

    :param s:
    :param prefix:
    :return:
    """
    if s.startswith(prefix):
        return s[1:]
    return s

class MYDOCKER(object):
    def __init__(self, container=None):
        super(MYDOCKER, self).__init__()
        if not os.path.exists("/var/run/docker.sock"):
            self.help_msg()
            exit(1)
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

        # container name or container id. type is str
        self.container = container
        self.inspect:dict = {}
        self.docker_run_cmd = ""
        self.options = {"kv": [], "k": []}
        self.image = None  # str
        self.args = []
        self.inspect_image:dict = {}
        self.entity_info = {'type': None, 'name': None}  # Options: container, service, stack

    def get_containers(self, all=False) -> list:
        """

        :param all: bool
            True: 所有容器，包括已经 shutdown的容器
            False: 当前在run的容器
        :return:
        """
        return self.api_client.containers(all=all)

    def check_entity_type(self):
        """判断传入的实体类型

        :return:
        """
        if not self.inspect:
            return
        if key_in_dict("Labels", self.inspect['Config']):
            if key_in_dict("com.docker.stack.namespace", self.inspect['Config']['Labels']):
                self.entity_info['type'] = "stack"
                self.entity_info['name'] = self.inspect['Config']['Labels']['com.docker.stack.namespace']
            elif key_in_dict("com.docker.swarm.service.name", self.inspect['Config']['Labels']):
                self.entity_info['type'] = "service"
                self.entity_info['name'] = self.inspect['Config']['Labels']['com.docker.swarm.service.name']
            else:
                self.entity_info['type'] = "container"

    def _print_command(self):
        """

        Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

        :return: str
            运行容器的完整命令
        """
        if not self.inspect:
            return
        if self.entity_info['type'] == "stack":
            print(f"This is a docker stack: {self.entity_info['name']}.")
            print(
                "Reverse stack to a compose file reference `https://hub.docker.com/repository/docker/cucker/stack2compose`")
            print("docker run command: ")
        elif self.entity_info['type'] == "service":
            print(f"This is a docker service: {self.entity_info['name']}.")
            print(
                "Get the command for docker service create by the service reference `https://hub.docker.com/repository/docker/cucker/get_command_by_service`")
            print("docker run command: ")

        options_key = ""
        if self.options['k']:
            options_key = "-"
        #  key 型options
        for k in self.options['k']:
            options_key += f"{k}"
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
                options = f"{options_key} \\\n {options_kv.lstrip(' ')}"
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
                    if i.startswith('"') and i.endswith('"'):
                        pass
                    elif i.startswith("'") and i.endswith("'"):
                        pass
                    else:
                        i = f'"{i}"'
                _args += f"{i} "

            command = f"docker run {options} {self.image} {_args}"
        else:
            command = f"docker run {options} {self.image}"
        print(command)

    def _get_inspect_container(self):

        """

        :return:
        """
        try:
            self.inspect = self.api_client.inspect_container(self.container)

        except APIError as e:
            print(e)
            exit(-1)

    def _get_inspect_image(self):
        if not self.inspect:
            self._get_inspect_container()

        # image
        image = self.inspect['Config']['Image']
        try:
            self.inspect_image = self.api_client.inspect_image(image)
        except Exception as e:
            print(e)

    def _get_container_name_by_id(self, container_id):
        """通过容器ID查询容器名

        :param container_id:
        :return: str
            容器名
        """
        inspect = self.api_client.inspect_container(container_id)
        return inspect['Name'].replace("/", "")

    def _parse_inspect_container(self):
        # image
        self.image: str = self.inspect['Config']['Image'].split('@')[0]
        if self.image.startswith('sha256:'):  # 在本地没有此image的，将直接显示原来的image id. 或者有些直接指定就是image_id
            self.image = self.image.split(':')[1]

        # parse options
        obj = PARSE_OPTIONS(self.inspect, self.options, self.args, self.inspect_image)
        for m in get_user_methods_by_class_(obj):
            try:
                m()
            except:
                pass

    @staticmethod
    def help_msg():
        _MSG = """Usage:
# Command alias
echo "alias get_run_command='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock cucker/get_command_4_run_container'" >> ~/.bashrc
. ~/.bashrc

# Excute command
## For all runing containers
get_run_command {allrun}

## For all containers include shutdown
get_run_command {all}

## For one or more containers
get_run_command <CONTAINER> [CONTAINER...]
"""
        print(_MSG)

    def start(self):
        self._get_inspect_container()
        self._get_inspect_image()
        self.check_entity_type()
        self._parse_inspect_container()
        self._print_command()

class PARSE_OPTIONS(object):
    """从container inspect信息中解析docker run命令的options 和 arguments

    """
    dock = MYDOCKER()

    def __init__(self, inspect: dict, options: dict, args: list, inspect_image: dict):
        self.inspect = inspect
        self.options = options
        self.args = args
        self.inspect_image = inspect_image

    # --name
    def _name(self):
        if "Name" in self.inspect:
            self.options['kv'].append(
                {"--name": self.inspect['Name'].replace("/", "")}
            )

    # --rm, Automatically remove the container when it exits。
    # --rm比较特殊，放在options['kv']的第一个。 这里把它当kv类型的option处理。
    def _rm(self):
        if self.inspect['HostConfig']['AutoRemove']:
            self.options['kv'].append(
                {"--rm": ""}
            )

    # --privileged
    def _privileged(self):
        if self.inspect['HostConfig']['Privileged']:
            self.options['kv'].append(
                {"--privileged": ""}
            )

    # --hostname
    def hostname(self):
        if not self.inspect['Id'].startswith(self.inspect['Config']['Hostname']):
            self.options['kv'].append(
                {"--hostname": self.inspect['Config']['Hostname']}
            )

    # --detach. Run container in background and print container ID
    def detach(self):
        self.options['k'].append("d")

    # --tty, -t		Allocate a pseudo-TTY
    # --interactive, -i, Keep STDIN open even if not attached
    def tty(self):
        if self.inspect['Config']['Tty']:
            self.options['k'].append("t")
        if self.inspect['Config']['OpenStdin']:
            self.options['k'].append("i")

    # --attach, -a		Attach to STDIN, STDOUT or STDERR
    def attach(self):
        if self.inspect['Config']['AttachStdin'] and self.inspect['Config']['AttachStdout'] and self.inspect['Config'][
            'AttachStderr']:
            self.options['k'].append("a")

    # --restart, "no" is default.
    def restart(self):
        _restart_policy = self.inspect['HostConfig']['RestartPolicy']
        if _restart_policy['Name'] == "on-failure":
            self.options['kv'].append(
                {"--restart=": f"on-failure:{_restart_policy['MaximumRetryCount']}"}
            )
        if _restart_policy['Name'] in ("unless-stopped", "always"):
            self.options['kv'].append(
                {"--restart=": _restart_policy['Name']}
            )

    # --mount
    def mount(self):
        if not self.inspect['Mounts']:
            return
        bs = []
        if self.inspect['HostConfig']['Binds']:
            for b in self.inspect['HostConfig']['Binds']:
                bs.append(b.split(":")[0])
        image_volumes = []
        if self.inspect['Config']['Volumes']:
            image_volumes = list(self.inspect['Config']['Volumes'].keys())
        for m in self.inspect['Mounts']:
            try:
                if m['Source'].endswith("/"):
                    source_m = m['Source'][:-1]
                else:
                    source_m = f"{m['Source']}/"

                if (m['Source'] in bs) or (source_m in bs):
                    continue
                # 在image定义的 VOLUME
                if key_in_dict("Name", m) and (len(m['Name']) == 64) and (m['Destination'] in image_volumes):
                    continue
                v = f"type={m['Type']},src={m['Source']},dst={m['Destination']}"
                if key_in_dict("Driver", m):
                    if m['Driver'] != "local":
                        v += f",volume-driver={m['Driver']}"
                if m['Mode']:
                    v += f",mode={m['Mode']}"

                self.options['kv'].append(
                    {"--mount": v}
                    )
            except Exception as e:
                print(e)
                pass

    # --volume, -v
    def volume(self):
        if not self.inspect['HostConfig']['Binds']:
            return
        for v in self.inspect['HostConfig']['Binds']:
            self.options['kv'].append(
                {'-v': v}
            )

    # --volumes-from, 挂载指定容器的数据卷
    '''
    "VolumesFrom": [
            "web_data:rw",
            "nginx-2:Z"
        ]
    '''
    def volumes_from(self):
        if self.inspect['HostConfig']['VolumesFrom']:
            for volu in self.inspect['HostConfig']['VolumesFrom']:
                self.options['kv'].append(
                    {"--volumes-from": volu}
                )

    # --publish, -p  Publish a container's port(s) to the host
    def publish(self):
        if self.inspect['HostConfig']['PortBindings']:
            _pbs = self.inspect['HostConfig']['PortBindings']
            for p in _pbs:
                for psub in _pbs[p]:
                    if psub['HostIp']:
                        self.options['kv'].append(
                            {"-p": f"{psub['HostIp']}:{psub['HostPort']}:{p}"}
                        )
                    else:
                        self.options['kv'].append(
                            {"-p": f"{psub['HostPort']}:{p}"}
                        )

    # --env, -e
    def env(self):
        # 在容器inspect['Config']['Env']存在，且在镜像inspect_image['Config']['Env']不存在的元素，则为容器运行时添加的env
        """
        "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "NGINX_VERSION=1.19.1",
                "NJS_VERSION=0.4.2",
                "PKG_RELEASE=1~buster"
            ]


        -- inspect_image
        "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "NGINX_VERSION=1.21.1",
                "NJS_VERSION=0.6.1",
                "PKG_RELEASE=1~buster"
            ]
        """
        for env in self.inspect['Config']['Env']:
            if env not in self.inspect_image['Config']['Env']:
                self.options['kv'].append(
                    {"--env": env}
                )

    # --workdir, -w
    def workdir(self):
        if self.inspect['Config']['WorkingDir']:
            self.options['kv'].append(
                {"-w": self.inspect['Config']['WorkingDir']}
            )

    # --cpu-shares, -c
    def cpu_shares(self):
        if self.inspect['HostConfig']['CpuShares'] != 0:
            self.options['kv'].append(
                {"-c": self.inspect['HostConfig']['CpuShares']}
            )

    # --cpu-period
    def cpu_period(self):
        if self.inspect['HostConfig']['CpuPeriod'] != 0:
            self.options['kv'].append(
                {"--cpu-period=": self.inspect['HostConfig']['CpuPeriod']}
            )

    # --cpu-quota
    def cpu_quota(self):
        if self.inspect['HostConfig']['CpuQuota'] != 0:
            self.options['kv'].append(
                {"--cpu-quota=": self.inspect['HostConfig']['CpuQuota']}
            )

    # --cpus
    def cpus(self):
        if self.inspect['HostConfig']['NanoCpus'] != 0:
            self.options['kv'].append(
                {"--cpus": self.inspect['HostConfig']['NanoCpus'] / 10 ** 9}
            )

    # --memory, -m
    def memory(self):
        if self.inspect['HostConfig']['Memory'] != 0:
            self.options['kv'].append(
                {"-m": unit_converter(self.inspect['HostConfig']['Memory'])}
            )

    # --blkio-weight
    def blkio_weight(self):
        if self.inspect['HostConfig']['BlkioWeight'] != 0:
            self.options['kv'].append(
                {"--blkio-weight": self.inspect['HostConfig']['BlkioWeight']}
            )

    # --device-read-bps
    def device_read_bps(self):
        if self.inspect['HostConfig']['BlkioDeviceReadBps']:
            for r in self.inspect['HostConfig']['BlkioDeviceReadBps']:
                self.options['kv'].append(
                    {"--device-read-bps": f"{r['Path']}:{unit_converter(r['Rate'])}"}
                )

    # --device-write-bps
    def device_write_bps(self):
        if self.inspect['HostConfig']['BlkioDeviceWriteBps']:
            for w in self.inspect['HostConfig']['BlkioDeviceWriteBps']:
                self.options['kv'].append(
                    {"--device-write-bps": f"{w['Path']}:{unit_converter(w['Rate'])}"}
                )

    # --device-read-iops
    def device_read_iops(self):
        if self.inspect['HostConfig']['BlkioDeviceReadIOps']:
            for rio in self.inspect['HostConfig']['BlkioDeviceReadIOps']:
                self.options['kv'].append(
                    {"--device-read-iops": f"{rio['Path']}:{rio['Rate']}"}
                )

    # --device-write-iops
    def device_write_iops(self):
        if self.inspect['HostConfig']['BlkioDeviceWriteIOps']:
            for wio in self.inspect['HostConfig']['BlkioDeviceWriteIOps']:
                self.options['kv'].append(
                    {"--device-write-iops": f"{wio['Path']}:{wio['Rate']}"}
                )

    # --net, --network
    def network(self):
        if self.inspect['HostConfig']['NetworkMode'] != 'default':
            # joined容器网络（共用容器网络）==
            '''共用容器网络 示例
            {
                "HostConfig": {
                    "NetworkMode": "container:8c9d8e9a4180f3e28c287202b4638a6ef9d26e639726b4a1140704d1ebab70b2"
                    ...
            }
                ...
            '''
            if self.inspect['HostConfig']['NetworkMode'].startswith('container:'):
                source_container_id = self.inspect['HostConfig']['NetworkMode'].split(':')[1]
                self.options['kv'].append(
                    {"--network=": "container:" + self.dock._get_container_name_by_id(source_container_id)}
                )
            else:  # 指定网络 ==
                self.options['kv'].append(
                    {"--network=": self.inspect['HostConfig']['NetworkMode']}
                )

    # --entrypoint
    def entrypoint(self):
        if not self.inspect['Config']['Entrypoint']:  # self.inspect['Config']['Entrypoint'] 为list
            return
        if self.inspect['Config']['Entrypoint'] != self.inspect_image['Config']['Entrypoint']:
            ep = " ".join(self.inspect['Config']['Entrypoint'])
            if ep.__contains__(' "'):
                v = f"'{ep}'"
            elif ep.__contains__(" '"):
                v = f'"{ep}"'
            elif ep.__contains__(" "):
                v = f'"{ep}"'
            else:
                v = ep
            self.options['kv'].append(
                {"--entrypoint": v}
            )

    # --dns
    def dns(self):
        if self.inspect['HostConfig']['Dns']:  # self.inspect['HostConfig']['Dns'] 为list
            for d in self.inspect['HostConfig']['Dns']:
                self.options['kv'].append(
                    {"--dns": d}
                )
    # --dns-option
    def dns_option(self):
        if self.inspect['HostConfig']['DnsOptions']:
            for d in self.inspect['HostConfig']['DnsOptions']:
                self.options['kv'].append(
                    {"--dns-option": d}
                )

    # --dns-search
    def dns_search(self):
        if self.inspect['HostConfig']['DnsSearch']:
            for d in self.inspect['HostConfig']['DnsSearch']:
                self.options['kv'].append(
                    {"--dns-search": d}
                )

    # --domainname
    def domainname(self):
        if self.inspect['Config']['Domainname']:
            self.options['kv'].append(
                {"--domainname": self.inspect['Config']['Domainname']}
            )

    # --user , -u
    def user(self):
        if self.inspect['Config']['User']:
            self.options['kv'].append(
                {"--user": self.inspect['Config']['User']}
            )

    # --add-host
    def add_host(self):
        if self.inspect['HostConfig']['ExtraHosts']:
            for h in self.inspect['HostConfig']['ExtraHosts']:
                self.options['kv'].append(
                    {"--add-host=": h}
                )

    # --volume-driver
    def volume_driver(self):
        if self.inspect['HostConfig']['VolumeDriver']:
            self.options['kv'].append(
                {"--volume-driver": self.inspect['HostConfig']['VolumeDriver']}
            )

    # --uts
    def uts(self):
        if self.inspect['HostConfig']['UTSMode']:
            self.options['kv'].append(
                {"--uts": self.inspect['HostConfig']['UTSMode']}
            )

    # --userns
    def userns(self):
        if self.inspect['HostConfig']['UsernsMode']:
            self.options['kv'].append(
                {"--uts": self.inspect['HostConfig']['UsernsMode']}
            )

    # --shm-size, Size of /dev/shm default is 64MB(67108864 byte).
    def shm_size(self):
        if self.inspect['HostConfig']['ShmSize'] != 67108864:
            self.options['kv'].append(
                {"--shm-size": unit_converter(self.inspect['HostConfig']['ShmSize'])}
            )

    # --link. 用于连接其它容器。是比较老旧的技术，可以把要通行的几个容器连接到同一个单独的网络 来替代
    def link(self):
        if self.inspect['HostConfig']['Links']:  # self.inspect['HostConfig']['Links'] 为null或[]
            for i in self.inspect['HostConfig']['Links']:
                self.options['kv'].append(
                    {"--add-host=": i}
                )

    # --ipc
    def ipc(self):
        if self.inspect['HostConfig']['IpcMode'] and (self.inspect['HostConfig']['IpcMode'] != "private"):
            self.options['kv'].append(
                {"--ipc": self.inspect['HostConfig']['IpcMode']}
            )
    # --log-driver
    # --log-opt
    def log_config(self):
        logconfig: dict = self.inspect['HostConfig']['LogConfig']
        ## --log-driver
        if key_in_dict("Type", logconfig):
            if logconfig['Type'] != "json-file":
                self.options['kv'].append(
                    {'--log-driver': logconfig['Type']}
                )
        # --log-opt
        if key_in_dict("Config", logconfig):
            for k in logconfig['Config']:
                self.options['kv'].append(
                    {'--log-opt': f"{k}={logconfig['Config'][k]}"}
                )


    # --label , -l
    def label(self):
        labels: dict = self.inspect['Config']['Labels']
        for k in labels:
            if not key_in_dict(k, self.inspect_image['Config']['Labels']):
                if labels[k]:
                    self.options['kv'].append(
                        {'--label': f"{k}={labels[k]}"}
                    )
                else:
                    self.options['kv'].append(
                        {'--label': f'{k}=""'}
                    )

    # --init
    def init(self):
        if self.inspect['HostConfig']['Init']:  # inspect['HostConfig']['Init'] 为 bool值
            self.options['kv'].append(
                {'--init': ''}
            )


    # --stop-signal
    def stop_signal(self):
        if key_in_dict("StopSignal", self.inspect['Config']):
            self.options['kv'].append(
                {'--stop-signal': self.inspect['Config']['StopSignal']}
            )

    # --health-cmd
    # --health-interval
    # --health-retries
    # --health-start-period
    # --health-timeout
    # --no-healthcheck
    def health_check(self):
        hc: dict = self.inspect['Config']['Healthcheck']
        # --health-cmd
        try:
            if hc['Test'][0] == "CMD-SHELL":
                self.options['kv'].append(
                    {'--health-cmd': f'"{hc["Test"][1]}"'}
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
                    {'--health-interval': f"{int(hc['Interval'] / 10 ** 9)}s"}
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
                    {'--health-start-period': f"{int(hc['StartPeriod'] / 10 ** 9)}s"}
                )
        except:
            pass

        # --health-timeout
        try:
            if hc['Timeout']:
                self.options['kv'].append(
                    {'--health-timeout': f"{int(hc['Timeout'] / 10 ** 9)}s"}
                )
        except:
            pass

    # --isolation
    def isolation(self):
        if self.inspect['HostConfig']['Isolation'] and (self.inspect['HostConfig']['Isolation'] != "default"):
            self.options['kv'].append(
                {'--isolation': self.inspect['HostConfig']['Isolation']}
            )

    # --device
    def device(self):
        devices: list = self.inspect['HostConfig']['Devices']
        for d in devices:
            if d['CgroupPermissions'] == "rwm":
                v = f"{d['PathOnHost']}:{d['PathInContainer']}"
            else:
                v = f"{d['PathOnHost']}:{d['PathInContainer']}:{d['CgroupPermissions']}"
            self.options['kv'].append(
                {'--device=': v}
            )

    # --sysctl
    def sysctl(self):
        sysctls: dict = self.inspect['HostConfig']['Sysctls']
        for k in sysctls:
            self.options['kv'].append(
                {'--sysctl': f"{k}={sysctls[k]}"}
            )

    # --pid
    def pid(self):
        if self.inspect['HostConfig']['PidMode']:
            self.options['kv'].append(
                {'--pid': self.inspect['HostConfig']['PidMode']}
            )
    # --cap-add
    def cap_add(self):
        if self.inspect['HostConfig']['CapAdd']:
            for c in self.inspect['HostConfig']['CapAdd']:
                self.options['kv'].append(
                    {'--cap-add': c}
                )


    # --cap-drop
    def cap_drop(self):
        if self.inspect['HostConfig']['CapDrop']:
            for c in self.inspect['HostConfig']['CapDrop']:
                self.options['kv'].append(
                    {'--cap-drop': c}
                )

    # --ulimit
    def ulimit(self):
        ulimits: list = self.inspect['HostConfig']['Ulimits']
        for u in ulimits:
            if u['Hard'] != u['Soft']:
                v = f"{u['Soft']}:{u['Hard']}"
            else:
                v = u['Soft']
            self.options['kv'].append(
                {'--ulimit': f"{u['Name']}={v}"}
            )

    # --cgroupns, Cgroup namespace to use (host|private|'')
    def cgroupns(self):
        if not self.inspect['HostConfig']['CgroupnsMode']:
            return
        if self.inspect['HostConfig']['CgroupnsMode'] != "private":
            self.options['kv'].append(
                {'--cgroupns': self.inspect['HostConfig']['CgroupnsMode']}
            )

    # --cgroup-parent
    def cgroup_parent(self):
        v = self.inspect['HostConfig']['CgroupParent']
        if v:
            self.options['kv'].append(
                {'--cgroup-parent': v}
            )

    # --tmpfs
    def tmpfs(self):
        if not key_in_dict("Tmpfs", self.inspect['HostConfig']):
            return
        ts: dict = self.inspect['HostConfig']['Tmpfs']
        for k in ts:
            self.options['kv'].append(
                {'--tmpfs': f"{k}:{ts[k]}"}
            )

    # --cidfile
    def cidfile(self):
        v = self.inspect['HostConfig']['ContainerIDFile']
        if v:
            self.options['kv'].append(
                {'--cidfile': v}
            )

    # --cpu-rt-period, Limit CPU real-time period in microseconds
    def cpu_rt_period(self):
        v: int = self.inspect['HostConfig']['CpuRealtimePeriod']
        if v != 0:
            self.options['kv'].append(
                {'--cpu-rt-period': v}
            )

    # --cpu-rt-runtime, Limit CPU real-time runtime in microseconds
    def cpu_rt_runtime(self):
        v: int = self.inspect['HostConfig']['CpuRealtimeRuntime']
        if v != 0:
            self.options['kv'].append(
                {'--cpu-rt-runtime': v}
            )

    # command and args
    def arguments(self):
        # 如果 self.inspect['Config']['Cmd'] 与 self.inspect_image['Config']['Cmd'] 不相同，说明docker run传参数了。
        if self.inspect['Config']['Cmd'] and (self.inspect['Config']['Cmd'] != self.inspect_image['Config']['Cmd']):
            self.args.append(self.inspect['Config']['Cmd'])

def main():
    if len(argv) < 2 or argv[1] == "--help":
        MYDOCKER.help_msg()
        exit(1)

    # 查看所有container的docker run命令
    elif argv[1] in ("{all}", "{allrun}"):
        # {all}: 包括shutdown的所有容器
        # {allrun}: 当前状态为run的所有容器
        is_all = False
        if argv[1] == "{all}":
            is_all = True

        for container in MYDOCKER().get_containers(is_all):
            print(f"=== container: {remve_prefix(container['Names'][0])} ===")
            try:
                MYDOCKER(container['Id']).start()
            except:
                pass
            print("\n")
    elif len(argv) > 2:
        for s in argv[1:]:
            print(f"=== container: {s} ===")
            try:
                MYDOCKER(s).start()
            except:
                pass
            print("\n")
    else:
        MYDOCKER(argv[1]).start()

if __name__ == '__main__':
    main()
