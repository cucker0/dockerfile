#!/usr/bin/env python

"""
author: song yanlin
mail: hanxiao2100@qq.com
"""

# Example for a service inspect of stack
# api_client.inspect_service('mywp_db'):

inspect = \
{
    'ID': 'jai92yssyscu1mf4g3scnz0uz',
    'Version': {'Index': 2310},
    'CreatedAt': '2021-12-05T08:59:56.733999767Z',
    'UpdatedAt': '2021-12-06T03:19:09.506777478Z',
    'Spec': {
        'Name': 'mywp_db',
        'Labels': {
            'com.docker.stack.image': 'mysql:latest',
            'com.docker.stack.namespace': 'mywp'
        },
        'TaskTemplate': {
            'ContainerSpec': {
                'Image': 'mysql:latest@sha256:ff9a288d1ecf4397967989b5d1ec269f7d9042a46fc8bc2c3ae35458c1a26727',
                'Labels': {'com.docker.stack.namespace': 'mywp'},
                'Env': [
                    'MYSQL_DATABASE=wordpress',
                    'MYSQL_PASSWORD_FILE=/run/secrets/wordpress_db_password',
                    'MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_root_password',
                    'MYSQL_USER=wordpress'
                ],
                'Privileges': {
                    'CredentialSpec': None,
                    'SELinuxContext': None
                },
                'Mounts': [
                    {
                        'Type': 'volume',
                        'Source': 'mywp_db_data',
                        'Target': '/var/lib/mysql',
                        'VolumeOptions': {
                            'Labels': {
                                'com.docker.stack.namespace': 'mywp'
                            }
                        }
                    }
                ],
                'Secrets': [
                    {
                        'File': {
                            'Name': 'db_root_password',
                            'UID': '0',
                            'GID': '0',
                            'Mode': 292
                        },
                        'SecretID': 'jbu8gk3podn3suae0p82knivk',
                        'SecretName': 'mywp_db_root_password'
                    },
                    {
                        'File': {
                            'Name': 'wordpress_db_password',
                            'UID': '0', 'GID': '0',
                            'Mode': 292
                        },
                        'SecretID': 'xjrq6acqaidy0sidh27nkeiju',
                        'SecretName': 'mywp_wordpress_db_password'
                    }
                ],
                'Isolation': 'default'
            },
            'Resources': {},
            'Placement': {
                'Platforms': [
                    {
                        'Architecture': 'amd64',
                        'OS': 'linux'
                    }
                ]
            },
            'Networks': [
                {
                    'Target': 'iv80de1gyydkxxzskd3rkpg37',
                    'Aliases': ['db']
                }
            ],
            'ForceUpdate': 0,
            'Runtime': 'container'
        },
        'Mode': {
            'Replicated': {'Replicas': 1}
        },
        'EndpointSpec': {'Mode': 'vip'}
    },
    'PreviousSpec': {
        'Name': 'mywp_db',
        'Labels': {
            'com.docker.stack.image': 'mysql:latest',
            'com.docker.stack.namespace': 'mywp'
        },
        'TaskTemplate': {
            'ContainerSpec': {
                'Image': 'mysql:latest@sha256:ff9a288d1ecf4397967989b5d1ec269f7d9042a46fc8bc2c3ae35458c1a26727',
                'Labels': {'com.docker.stack.namespace': 'mywp'},
                'Env': [
                    'MYSQL_DATABASE=wordpress',
                    'MYSQL_PASSWORD_FILE=/run/secrets/wordpress_db_password',
                    'MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_root_password',
                    'MYSQL_USER=wordpress'
                ],
                'Privileges': {
                    'CredentialSpec': None,
                    'SELinuxContext': None
                },
                'Mounts': [
                    {
                        'Type': 'volume',
                        'Source': 'mywp_db_data',
                        'Target': '/var/lib/mysql',
                        'VolumeOptions': {
                            'Labels': {'com.docker.stack.namespace': 'mywp'}
                        }
                    }
                ],
                'Secrets': [
                    {
                        'File': {
                            'Name': 'db_root_password',
                            'UID': '0', 'GID': '0',
                            'Mode': 292
                        },
                        'SecretID': 'jbu8gk3podn3suae0p82knivk',
                        'SecretName': 'mywp_db_root_password'
                    },
                    {'File': {
                        'Name': 'wordpress_db_password',
                        'UID': '0', 'GID': '0',
                        'Mode': 292},
                        'SecretID': 'xjrq6acqaidy0sidh27nkeiju',
                        'SecretName': 'mywp_wordpress_db_password'
                    }
                ],
                'Isolation': 'default'
            },
            'Resources': {},
            'Placement': {
                'Platforms': [
                    {'Architecture': 'amd64', 'OS': 'linux'}
                ]
            },
            'Networks': [
                {
                    'Target': 'iv80de1gyydkxxzskd3rkpg37',
                    'Aliases': ['db']
                }
            ],
            'ForceUpdate': 0,
            'Runtime': 'container'
        },
        'Mode': {
            'Replicated': {'Replicas': 1}
        },
        'EndpointSpec': {'Mode': 'vip'}
    },
    'Endpoint': {
        'Spec': {'Mode': 'vip'},
        'VirtualIPs': [
            {
                'NetworkID': 'iv80de1gyydkxxzskd3rkpg37',
                'Addr': '10.0.3.5/24'
            }
        ]
    }
}


inspect2 = \
[
    {
        "ID": "dg3vntk1qqmpu1wf28ojqc57v",
        "Version": {
            "Index": 2323
        },
        "CreatedAt": "2021-12-05T08:59:51.918258395Z",
        "UpdatedAt": "2021-12-06T03:19:24.045643745Z",
        "Spec": {
            "Name": "mywp_wordpress",
            "Labels": {
                "com.docker.stack.image": "wordpress:latest",
                "com.docker.stack.namespace": "mywp"
            },
            "TaskTemplate": {
                "ContainerSpec": {
                    "Image": "wordpress:latest@sha256:7ac56e4299c1e71062be5dc8e9ace8ec7c891f5d50f2d0f4c0907fe403187d53",
                    "Labels": {
                        "com.docker.stack.namespace": "mywp"
                    },
                    "Env": [
                        "WORDPRESS_DB_HOST=db:3306",
                        "WORDPRESS_DB_NAME=wordpress",
                        "WORDPRESS_DB_PASSWORD_FILE=/run/secrets/wordpress_db_password",
                        "WORDPRESS_DB_USER=wordpress"
                    ],
                    "Privileges": {
                        "CredentialSpec": null,
                        "SELinuxContext": null
                    },
                    "Mounts": [
                        {
                            "Type": "volume",
                            "Source": "mywp_wordpress_data",
                            "Target": "/var/www/html",
                            "VolumeOptions": {
                                "Labels": {
                                    "com.docker.stack.namespace": "mywp"
                                }
                            }
                        }
                    ],
                    "StopGracePeriod": 10000000000,
                    "DNSConfig": {},
                    "Secrets": [
                        {
                            "File": {
                                "Name": "wordpress_db_password",
                                "UID": "0",
                                "GID": "0",
                                "Mode": 292
                            },
                            "SecretID": "xjrq6acqaidy0sidh27nkeiju",
                            "SecretName": "mywp_wordpress_db_password"
                        }
                    ],
                    "Isolation": "default"
                },
                "Resources": {},
                "RestartPolicy": {
                    "Condition": "any",
                    "Delay": 5000000000,
                    "MaxAttempts": 0
                },
                "Placement": {
                    "Platforms": [
                        {
                            "Architecture": "amd64",
                            "OS": "linux"
                        },
                        {
                            "OS": "linux"
                        },
                        {
                            "OS": "linux"
                        },
                        {
                            "Architecture": "arm64",
                            "OS": "linux"
                        },
                        {
                            "Architecture": "386",
                            "OS": "linux"
                        },
                        {
                            "Architecture": "mips64le",
                            "OS": "linux"
                        },
                        {
                            "Architecture": "ppc64le",
                            "OS": "linux"
                        },
                        {
                            "Architecture": "s390x",
                            "OS": "linux"
                        }
                    ]
                },
                "Networks": [
                    {
                        "Target": "iv80de1gyydkxxzskd3rkpg37",
                        "Aliases": [
                            "wordpress"
                        ]
                    }
                ],
                "ForceUpdate": 0,
                "Runtime": "container"
            },
            "Mode": {
                "Replicated": {
                    "Replicas": 1
                }
            },
            "UpdateConfig": {
                "Parallelism": 1,
                "FailureAction": "pause",
                "Monitor": 5000000000,
                "MaxFailureRatio": 0,
                "Order": "stop-first"
            },
            "RollbackConfig": {
                "Parallelism": 1,
                "FailureAction": "pause",
                "Monitor": 5000000000,
                "MaxFailureRatio": 0,
                "Order": "stop-first"
            },
            "EndpointSpec": {
                "Mode": "vip",
                "Ports": [
                    {
                        "Protocol": "tcp",
                        "TargetPort": 80,
                        "PublishedPort": 5600,
                        "PublishMode": "ingress"
                    }
                ]
            }
        },
        "PreviousSpec": {
            "Name": "mywp_wordpress",
            "Labels": {
                "com.docker.stack.image": "wordpress:latest",
                "com.docker.stack.namespace": "mywp"
            },
            "TaskTemplate": {
                "ContainerSpec": {
                    "Image": "wordpress:latest@sha256:7ac56e4299c1e71062be5dc8e9ace8ec7c891f5d50f2d0f4c0907fe403187d53",
                    "Labels": {
                        "com.docker.stack.namespace": "mywp"
                    },
                    "Env": [
                        "WORDPRESS_DB_HOST=db:3306",
                        "WORDPRESS_DB_NAME=wordpress",
                        "WORDPRESS_DB_PASSWORD_FILE=/run/secrets/wordpress_db_password",
                        "WORDPRESS_DB_USER=wordpress"
                    ],
                    "Privileges": {
                        "CredentialSpec": null,
                        "SELinuxContext": null
                    },
                    "Mounts": [
                        {
                            "Type": "volume",
                            "Source": "mywp_wordpress_data",
                            "Target": "/var/www/html",
                            "VolumeOptions": {
                                "Labels": {
                                    "com.docker.stack.namespace": "mywp"
                                }
                            }
                        }
                    ],
                    "Secrets": [
                        {
                            "File": {
                                "Name": "wordpress_db_password",
                                "UID": "0",
                                "GID": "0",
                                "Mode": 292
                            },
                            "SecretID": "xjrq6acqaidy0sidh27nkeiju",
                            "SecretName": "mywp_wordpress_db_password"
                        }
                    ],
                    "Isolation": "default"
                },
                "Resources": {},
                "Placement": {
                    "Platforms": [
                        {
                            "Architecture": "amd64",
                            "OS": "linux"
                        },
                        {
                            "OS": "linux"
                        },
                        {
                            "OS": "linux"
                        },
                        {
                            "Architecture": "arm64",
                            "OS": "linux"
                        },
                        {
                            "Architecture": "386",
                            "OS": "linux"
                        },
                        {
                            "Architecture": "mips64le",
                            "OS": "linux"
                        },
                        {
                            "Architecture": "ppc64le",
                            "OS": "linux"
                        },
                        {
                            "Architecture": "s390x",
                            "OS": "linux"
                        }
                    ]
                },
                "Networks": [
                    {
                        "Target": "iv80de1gyydkxxzskd3rkpg37",
                        "Aliases": [
                            "wordpress"
                        ]
                    }
                ],
                "ForceUpdate": 0,
                "Runtime": "container"
            },
            "Mode": {
                "Replicated": {
                    "Replicas": 1
                }
            },
            "EndpointSpec": {
                "Mode": "vip",
                "Ports": [
                    {
                        "Protocol": "tcp",
                        "TargetPort": 80,
                        "PublishedPort": 5000,
                        "PublishMode": "ingress"
                    }
                ]
            }
        },
        "Endpoint": {
            "Spec": {
                "Mode": "vip",
                "Ports": [
                    {
                        "Protocol": "tcp",
                        "TargetPort": 80,
                        "PublishedPort": 5600,
                        "PublishMode": "ingress"
                    }
                ]
            },
            "Ports": [
                {
                    "Protocol": "tcp",
                    "TargetPort": 80,
                    "PublishedPort": 5600,
                    "PublishMode": "ingress"
                }
            ],
            "VirtualIPs": [
                {
                    "NetworkID": "f6qb2d6rlokau6z5ae0kwhw58",
                    "Addr": "10.0.0.188/24"
                },
                {
                    "NetworkID": "iv80de1gyydkxxzskd3rkpg37",
                    "Addr": "10.0.3.2/24"
                }
            ]
        },
        "UpdateStatus": {
            "State": "completed",
            "StartedAt": "2021-12-06T03:19:13.330784899Z",
            "CompletedAt": "2021-12-06T03:19:24.045614877Z",
            "Message": "update completed"
        }
    }
]
