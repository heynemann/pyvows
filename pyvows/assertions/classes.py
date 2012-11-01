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
    if not isinstance(topic, expected):
        raise VowsAssertionError('Expected topic({topic!r}) to be an instance of {expected!r}, but it was a {klass!r}'.format( 
            topic    = topic, 
            expected = expected, 
            klass    = topic.__class__ ))

@Vows.assertion
def not_to_be_instance_of(topic, expected):
    if isinstance(topic, expected):
        raise VowsAssertionError('Expected topic({topic!r}) not to be an instance of {expected!r}'.format(
            topic    = topic, 
            expected = expected ))

