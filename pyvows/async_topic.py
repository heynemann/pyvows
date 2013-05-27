# -*- coding: utf-8 -*-
'''Implementation for `Vows.async_topic` decorator. (See `core`
module).

'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys

#-------------------------------------------------------------------------------------------------


class VowsAsyncTopic(object):
    #   FIXME: Add Docstring
    def __init__(self, func, args, kw):
        self.func = func
        self.args = args
        self.kw = kw

    def __call__(self, callback):
        args = (self.args[0], callback,) + self.args[1:]
        try:
            self.func(*args, **self.kw)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            callback(exc_type, exc_value, exc_traceback)


class VowsAsyncTopicValue(object):
    #   FIXME: Add Docstring
    def __init__(self, args, kw):
        self.args = args
        self.kw = kw
        self.error = None
        if len(self.args) >= 1 and isinstance(self.args[0], Exception):
            self.error = self.args

    def __getitem__(self, attr):
        if type(attr) is int:
            return self.args[attr]

        if attr in self.kw:
            return self.kw[attr]

        raise AttributeError

    def __getattr__(self, attr):
        if attr in self.kw:
            return self.kw[attr]

        if hasattr(self, attr):
            return self.attr

        raise AttributeError
