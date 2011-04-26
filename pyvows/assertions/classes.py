#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.assertion
def is_instance_of(expected, actual):
    assert isinstance(actual, expected), "Expected topic(%s) to be an instance of %s, but it was a %s" % (actual, expected, actual.__class__)

@Vows.assertion
def not_is_instance_of(expected, actual):
    assert not isinstance(actual, expected), "Expected topic(%s) not to be an instance of %s, but it was a %s" % (actual, expected, actual.__class__)

