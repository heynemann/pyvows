# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows.async_topic import VowsAsyncTopic

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
    
    
def _batch(method):
    # This is underscored-prefixed because the only intended use is via 
    # `Vows.batch`.  Also, `Vows.batch` expands on this core implementation.
    def method_name(*args, **kw):
        method(*args, **kw)

    return method_name