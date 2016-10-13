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
    """
        `id` varchar(50) not null,
        `email` varchar(50) not null,
        `passwd` varchar(50) not null,
        `admin` bool not null,
        `name` varchar(50) not null,
        `image` varchar(500) not null,
        `created_at` real not null,
        unique key `idx_email` (`email`),
        key `idx_created_at` (`created_at`),
        primary key (`id`)
    """
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class Blog(Model):
    """
        `id` varchar(50) not null,
        `user_id` varchar(50) not null,
        `user_name` varchar(50) not null,
        `user_image` varchar(500) not null,
        `name` varchar(50) not null,
        `summary` varchar(200) not null,
        `content` mediumtext not null,
        `created_at` real not null,
        key `idx_created_at` (`created_at`),
        primary key (`id`)
    """
    __table__ = 'bolgs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Comment(Model):
    """
       `id` varchar(50) not null,
        `blog_id` varchar(50) not null,
        `user_id` varchar(50) not null,
        `user_name` varchar(50) not null,
        `user_image` varchar(500) not null,
        `content` mediumtext not null,
        `created_at` real not null,
        key `idx_created_at` (`created_at`),
        primary key (`id`)
    """
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField('varchar(50)')
    user_id = StringField('varchar(50)')
    user_name = StringField('varchar(50)')
    user_image = StringField('varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)
