#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging

from models import User
from coreweb import get

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'

'url handlers'


@get('/')
@asyncio.coroutine
def index(request): # 需要变长参数或关键字参数 找到原因了
    users = yield from User.findAll()
    logging.info('users len %d' % len(users))
    return {
        '__template__': 'test.html',
        'users': users
    }
