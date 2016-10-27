#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'


class Page(object):
    """
    页码,用作分页
    """

    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (page_index > self.item_count):
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item count: %s, page_count: %s, page_size: %s, offset: %s, limit: %s' \
               % (self.item_count, self.page_count, self.page_size, self.offset, self.limit)

    __repr__ = __str__


class UserInfo(object):
    """
    用户信息,管理用户
    """

    def __init__(self, user, blogs, comments):
        self.user = user
        if blogs:
            self.blogs_num = len(blogs)
        else:
            self.blogs_num = 0
        if comments:
            self.comments_num = len(comments)
        else:
            self.comments_num = 0

    def __str__(self):
        return 'user name:%s, blogs_num:%d, comments_num:%d' % (self.user.name, self.blogs_num, self.comments_num)

    __repr__ = __str__
