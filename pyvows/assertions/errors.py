#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows error assertions.  For use with `expect()` (see `pyvows.core`).
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import inspect

from pyvows import Vows, VowsAssertionError

@Vows.assertion
def to_be_an_error_like(topic, expected):
    if not isinstance(topic, expected):
        raise VowsAssertionError('Expected topic({topic!r}) to be an error of type {expected!r}, but it was a {klass!r}'.format(
            topic    = topic, 
            expected = expected,
            klass    = topic.__class__ ))

@Vows.assertion
def to_have_an_error_message_of(topic, expected):
    if str(topic) != expected:
        raise VowsAssertionError('Expected topic({topic!r}) to be an error with message {expected!r}'.format(
            topic    = topic, 
            expected = expected))

@Vows.create_assertions
def to_be_an_error(topic):
    return topic and (isinstance(topic, Exception) or (inspect.isclass(topic) and issubclass(topic, Exception)))

