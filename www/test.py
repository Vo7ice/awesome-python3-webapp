#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test
"""
import asyncio
import time
import uuid
import logging

import orm
from models import User

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


def test_save(loop):
    yield from orm.create_pool(loop=loop, host='localhost', port='3306', user='www-data', password='www-data',
                               db='awesome')
    u = User(name='Test', email='test@example.com', passwd='123456', image='about:blank')
    res = yield from u.save()
    return res


def test_find():
    yield from orm.create_pool(user='www-data', password='www-data', database='awesome')
    use = yield from User.findAll()
    return use


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_save(loop))
    loop.close()
