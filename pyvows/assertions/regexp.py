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
def to_match(topic, expected):
    assert re.match(expected, topic), "Expected topic(%s) to match the regular expression %s" % (topic, expected)

@Vows.assertion
def not_to_match(topic, expected):
    assert not re.match(expected, topic), "Expected topic(%s) not to match the regular expression %s" % (topic, expected)

