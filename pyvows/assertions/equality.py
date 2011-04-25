#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.assertion
def are_equal(expected, actual):
    assert expected == actual, "Expected topic to be %s, but it was %s" % (expected, actual)

@Vows.assertion
def not_are_equal(expected, actual):
    assert expected != actual, "Expected topic not to be %s, but it was" % (expected)

