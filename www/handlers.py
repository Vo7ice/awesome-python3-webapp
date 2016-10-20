#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import hashlib
import json
import logging

import time

import re

from aiohttp import web

from config import configs
from errors import APIValueError, APIError
from models import User, Blog, next_id
from coreweb import get, post

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'

'url handlers'

COOKIE_NAME = 'awession'
_COOKIE_KEY = configs.session.secret


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


# 生成cookie
def user2cookie(user, max_age):
    """
    Generate cookie str by user
    """
    expires = str(int(time.time()) + max_age)
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    l = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(l)


# 解析cookie
@asyncio.coroutine
def cookie2user(cookie_str):
    """
    Parse cookie and load user if cookie is valid
    """
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = yield from User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user

    except Exception as e:
        logging.exception(e)
        return None


@get('/api/users')
@asyncio.coroutine
def api_get_users():
    users = yield from User.findAll()
    for u in users:
        u.passwd = '******'
    return dict(users=users)


@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


_RE_EMAIL = re.compile(r'[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


# 注册用户
@post('/api/user')
@asyncio.coroutine
def api_register_user(*, email, name, passwd):
    if not name or not name.strip():  # 校验名字
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):  # 校验email
        raise APIValueError('email', 'Invalid email')
    if not passwd or not _RE_SHA1.match(passwd):  # 校验password
        raise APIValueError('passwd')
    users = yield from User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid,
                name=name.strip(),
                email=email,
                # sha1加密
                passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
                # sha1加密
                image='http://www.grvatar.com/avatar/%s?d=mm&s=120' % hashlib.sha1(email.encode('utf-8')).hexdigest())
    yield from user.save()
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


# 验证登录
@post('/api/authenticate')
@asyncio.coroutine
def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email')
    if not passwd:
        raise APIValueError('password', 'Invalid password')
    users = yield from User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'email not exsit')
    user = users[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        logging.info('not eaqual user.passwd:%s , sha1.hexdigest:%s' % (user.passwd,sha1.hexdigest()))
        raise APIValueError('passwd', 'Invalid password')
    # 验证通过 设置cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r
