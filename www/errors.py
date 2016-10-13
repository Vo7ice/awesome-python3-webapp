#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'


class APIError(Exception):
    """
    the base APIError which contains error(required),data(optional) and message(optional)
    """

    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message
