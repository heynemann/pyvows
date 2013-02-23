# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from functools import wraps
import re

from pyvows.async_topic import VowsAsyncTopic
from pyvows.errors import VowsAssertionError


def _batch(method):
    # This is underscored-prefixed because the only intended use (via
    # `@Vows.batch`) expands on this core functionality
    def method_name(*args, **kw):
        method(*args, **kw)
    return method_name


def _assertion(method, assertion_obj):
    # This is underscored-prefixed because the only intended use (via
    # `@Vows.assertion`) expands on this core functionality

    def method_name(*args, **kw):
        method(*args, **kw)

    def exec_assertion(*args, **kw):
        return method_name(*args, **kw)

    setattr(assertion_obj, method.__name__, exec_assertion)
    return method_name


def _create_assertions(method, assertion_obj):
    # This is underscored-prefixed because the only intended use (via
    # `@Vows.create_assertions`) expands on this core functionality

    humanized_method_name = re.sub(r'_+', ' ', method.__name__)

    def _assertion_msg(assertion_clause=None, *args):
        raw_msg = 'Expected topic({{0}}) {assertion_clause}'.format(
            assertion_clause=assertion_clause)
        if len(args) is 2:
            raw_msg += ' {1}'
        return raw_msg

    def exec_assertion(*args):
        raw_msg = _assertion_msg(humanized_method_name, *args)
        if not method(*args):
            raise VowsAssertionError(raw_msg, *args)

    def exec_not_assertion(*args):
        raw_msg = _assertion_msg('not {0}'.format(humanized_method_name), *args)
        if method(*args):
            raise VowsAssertionError(raw_msg, *args)

    setattr(assertion_obj, method.__name__, exec_assertion)
    setattr(assertion_obj, 'not_{method.__name__}'.format(
        method=method),
        exec_not_assertion)

    def wrapper(*args, **kw):
        return method(*args, **kw)

    return wrapper


def async_topic(topic):
    '''Topic decorator.  Allows PyVows testing of asynchronous topics.

    Use `@Vows.async_topic` on your `topic` method to mark it as
    asynchronous.  This allows PyVows to test topics which use callbacks
    instead of return values.

    '''
    def wrapper(*args, **kw):
        return VowsAsyncTopic(topic, args, kw)
    wrapper._original = topic
    wrapper.__name__ = topic.__name__
    return wrapper


class FunctionWrapper(object):
    '''Function decorator.  Simply calls the decorated function when all
    the wrapped functions have been called.

    '''
    def __init__(self, func):
        self.waiting = 0
        self.func = func

    def wrap(self, method):
        self.waiting += 1

        @wraps(method)
        def wrapper(*args, **kw):
            try:
                ret = method(*args, **kw)
                return ret
            finally:
                self.waiting -= 1
                self()

        wrapper._original = method
        return wrapper

    def __call__(self):
        if self.waiting == 0:
            self.func()
