#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows boolean assertions.  For use with `expect()` (see `pyvows.core`).
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, VowsAssertionError


@Vows.assertion
def to_be_true(topic):
    '''Asserts that the boolean value of `topic` is `True`.'''
    if not bool(topic):
        raise VowsAssertionError("Expected topic({0}) to be truthy", topic)


@Vows.assertion
def to_be_false(topic):
    '''Asserts that the boolean value of `topic` is `False`.'''
    if bool(topic):
        raise VowsAssertionError("Expected topic({0}) to be falsy", topic)
