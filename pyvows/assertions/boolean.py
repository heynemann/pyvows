#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.assertion
def is_true(actual):
    assert bool(actual), "Expected topic(%s) to be truthy, but it wasn't" % (actual, )

@Vows.assertion
def is_false(actual):
    assert not bool(actual), "Expected topic(%s) to be falsy, but it wasn't" % (actual, )

