#!/usr/bin/env python

"""
author: song yanlin
mail: hanxiao2100@qq.com
"""

# Example for a service inspect
# api_client.inspect_service('my_web'):
inspect = \
{
    'ID': 't68zx22fl71i54i671wwzpt7o',
    'Version': {'Index': 1398},
    'CreatedAt': '2021-11-30T09:59:52.737880718Z',
    'UpdatedAt': '2021-12-02T09:44:44.575650612Z',
    'Spec': {
        'Name': 'my_web',
        'Labels': {},
        'TaskTemplate': {
            'ContainerSpec': {
                'Image': 'cucker/httpd:latest@sha256:c3a4a82936a6fa92b923f8a590e84a3977bb8b8024c5a9a7dd9708990eb49b3b',
                'Init': False,
                'DNSConfig': {},
                'Isolation': 'default'
            },
            'Resources': {
                'Limits': {},
                'Reservations': {}
            },
            'Placement': {
                'Platforms': [
                    {'Architecture': 'amd64', 'OS': 'linux'}
                ]
            },
            'Networks': [
                {'Target': 'ub74xvfpp0co6nx5qdfaa7w2f'}
            ],
            'ForceUpdate': 0,
            'Runtime': 'container'
        },
        'Mode': {
            'Replicated': {'Replicas': 3}
        },
        'EndpointSpec': {
            'Mode': 'vip'
        }
    },
    'Endpoint': {
        'Spec': {
            'Mode': 'vip'
        },
        'VirtualIPs': [
            {
                'NetworkID': 'ub74xvfpp0co6nx5qdfaa7w2f',
                'Addr': '10.0.1.11/24'
            }
        ]
    }
}