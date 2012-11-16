#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows error assertions.  For use with `expect()` (see `pyvows.core`).
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 Bernardo Heynemann heynemann@gmail.com

import inspect

from pyvows import Vows, VowsAssertionError

@Vows.assertion
def to_be_an_error_like(topic, expected):
    if not isinstance(topic, expected):
        raise VowsAssertionError('Expected topic(%s) to be an error of type %s, but it was a %s', topic, expected, topic.__class__)

@Vows.assertion
def to_have_an_error_message_of(topic, expected):
    if str(topic) != expected:
        raise VowsAssertionError('Expected topic(%s) to be an error with message %s', topic, expected)

@Vows.create_assertions
def to_be_an_error(topic):
    return topic and (isinstance(topic, Exception) or (inspect.isclass(topic) and issubclass(topic, Exception)))

