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
def to_be_numeric(topic):
    assert isinstance(topic, numbers.Number), "Expected topic(%s) to be numeric, but it wasn't" % topic

@Vows.assertion
def not_to_be_numeric(topic):
    assert not isinstance(topic, numbers.Number), "Expected topic(%s) not to be numeric, but it was" % topic

