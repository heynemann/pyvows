#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows function assertions.  For use with `expect()` (see `pyvows.core`).
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import inspect

from pyvows import Vows, VowsAssertionError


@Vows.assertion
def to_be_a_function(topic):
    '''Asserts that `topic` is a function.'''
    if not (inspect.ismethod(topic) or inspect.isfunction(topic)):
        raise VowsAssertionError('Expected topic({0}) to be a function or a method, but it was a {1}', topic, topic.__class__)


@Vows.assertion
def not_to_be_a_function(topic):
    '''Asserts that `topic` is NOT a function.'''
    if inspect.ismethod(topic) or inspect.isfunction(topic):
        raise VowsAssertionError('Expected topic({0}) not to be a function or a method', topic)
