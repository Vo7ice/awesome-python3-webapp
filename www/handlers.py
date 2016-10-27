#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import hashlib
import json
import logging

import time

import re

from aiohttp import web

import markdown2
from config import configs
from errors import APIValueError, APIError, APIPermissionError
from models import User, Blog, next_id, Comment
from coreweb import get, post
from apis import Page, UserInfo

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'

'url handlers'

COOKIE_NAME = 'awession'
_COOKIE_KEY = configs.session.secret


@get('/')
@asyncio.coroutine
def index(*, page='1'):  # 需要变长参数或关键字参数 找到原因了
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
        'page': get_page_index(page),
        'blogs': blogs
    }


# 检查权限
# 是否登录或是管理员
def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        logging.info('U R not allow to create blogs!')
        raise APIPermissionError()


# 获取page的页数
def get_page_index(page):
    p = 1

    try:
        p = int(page)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


# 新建blog
@post('/api/blogs')
@asyncio.coroutine
def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name can`t be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary can`t be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content can`t be empty.')
    logging.info('args is okay!')

    blog = Blog(user_id=request.__user__.id,
                user_name=request.__user__.name,
                user_image=request.__user__.image,
                name=name.strip(),
                summary=summary.strip(),
                content=content.strip())
    yield from blog.save()
    return blog


@get('/blog/{id}')
@asyncio.coroutine
def api_get_blog(*, id):
    blog = yield from Blog.find(id)
    comments = yield from Comment.findAll(where='blog_id = ?', args=blog.id, orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }


@get('/api/blogs')
@asyncio.coroutine
def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = yield from Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


@get('/api/users')
@asyncio.coroutine
def api_users(*, page='1'):
    page_index = get_page_index(page)
    num = yield from User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, userInfos=())
    users = yield from User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    userInfos = []
    for u in users:
        blogs = yield from Blog.findAll(where='user_id = ?', args=[u.id])
        comments = yield from Comment.findAll(where='user_id = ?', args=[u.id])
        userInfo = UserInfo(u, blogs, comments)
        userInfos.append(userInfo)
    return dict(page=p, userInfos=userInfos)


# 新增blog
@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }


@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


@get('/manage/users')
def manage_users(*, page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }


@get('/manage/comments')
def manage_comments(*, page='1'):
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page)
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


# @get('/api/users')
# @asyncio.coroutine
# def api_get_users():
#     users = yield from User.findAll()
#     for u in users:
#         u.passwd = '******'
#     return dict(users=users)


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


@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-delete-', max_age=0, httponly=True)
    logging.info('user sign out')
    return r


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
        logging.info('not eaqual user.passwd:%s , sha1.hexdigest:%s' % (user.passwd, sha1.hexdigest()))
        raise APIValueError('passwd', 'Invalid password')
    # 验证通过 设置cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r
