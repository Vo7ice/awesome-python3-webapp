#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging

import time

from models import User, Blog
from coreweb import get, post

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'

'url handlers'


@get('/')
@asyncio.coroutine
def index(request):  # 需要变长参数或关键字参数 找到原因了
    # users = yield from User.findAll()
    # logging.info('users len %d' % len(users))
    # return {
    #     '__template__': 'test.html',
    #     'users': users
    # }
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time() - 120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time() - 7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }
