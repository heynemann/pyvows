#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.assertion
def to_be_null(topic):
    assert topic is None, "Expected topic(%s) to be None, but it wasn't" % topic

@Vows.assertion
def not_to_be_null(topic):
    assert topic is not None, "Expected topic(%s) not to be None, but it was" % topic

