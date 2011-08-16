#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import numbers

from pyvows import Vows

@Vows.create_assertions
def to_be_numeric(topic):
    return isinstance(topic, numbers.Number)

