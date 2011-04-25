#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.assertion
def are_alike(expected, actual):
    if isinstance(actual, basestring):
        assert compare_strings(expected, actual), "Expected topic('%s') to be like '%s', but it wasn't" % (actual, expected)

@Vows.assertion
def not_are_alike(expected, actual):
    if isinstance(actual, basestring):
        assert not compare_strings(expected, actual), "Expected topic('%s') not to be like '%s', but it was" % (actual, expected)

def compare_strings(expected, actual):
    replaced_actual = actual.lower().replace(' ', '')
    replaced_expected = expected.lower().replace(' ', '')
    return replaced_expected.lower() == replaced_actual.lower()
