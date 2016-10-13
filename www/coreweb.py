#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import logging
import asyncio
import inspect
import os

from os import path

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'


# 在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）
# Python内置的functools.wraps可以把原始函数的__name__等属性复制到wrapper()函数中.否则,有些依赖函数签名的代码执行就会出错.
# 代码执行顺序
# 首先执行get('path'),返回的是decorator函数,再调用返回的函数,参数是目标函数,返回值最终是wrapper函数.

# get方法
def get(path):
    """
    define decorator @get('/path')
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.info('%s %s():' % (path, func.__name__))
            return func(*args, **kwargs)

        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator


# post方法
def post(path):
    """
    define decorator @get('/path')
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.info('%s %s():' % (path, func.__name__))
            return func(*args, **kwargs)

        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper

    return decorator


# `RequestHandler`是一个类,由于定义了`__call__()`方法，因此可以将其实例视为函数.
class RequestHandler(object):
    def __init__(self, app, fn):
        self.app = app
        self._func = fn

    @asyncio.coroutine
    def __call__(self, request):
        kw = None  # 获取参数
        r = yield from self._func(**kw)
        return r

    def add_static(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        self.app.router.add_static('/static/', file_path)
        logging.info('add static %s ===> %s' % ('/static/', file_path))

    # 用来注册一个URL处理函数：
    def add_route(self, fn):
        method = getattr(fn, '__method__', None)
        path = getattr(fn, '__route__', None)
        if path is None or method is None:
            raise ValueError('@get or @post not define in %s' % str(fn))
        if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
            fn = asyncio.coroutine(fn)
        logging.info('add route %s %s ===> %s(%s)' % (
            method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
        self.app.router.add_route(method, path, RequestHandler(self.app, fn))

    # 自动把handler模块的所有符合条件的函数注册了
    def add_routes(self, module_name):
        n = module_name.rfind('.')
        if n == (-1):
            mod = __import__(module_name, globals(), locals())
        else:
            name = module_name[n + 1:]
            mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
            fn = getattr(mod, attr)
            if callable(fn):
                method = getattr(fn, '__method__', None)
                path = getattr(fn, '__route__', None)
                if method and path:
                    self.add_route(self.app, fn)
