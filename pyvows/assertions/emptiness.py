#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.assertion
def is_empty(actual):
    message = "Expected topic(%s) to be empty, but it wasn't" % (actual, )

    assert len(actual) == 0, message

@Vows.assertion
def is_not_empty(actual):
    message = "Expected topic(%s) not to be empty, but it was" % (actual, )

    assert len(actual) > 0, message

