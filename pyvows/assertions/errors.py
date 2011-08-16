#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import inspect

from pyvows import Vows

@Vows.assertion
def to_be_an_error_like(topic, expected):
    assert isinstance(topic, expected), "Expected topic(%s) to be an error of type %s, but it was a %s" % (topic, expected, topic.__class__)

@Vows.assertion
def to_have_an_error_message_of(topic, expected):
    assert str(topic) == expected, "Expected topic(%s) to be an error with message '%s', but it had a different message" % (topic, expected)

@Vows.create_assertions
def to_be_an_error(topic):
    return topic and (isinstance(topic, Exception) or (inspect.isclass(topic) and issubclass(topic, Exception)))

