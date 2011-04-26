#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import re

from pyvows import Vows

@Vows.assertion
def match(expected, actual):
    assert re.match(expected, actual), "Expected topic(%s) to match the regular expression %s, but it didn't" % (actual, expected)

@Vows.assertion
def not_match(expected, actual):
    assert not re.match(expected, actual), "Expected topic(%s) to not match the regular expression %s, but it did" % (actual, expected)

