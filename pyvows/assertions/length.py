#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows length assertions.  For use with `expect()` (see `pyvows.core`).
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, VowsAssertionError

@Vows.assertion
def to_length(topic, expected):
    '''Asserts that `len(topic)` == `expected`.'''
    if len(topic) != expected:
        raise VowsAssertionError('Expected topic(%s) to have %s of length, but it has %s', topic, expected, len(topic))

@Vows.assertion
def not_to_length(topic, expected):
    '''Asserts that `len(topic)` != `expected`.'''
    if len(topic) == expected:
        raise VowsAssertionError('Expected topic(%s) not to have %s of length', topic, expected)
