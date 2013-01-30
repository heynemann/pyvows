#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows instance assertions.  For use with `expect()` (see `pyvows.core`).
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, VowsAssertionError

@Vows.assertion
def to_be_instance_of(topic, expected):
    '''Asserts that `topic` is an instance of `expected`.'''
    if not isinstance(topic, expected):
        raise VowsAssertionError('Expected topic(%s) to be an instance of %s, but it was a %s', topic, expected, topic.__class__)

@Vows.assertion
def not_to_be_instance_of(topic, expected):
    '''Asserts that `topic` is NOT an instance of `expected`.'''
    if isinstance(topic, expected):
        raise VowsAssertionError('Expected topic(%s) not to be an instance of %s', topic, expected)

