# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from functools import wraps

from pyvows.async_topic import VowsAsyncTopic
from pyvows.runner import SkipTest

#-------------------------------------------------------------------------------------------------


def _batch(klass):
    # This is underscored-prefixed because the only intended use (via
    # `@Vows.batch`) expands on this core functionality
    def klass_name(*args, **kw):
        klass(*args, **kw)
    return klass_name


def async_topic(topic):
    '''Topic decorator.  Allows PyVows testing of asynchronous topics.

    Use `@Vows.async_topic` on your `topic` method to mark it as
    asynchronous.  This allows PyVows to test topics which use callbacks
    instead of return values.

    '''
    def wrapper(*args, **kw):
        return VowsAsyncTopic(topic, args, kw)
    wrapper._original = topic
    wrapper._wrapper_type = 'async_topic'
    wrapper.__name__ = topic.__name__
    return wrapper


def capture_error(topic_func):
    '''Topic decorator.  Allows any errors raised to become the topic value.

    By default, errors raised in topic functions are reported as
    errors. But sometimes you want the error to be the topic value, in
    which case decorate the topic function with this decorator.'''
    def wrapper(*args, **kw):
        try:
            return topic_func(*args, **kw)
        except Exception as e:
            return e
    wrapper._original = topic_func
    wrapper._wrapper_type = 'capture_error'
    wrapper.__name__ = topic_func.__name__
    return wrapper


def skip_if(condition, reason):
    '''Topic or vow or context decorator.  Causes a topic or vow to be skipped if `condition` is True

    This is equivilent to `if condition: raise SkipTest(reason)`
    '''
    from pyvows.core import Vows

    def real_decorator(topic_or_vow_or_context):
        if not condition:
            return topic_or_vow_or_context

        if type(topic_or_vow_or_context) == type(Vows.Context):
            class klass_wrapper(topic_or_vow_or_context):
                def topic(self):
                    raise SkipTest(reason)
            klass_wrapper.__name__ = topic_or_vow_or_context.__name__
            return klass_wrapper
        else:
            def wrapper(*args, **kwargs):
                raise SkipTest(reason)
            wrapper.__name__ = topic_or_vow_or_context.__name__
            return wrapper
    return real_decorator

#-------------------------------------------------------------------------------------------------


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
