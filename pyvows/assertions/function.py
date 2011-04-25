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
def is_function(actual):
    assert inspect.ismethod(actual) or inspect.isfunction(actual), "Expected topic(%s) to be a function or a method, but it was a %s" % (actual, actual.__class__)

@Vows.assertion
def not_is_function(actual):
    assert not inspect.ismethod(actual) and not inspect.isfunction(actual), "Expected topic(%s) not to be a function or a method, but it was" % actual

