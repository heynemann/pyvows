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
    if len(topic) != expected:
        raise VowsAssertionError('Expected topic({topic!r}) to have {expected:d} of length, but it has {length:d}'.format(
            topic    = topic, 
            expected = expected, 
            length   = len(topic)))

@Vows.assertion
def not_to_length(topic, expected):
    if len(topic) == expected:
        raise VowsAssertionError('Expected topic({topic!r}) not to have {expected:d} of length'.format(
            topic    = topic, 
            expected = expected))
