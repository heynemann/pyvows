#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.assertion
def to_be_true(topic):
    assert bool(topic), "Expected topic(%s) to be truthy" % (topic, )

@Vows.assertion
def to_be_false(topic):
    assert not bool(topic), "Expected topic(%s) to be falsy" % (topic, )

