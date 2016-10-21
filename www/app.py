#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import os
import time
import orm

from datetime import datetime
from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from config import configs
from coreweb import add_routes, add_static
from handlers import COOKIE_NAME, cookie2user

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'

'''
async web application
'''


def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html', charset='utf-8')


# jinja初始化函数
def init_jinja2(app, **kwargs):
    logging.info('init jinja2...')
    # 设置
    options = dict(
        autoescape=kwargs.get('autoescape', True),
        block_start_string=kwargs.get('block_start_string', '{%'),
        block_end_string=kwargs.get('block_end_string', '%}'),
        variable_start_string=kwargs.get('variable_start_string', '{{'),
        variable_end_string=kwargs.get('variable_end_string', '}}'),
        auto_reload=kwargs.get('auto_reload', True)
    )
    # 从参数获取路径
    path = kwargs.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path:%s' % path)
    # 设置jinja2的环境
    env = Environment(loader=FileSystemLoader(path), **options)
    # 从参数获取拦截器
    filters = kwargs.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env


# -------------------------工厂函数------------------------------------
# 在每个响应之前打印日志
# 处理log的工厂函数
@asyncio.coroutine
def logger_factory(app, handler):
    @asyncio.coroutine
    def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        return (yield from handler(request))

    return logger


# 登录的时候验证cookie
@asyncio.coroutine
def auth_factory(app, handler):
    @asyncio.coroutine
    def auth(request):
        logging.info('check user: %s, %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        logging.info('cookie_str,%s' % cookie_str)
        if cookie_str:
            user = yield from cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                request.__user__ = user
        # 是否已经登录
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFound('/signin')

        return (yield from handler(request))  # 没有cookie需要返回

    return auth


# 处理请求数据的工厂函数
@asyncio.coroutine
def data_factory(app, handler):
    @asyncio.coroutine
    def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = yield from request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = yield from request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (yield from handler(request))

    return parse_data


# 处理返回结果的工厂函数
@asyncio.coroutine
def response_factory(app, handler):
    @asyncio.coroutine
    def response(request):
        logging.info('Response handler...')
        r = yield from handler(request)
        # 结果为媒体文件
        if isinstance(r, web.StreamResponse):
            return r
        # 结果为字节
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        # 结果为网页
        if isinstance(r, str):
            # 重新请求重定向的url
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        # 结果是字典的json
        if isinstance(r, dict):
            template = r.get('__template__')
            logging.info('template %s' % template)
            if template is None:
                resp = web.Response(
                    body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = web.Response(
                    body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))  # 需要templating关键字
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        # 状态码
        if isinstance(r, int) and 100 <= r <= 600:
            return web.Response(status=r)
        # 状态码和消息
        if isinstance(r, tuple) and 2 == len(r):
            status, message = r
            if isinstance(status, int) and 100 <= status <= 600:
                return web.Response(status=status, text=str(message))
        # default 默认结果
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp

    return response


# 格式化时间戳
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s 小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s 天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


@asyncio.coroutine
def init(loop):
    yield from orm.create_pool(loop=loop, **configs.db)
    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, data_factory, response_factory
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000....')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
