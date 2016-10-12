#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

__author__ = 'Vo7ice'


# get方法
def get(path):
    """
    define decorator @get('/path')
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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
            return func(*args, **kwargs)

        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper

    return decorator
