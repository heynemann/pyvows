#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import numbers

from pyvows import Vows

@Vows.assertion
def is_numeric(actual):
    assert isinstance(actual, numbers.Number), "Expected topic(%s) to be numeric, but it wasn't" % actual

@Vows.assertion
def not_is_numeric(actual):
    assert not isinstance(actual, numbers.Number), "Expected topic(%s) not to be numeric, but it was" % actual

