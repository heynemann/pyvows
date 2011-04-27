#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.assertion
def to_include(topic, expected):
    message = "Expected topic(%s) to include %s, but it didn't" % (topic, expected)

    assert expected in topic, message

@Vows.assertion
def not_to_include(topic, expected):
    message = "Expected topic(%s) not to include %s, but it did" % (topic, expected)

    assert expected not in topic, message
