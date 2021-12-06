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
