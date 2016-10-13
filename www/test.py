#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test
"""
import asyncio
import time
import uuid
import logging

import aiomysql
import pymysql

import orm
from models import User

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


def test_save(in_loop):
    yield from orm.create_pool(loop=in_loop, host='127.0.0.1', user='Vo7ice', password='passwd',
                               db='awesome')
    u = User(name='Test', email='test@example.com', passwd='123456', image='about:blank')
    res = yield from u.save()
    yield from orm.destroy_pool()
    return res
    # pool = yield from aiomysql.create_pool(host='127.0.0.1',
    #                                        port=3306,
    #                                        user='Vo7ice',
    #                                        password='passwd',
    #                                        db='awesome',
    #                                        charset='utf8',
    #                                        autocommit=True,
    #                                        maxsize=10,
    #                                        minsize=1,
    #                                        loop=in_loop)
    # with (yield from pool) as conn:
    #     cur = yield from conn.cursor()
    #     u = User(name='Test', email='test@example.com', passwd='123456', image='about:blank')
    #     args = list(map(u.getValueOrDefault, u.__fields__))
    #     args.append(u.getValueOrDefault(u.__primary_key__))
    #     yield from cur.execute(u.__insert__.replace('?', '%s'), args)
    #     yield from cur.close()
    #     yield from conn.commit()
    # pool.close()
    # yield from pool.wait_closed()


def test_find(in_loop):
    yield from orm.create_pool(loop=in_loop, host='127.0.0.1', user='Vo7ice', password='passwd',
                               db='awesome')
    users = yield from User.findAll(orderBy='created_at')

    for u in users:
        logging.info('name %s,passwd %s,email %s' % (u.name, u.passwd, u.email))
    user = users[0]
    user.passwd = '000000'
    user.email = '11111@qq.com'
    yield from user.remove()

    yield from orm.destroy_pool()


def test_update(in_loop, user):
    yield from orm.create_pool(loop=in_loop, host='127.0.0.1', user='Vo7ice', password='passwd',
                               db='awesome')
    user.passwd = '000000'
    user.updateItem()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_find(loop))
    loop.close()
    # conn = pymysql.connect(host='127.0.0.1', port=3306,
    #                        user='root', password='',
    #                        db='mysql')
    # logging.info('link end...')
    # cur = conn.cursor()
    # cur.execute("SELECT Host,User FROM user;")
