#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Models for user, blog, comment
"""
import time
import uuid

from orm import Model, StringField, BooleanField, IntegerField, FloatField, TextField

__author__ = 'Vo7ice'


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(50)')
    create_at = FloatField(default=time.time())


###class Blog(Model):
#    pass


#class Comment(Model):
#   pass

