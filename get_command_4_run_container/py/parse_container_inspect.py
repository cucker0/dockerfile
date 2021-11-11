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

class MYDOCKER(object):
    def __init__(self):
        super(MYDOCKER, self).__init__()
        if not os.path.exists("/var/run/docker.sock"):
            self.help_msg()
            exit(1)
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

        # container name or container id. type is str
        self.container = argv[1]
        self.inspect:dict = {}
        self.docker_run_cmd = ""
        self.options = {"kv": [], "k": []}
        self.image = None  # str
        self.args = []
        self.inspect_image:dict = {}

    def _print_docker_run_cmd(self):
        """

        Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

        :return: str
            运行容器的完整命令
        """
        if not self.inspect:
            return

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

        if self.args:
            _args = ""
            for i in self.args:
                _args += f"{i} "
            _args = _args.strip()
            self.docker_run_cmd = f"docker run {options} {self.image} {_args}"
        else:
            self.docker_run_cmd = f"docker run {options} {self.image}"
        print(self.docker_run_cmd)

    def _get_inspect_container(self):

        """

        * Example for get inspect for a container
        self.api_client.inspect_container("mysql01")
{
    'Id': 'cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955',
    'Created': '2021-04-25T09:52:13.612852757Z',
    'Path': 'docker-entrypoint.sh', 'Args': ['mysqld'],
    'State': {
        'Status': 'running',
        'Running': True,
        'Paused': False,
        'Restarting': False,
        'OOMKilled': False,
        'Dead': False,
        'Pid': 2133,
        'ExitCode': 0,
        'Error': '',
        'StartedAt': '2021-09-11T14:12:05.741885047Z',
        'FinishedAt': '2021-09-11T22:12:03.260400088+08:00'
    },
    'Image': 'sha256:0627ec6901db4b2aed6ca7ab35e43e19838ba079fffe8fe1be66b6feaad694de',
    'ResolvConfPath': '/var/lib/docker/containers/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955/resolv.conf',
    'HostnamePath': '/var/lib/docker/containers/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955/hostname',
    'HostsPath': '/var/lib/docker/containers/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955/hosts',
    'LogPath': '/var/lib/docker/containers/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955-json.log',
    'Name': '/mysql01',
    'RestartCount': 0,
    'Driver': 'overlay2',
    'Platform': 'linux',
    'MountLabel': '',
    'ProcessLabel': '',
    'AppArmorProfile': '',
    'ExecIDs': None,
    'HostConfig': {
        'Binds': None,
        'ContainerIDFile': '',
        'LogConfig': {'Type': 'json-file', 'Config': {}},
        'NetworkMode': 'default',
        'PortBindings': {
            '3306/tcp': [
                {'HostIp': '', 'HostPort': '13306'}
            ]
        },
        'RestartPolicy': {
            'Name': 'always',
            'MaximumRetryCount': 0
        },
        'AutoRemove': False,
        'VolumeDriver': '',
        'VolumesFrom': None,
        'CapAdd': None,
        'CapDrop': None,
        'CgroupnsMode': 'host',
        'Dns': [],
        'DnsOptions': [],
        'DnsSearch': [],
        'ExtraHosts': None,
        'GroupAdd': None,
        'IpcMode': 'private',
        'Cgroup': '',
        'Links': None,
        'OomScoreAdj': 0,
        'PidMode': '',
        'Privileged': False,
        'PublishAllPorts': False,
        'ReadonlyRootfs': False,
        'SecurityOpt': None,
        'UTSMode': '',
        'UsernsMode': '',
        'ShmSize': 67108864,
        'Runtime': 'runc',
        'ConsoleSize': [0, 0],
        'Isolation': '',
        'CpuShares': 0,
        'Memory': 0,
        'NanoCpus': 0,
        'CgroupParent': '',
        'BlkioWeight': 0,
        'BlkioWeightDevice': [],
        'BlkioDeviceReadBps': None,
        'BlkioDeviceWriteBps': None,
        'BlkioDeviceReadIOps': None,
        'BlkioDeviceWriteIOps': None,
        'CpuPeriod': 0,
        'CpuQuota': 0,
        'CpuRealtimePeriod': 0,
        'CpuRealtimeRuntime': 0,
        'CpusetCpus': '',
        'CpusetMems': '',
        'Devices': [],
        'DeviceCgroupRules': None,
        'DeviceRequests': None,
        'KernelMemory': 0,
        'KernelMemoryTCP': 0,
        'MemoryReservation': 0,
        'MemorySwap': 0,
        'MemorySwappiness': None,
        'OomKillDisable': False,
        'PidsLimit': None,
        'Ulimits': None,
        'CpuCount': 0,
        'CpuPercent': 0,
        'IOMaximumIOps': 0,
        'IOMaximumBandwidth': 0,
        'MaskedPaths': [
            '/proc/asound', '/proc/acpi', '/proc/kcore', '/proc/keys', '/proc/latency_stats',
            '/proc/timer_list', '/proc/timer_stats', '/proc/sched_debug', '/proc/scsi',
            '/sys/firmware'
        ],
        'ReadonlyPaths': ['/proc/bus', '/proc/fs', '/proc/irq', '/proc/sys', '/proc/sysrq-trigger']
    },
    'GraphDriver': {
        'Data': {
            'LowerDir': '/var/lib/docker/overlay2/b29f5b9c07b807f6eba2f6d211f19f44e586fa8be48251c8b1cda8b816d23b5c-init/diff:/var/lib/docker/overlay2/bac38b553cca1c699e52cb93363d1a8480bfa2b881f0f62bb58549fd8f91f26a/diff:/var/lib/docker/overlay2/59d145469aba9d31081bd44decae7f97595d48befa1f63f4bfa70e7a6f126e75/diff:/var/lib/docker/overlay2/4e2678dbfad6da11df7c3f5812d344560ec4b55e0f70b81f28b0d02797cafacd/diff:/var/lib/docker/overlay2/8f051956166a117b761cfffbc23ae0ecf25575ec9756e037cc8e6877d4d0a834/diff:/var/lib/docker/overlay2/46974c7adc17c06e6b00720ff4797ff0c3b3a71454e89698fdae4aa030859488/diff:/var/lib/docker/overlay2/d714cc813d881b0281d4a63e45cec659ce0476e5c1464a17608b03a9554f1810/diff:/var/lib/docker/overlay2/96ed59222c210bacb377c2a23fec49b695f40d44fc12cfa7194ce865f231d6ec/diff:/var/lib/docker/overlay2/1f6bb66f8a09f556743e8e7ba5844cf7d9e8fd0fc1a9fee634cfba89bd233448/diff:/var/lib/docker/overlay2/abd94392e67ede2992a75ecdc00d5d01af4d581b24929a63d7e751a8d0f7eba3/diff:/var/lib/docker/overlay2/3cf69fc044e1a9c3936627f6a8a2ee4f30ade78a4fc26c02802416b2a7120a6e/diff:/var/lib/docker/overlay2/498d52bfc59807623d172a07df8e7afa631995452098711a954459dd07364ab7/diff:/var/lib/docker/overlay2/65224c6b7f4880dbedc01e02b903b21b0e032bd28ffdaf4a2d758ec35c1fcc31/diff',
            'MergedDir': '/var/lib/docker/overlay2/b29f5b9c07b807f6eba2f6d211f19f44e586fa8be48251c8b1cda8b816d23b5c/merged',
            'UpperDir': '/var/lib/docker/overlay2/b29f5b9c07b807f6eba2f6d211f19f44e586fa8be48251c8b1cda8b816d23b5c/diff',
            'WorkDir': '/var/lib/docker/overlay2/b29f5b9c07b807f6eba2f6d211f19f44e586fa8be48251c8b1cda8b816d23b5c/work'
        },
        'Name': 'overlay2'
    },
    'Mounts': [
        {'Type': 'volume',
         'Name': 'c69b2a1b7f8ff84bf90f52306c7ca86a944633d11e61ea7c29b75e8aeda4da34',
         'Source': '/var/lib/docker/volumes/c69b2a1b7f8ff84bf90f52306c7ca86a944633d11e61ea7c29b75e8aeda4da34/_data',
         'Destination': '/var/lib/mysql',
         'Driver': 'local',
         'Mode': '',
         'RW': True,
         'Propagation': ''
         }
    ],
    'Config': {
        'Hostname': 'cff524e16f5c',
        'Domainname': '',
        'User': '',
        'AttachStdin': False,
        'AttachStdout': False,
        'AttachStderr': False,
        'ExposedPorts': {
            '3306/tcp': {},
            '33060/tcp': {}
        },
        'Tty': False,
        'OpenStdin': False,
        'StdinOnce': False,
        'Env': [
            'MYSQL_ROOT_PASSWORD=py123456',
            'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
            'GOSU_VERSION=1.12', 'MYSQL_MAJOR=8.0', 'MYSQL_VERSION=8.0.24-1debian10'
        ],
        'Cmd': ['mysqld'],
        'Image': 'mysql',
        'Volumes': {'/var/lib/mysql': {}},
        'WorkingDir': '',
        'Entrypoint': ['docker-entrypoint.sh'],
        'OnBuild': None,
        'Labels': {}
    },
    'NetworkSettings': {
        'Bridge': '',
        'SandboxID': '4ff2100de411cf4eb0761f25bb8f9bf5d8fc99fc7dd8a9a566fe736de181bbcd',
        'HairpinMode': False,
        'LinkLocalIPv6Address': '',
        'LinkLocalIPv6PrefixLen': 0,
        'Ports': {
            '3306/tcp': [
                {'HostIp': '0.0.0.0', 'HostPort': '13306'}, {'HostIp': '::', 'HostPort': '13306'}
            ],
            '33060/tcp': None
        },
        'SandboxKey': '/var/run/docker/netns/4ff2100de411',
        'SecondaryIPAddresses': None,
        'SecondaryIPv6Addresses': None,
        'EndpointID': 'b8466e7784f624f17b55fad2c6fc31486c26444505d4315beb67cf53faa55e6b',
        'Gateway': '172.17.0.1',
        'GlobalIPv6Address': '',
        'GlobalIPv6PrefixLen': 0,
        'IPAddress': '172.17.0.3',
        'IPPrefixLen': 16,
        'IPv6Gateway': '',
        'MacAddress': '02:42:ac:11:00:03',
        'Networks': {
            'bridge': {
                'IPAMConfig': None,
                'Links': None,
                'Aliases': None,
                'NetworkID': 'ae3745bc55a172f99410058e94d5800b538dc8b7d08715a836ae4b929a1e3df5',
                'EndpointID': 'b8466e7784f624f17b55fad2c6fc31486c26444505d4315beb67cf53faa55e6b',
                'Gateway': '172.17.0.1',
                'IPAddress': '172.17.0.3',
                'IPPrefixLen': 16,
                'IPv6Gateway': '',
                'GlobalIPv6Address': '',
                'GlobalIPv6PrefixLen': 0,
                'MacAddress': '02:42:ac:11:00:03',
                'DriverOpts': None
            }
        }
    }
}

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
        if not self.inspect:
            self._get_inspect_container()

        # image
        self.image: str = self.inspect['Config']['Image']
        if self.image.startswith('sha256:'):  # 在本地没有此image的，将直接显示原来的image id
            self.image = self.image.split(':')[1]

        # options  --start
        # --rm, Automatically remove the container when it exits。
        # --rm比较特殊，放在options['kv']的第一个。 这里把它当kv类型的option处理。
        if self.inspect['HostConfig']['AutoRemove']:
            self.options['kv'].append(
                {"--rm": ""}
            )

        ## --privileged
        if self.inspect['HostConfig']['Privileged']:
            self.options['kv'].append(
                {"--privileged": ""}
            )

        ## --hostname
        if not self.inspect['Id'].startswith(self.inspect['Config']['Hostname']):
            self.options['kv'].append(
                {"--hostname": self.inspect['Config']['Hostname']}
            )

        ## --detach. Run container in background and print container ID
        self.options['k'].append("d")

        ## tty and stdin
        if self.inspect['Config']['Tty']:
            self.options['k'].append("t")
        if self.inspect['Config']['OpenStdin']:
            self.options['k'].append("i")

        ## --attach
        if self.inspect['Config']['AttachStdin'] and self.inspect['Config']['AttachStdout'] and self.inspect['Config']['AttachStderr']:
            self.options['k'].append("a")

        ## --name
        if "Name" in self.inspect:
            self.options['kv'].append(
                {"--name": self.inspect['Name'].replace("/", "")}
            )

        ## --restart, "no" is default.
        _restart_policy = self.inspect['HostConfig']['RestartPolicy']
        if _restart_policy['Name'] == "on-failure":
            self.options['kv'].append(
                {"--restart=": f"on-failure:{_restart_policy['MaximumRetryCount']}"}
            )
        if _restart_policy['Name'] in ("unless-stopped", "always"):
            self.options['kv'].append(
                {"--restart=": _restart_policy['Name']}
            )

        ## --volume, -v
        for mount in self.inspect['Mounts']:
            if mount['Type'] == "bind":
                if mount['RW']:
                    self.options['kv'].append(
                        {"-v": f"{mount['Source']}:{mount['Destination']}"}
                    )
                else:
                    self.options['kv'].append(
                        {"-v": f"{mount['Source']}:{mount['Destination']}:ro"}
                    )

        ## --volumes-from, 挂载指定容器的数据卷
        '''
        "VolumesFrom": [
                "web_data:rw",
                "nginx-2:Z"
            ]
        '''
        if self.inspect['HostConfig']['VolumesFrom']:
            for volu in self.inspect['HostConfig']['VolumesFrom']:
                self.options['kv'].append(
                    {"--volumes-from": volu}
                )

        ## --publish, -p
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


        ## --env, -e
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

        ## --workdir, -w
        if self.inspect['Config']['WorkingDir']:
            self.options['kv'].append(
                {"-w": self.inspect['Config']['WorkingDir']}
            )

        ## --rm, Auto Remove
        if self.inspect['HostConfig']['AutoRemove']:
            self.options['kv'].append(
                {"--rm": ""}
            )

        ## --cpu-shares, -c
        if self.inspect['HostConfig']['CpuShares'] != 0:
            self.options['kv'].append(
                {"-c": self.inspect['HostConfig']['CpuShares']}
            )

        ## --cpu-period
        if self.inspect['HostConfig']['CpuPeriod'] != 0:
            self.options['kv'].append(
                {"--cpu-period=": self.inspect['HostConfig']['CpuPeriod']}
            )

        ## --cpu-quota
        if self.inspect['HostConfig']['CpuQuota'] != 0:
            self.options['kv'].append(
                {"--cpu-quota=": self.inspect['HostConfig']['CpuQuota']}
            )

        ## --cpus
        if self.inspect['HostConfig']['NanoCpus'] != 0:
            self.options['kv'].append(
                {"--cpus": self.inspect['HostConfig']['NanoCpus'] / 10**9}
            )

        ## --memory, -m
        if self.inspect['HostConfig']['Memory'] != 0:
            self.options['kv'].append(
                {"-m": unit_converter(self.inspect['HostConfig']['Memory'])}
            )

        ## --blkio-weight
        if self.inspect['HostConfig']['BlkioWeight'] != 0:
            self.options['kv'].append(
                {"--blkio-weight": self.inspect['HostConfig']['BlkioWeight']}
            )

        ## --device-read-bps
        if self.inspect['HostConfig']['BlkioDeviceReadBps']:
            for r in self.inspect['HostConfig']['BlkioDeviceReadBps']:
                self.options['kv'].append(
                    {"--device-read-bps": f"{r['Path']}:{unit_converter(r['Rate'])}"}
                )

        ## --device-write-bps
        if self.inspect['HostConfig']['BlkioDeviceWriteBps']:
            for w in self.inspect['HostConfig']['BlkioDeviceWriteBps']:
                self.options['kv'].append(
                    {"--device-write-bps": f"{w['Path']}:{unit_converter(w['Rate'])}"}
                )

        ## --device-read-iops
        if self.inspect['HostConfig']['BlkioDeviceReadIOps']:
            for rio in self.inspect['HostConfig']['BlkioDeviceReadIOps']:
                self.options['kv'].append(
                    {"--device-read-iops": f"{rio['Path']}:{rio['Rate']}"}
                )

        ## --device-write-iops
        if self.inspect['HostConfig']['BlkioDeviceWriteIOps']:
            for wio in self.inspect['HostConfig']['BlkioDeviceWriteIOps']:
                self.options['kv'].append(
                    {"--device-write-iops": f"{wio['Path']}:{wio['Rate']}"}
                )

        ## --net, --network=
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
                    {"--network=": "container:" + self._get_container_name_by_id(source_container_id)}
                )
            else:  # 指定网络 ==
                self.options['kv'].append(
                    {"--network=": self.inspect['HostConfig']['NetworkMode']}
                )

        ## --entrypoint
        if self.inspect['Config']['Entrypoint']:  # self.inspect['Config']['Entrypoint'] 为list
            for ep in self.inspect['Config']['Entrypoint']:
                if ep not in self.inspect_image['Config']['Entrypoint']:
                    self.options['kv'].append(
                        {"--entrypoint": ep}
                    )

        ## --dns
        if self.inspect['HostConfig']['Dns']:  # self.inspect['HostConfig']['Dns'] 为list
            for d in self.inspect['HostConfig']['Dns']:
                self.options['kv'].append(
                    {"--dns": d}
                )
        ## --dns-option
        if self.inspect['HostConfig']['DnsOptions']:
            for d in self.inspect['HostConfig']['DnsOptions']:
                self.options['kv'].append(
                    {"--dns-option": d}
                )

        ## --dns-search
        if self.inspect['HostConfig']['DnsSearch']:
            for d in self.inspect['HostConfig']['DnsSearch']:
                self.options['kv'].append(
                    {"--dns-search": d}
                )


        ## --domainname
        if self.inspect['Config']['Domainname']:
            self.options['kv'].append(
                {"--domainname": self.inspect['Config']['Domainname']}
            )

        ## --user , -u
        if self.inspect['Config']['User']:
            self.options['kv'].append(
                {"--user": self.inspect['Config']['User']}
            )

        ## --add-host
        if self.inspect['HostConfig']['ExtraHosts']:
            for h in self.inspect['HostConfig']['ExtraHosts']:
                self.options['kv'].append(
                    {"--add-host=": h}
                )

        ## --volume-driver
        if self.inspect['HostConfig']['VolumeDriver']:
            self.options['kv'].append(
                {"--volume-driver": self.inspect['HostConfig']['VolumeDriver']}
            )

        ## --uts
        if self.inspect['HostConfig']['UTSMode']:
            self.options['kv'].append(
                {"--uts": self.inspect['HostConfig']['UTSMode']}
            )

        ## --userns
        if self.inspect['HostConfig']['UsernsMode']:
            self.options['kv'].append(
                {"--uts": self.inspect['HostConfig']['UsernsMode']}
            )

        ## --shm-size, Size of /dev/shm default is 64MB(67108864 byte).
        if self.inspect['HostConfig']['ShmSize'] != 67108864:
            self.options['kv'].append(
                {"--shm-size": unit_converter(self.inspect['HostConfig']['ShmSize'])}
            )

        ## --link. 用于连接其它容器。是比较老旧的技术，可以把要通行的几个容器连接到同一个单独的网络 来替代
        if self.inspect['HostConfig']['Links']:  # self.inspect['HostConfig']['Links'] 为null或[]
            for i in self.inspect['HostConfig']['Links']:
                self.options['kv'].append(
                    {"--add-host=": i}
                )

        ## --ipc
        if self.inspect['HostConfig']['IpcMode'] != "private":
            self.options['kv'].append(
                {"--ipc":self.inspect['HostConfig']['IpcMode']}
            )

        # options  --end

        # command and args
        # 如果 self.inspect['Config']['Cmd'] 与 self.inspect_image['Config']['Cmd'] 不相同，说明docker run传参数了。
        if self.inspect['Config']['Cmd'] and (self.inspect['Config']['Cmd'] != self.inspect_image['Config']['Cmd']):
            for c in self.inspect['Config']['Cmd']:
                self.args.append(c)

    @staticmethod
    def help_msg():
        _MSG = """Usage:
# Command alias
echo "alias get_run_command='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock cucker/get_command_4_run_container'" >> ~/.bashrc
. ~/.bashrc

# Excute command
get_run_command <CONTAINER>
"""
        print(_MSG)

    def start(self):
        self._get_inspect_container()
        self._get_inspect_image()
        self._parse_inspect_container()
        self._print_docker_run_cmd()

if __name__ == '__main__':
    if len(argv) < 2 or argv[1] == "--help":
        MYDOCKER.help_msg()
        exit(1)

    mydocker = MYDOCKER()
    ret = mydocker.start()
