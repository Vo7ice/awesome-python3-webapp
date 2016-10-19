#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import config_default

logging.basicConfig(level=logging.INFO)

"""
Configurations
"""


class Dict(dict):
    """
    Simple dict but support access as x.y style.
    """

    def __init__(self, names=(), values=(), **kwargs):
        super(Dict, self).__init__(**kwargs)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute %s " % item)

    def __setattr__(self, key, value):
        self[key] = value


# 用override的配置覆盖默认配置
def merge(defaults, override):
    r = {}
    for k, v in defaults.items():  # 获取默认设置
        if k in override:  # 如果override有先关配置项,就进行修改
            if isinstance(v, dict):  # 如果还有子配置就递归
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:  # 没有就跳过该项
            r[k] = v
    return r


# 将dict转化为可以x.y形式的Dict
def toDict(d):
    D = Dict()  # 这里为转换后的类名
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


configs = config_default.configs

# 开始覆盖
try:
    import config_override

    configs = merge(configs, config_override.configs)
except ImportError:
    pass

# 转换为Dict类型
configs = toDict(configs)
