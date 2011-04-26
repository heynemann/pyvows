#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.assertion
def has_errored_with(expected, actual):
    assert isinstance(actual, expected), "Expected topic(%s) to be an error of type %s, but it was a %s" % (actual, expected, actual.__class__)

@Vows.assertion
def has_error_message_of(expected, actual):
    assert str(actual) == expected, "Expected topic(%s) to be an error with message '%s', but it had a different message" % (actual, expected)

