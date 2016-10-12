#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import aiomysql

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'


# 记录log
def log(sql, args=()):
    logging.info('SQL:%s' % sql)


# 创建连接池
@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),  # 默认host localhost
        port=kw.get('port', 3306),  # 默认端口 3306
        user=kw['user'],  # 用户
        password=kw['password'],  # 密码
        db=kw['db'],  # 数据库
        charset=kw.get('charset', 'utf8'),  # 编码
        autocommit=kw.get('autocommit', True),  # 自动提交
        maxsize=kw.get('maxsize', 10),  # 最高处理事务
        minsize=kw.get('minsize', 1),  # 最低处理事务
        loop=loop  # 事件
    )


# 销毁连接池
@asyncio.coroutine
def destroy_pool():
    logging.info('destroy database connection pool...')
    global __pool
    if __pool is not None:
        __pool.close()
        yield from __pool.wait_closed()


# 搜索语句
@asyncio.coroutine
def select(sql, args, size=None):
    log(sql, args)  # 记录语句
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        if size:  # 如果为数字,就返回符合条件的前几个结果集
            rs = yield from cur.fetchmany(size)
        else:  # 如果没有,就范围所有符合条件的结果集
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs


# 修改语句
@asyncio.coroutine
def execute(sql, args):
    log(sql)  # 记录语句
    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise
        return affected


# 参数补成?
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


# 基类属性
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name  # 列名
        self.column_type = column_type  # 类型
        self.primary_key = primary_key  # 主键
        self.default = default  # 默认值

    def __str__(self):
        return '<%s,%s,%s>' % (self.__class__.__name__, self.column_type, self.name)


# 字符串
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


# 布尔值
class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


# 整数值
class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


# 浮点数值
class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


# Text
class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


# 元类 映射类
class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name  # 表名
        logging.info('found model %s (table: %s)' % (name, tableName))
        mappings = dict()  # 初始化映射
        fields = []  # 初始化属性
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):  # 如果有属性
                logging.info('found mapping: %s ===> %s' % (k, v))
                mappings[k] = v  # 保存映射关系
                if v.primary_key:  # 如果是主键
                    # 找到主键:
                    if primaryKey:
                        raise BaseException('Duplicate primary key for field: %s' % k)
                    primaryKey = k  # 保存主键
                else:
                    fields.append(k)  # 保存属性集
        if not primaryKey:
            raise BaseException('Primary key not found')  # 多重主键会报错
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))  # 将属性增加``
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = tableName  # 表名
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名

        # ------sql语句-------- #
        attrs['__select__'] = 'select `%s`,%s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s,`%s`) values(%s)' % (
            tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s` = ?' % (
            tableName, '. '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaClass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    # 设置这个方法,可以通过对象.attr来访问属性
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    # 获得属性的值
    def getValue(self, key):
        return getattr(self, key, None)

    # 获得属性的值或默认值
    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s : %s' % (key, str(value)))
                setattr(self, key, value)

        return value

    # 根据查询条件查一个实例
    @classmethod
    @asyncio.coroutine
    def find(cls, pk):
        """find object by primary key"""
        rs = yield from select('%s where `%s = ?`' % (cls.__select__, cls.__primaryKey__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    # 根据列名和条件查看数据库有多少条信息
    @classmethod
    @asyncio.coroutine
    def findNumber(cls, selectField, where=None, args=None):
        """find number by select and where"""
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = yield from select('. '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    # 根据条件查询所有结果集
    @classmethod
    @asyncio.coroutine
    def findAll(cls, where=None, args=None, **kwargs):
        """find all objects by where clause"""
        sql = [cls.__select__]
        # where 查询条件
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        # orderBy 排序关键字
        orderBy = kwargs.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        # limit 筛选关键字
        limit = kwargs.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append('limit')
            elif isinstance(limit, tuple) and (len(limit) == 2):
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = yield from select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    # 保存一条数据
    @classmethod
    @asyncio.coroutine
    def save(cls):
        """save object"""
        args = []
        for x in cls.__fields__:
            logging.info('field:%s' % x)
            # res = cls.getValueOrDefault(cls,key=x)
            # args.append(res)
        args = list(map(cls.getValueOrDefault, cls.__fields__))
        args.append(cls.getValueOrDefault(cls.__primary_key__))
        rows = yield from execute('__insert__', args)
        if rows != 1:
            logging.warning('failed to insert record: affected rows:%s' % rows)
        return rows

    # 修改一条数据
    @classmethod
    @asyncio.coroutine
    def updateItem(cls):
        """update object"""
        args = list(map(cls.getValue, cls.__fields__))
        args.append(cls.getValue(cls.__primary_key__))
        rows = yield from execute('__update__', args)
        if rows != 1:
            logging.warning('failed to update record by primary key: affected rows:%s' % rows)

    # 去除一条数据
    @classmethod
    @asyncio.coroutine
    def remove(cls):
        """remove object by primary key"""
        args = [cls.getValue(key=cls.__primary_key__)]
        rows = yield from execute('__delete__', args)
        if rows != 1:
            logging.warning('failed to remove record by primary key: affected rows:%s' % rows)
