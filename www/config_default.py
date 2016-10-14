#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.INFO)

"""
Default Configurations
"""

__author__ = 'Vo7ice'

configs = {
    'debug': True,
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'Vo7ice',
        'password': 'passwd',
        'db': 'awesome'
    },
    'session': {
        'secret': 'AwEsOmE'
    }
}
