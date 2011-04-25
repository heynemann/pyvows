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
def are_alike(expected, actual):
    message = "Expected topic(%s) to be like %s, but it wasn't"
    compare_alike(expected, actual, lambda result: result, message)

@Vows.assertion
def not_are_alike(expected, actual):
    message = 'Expected topic(%s) not to be like %s, but it was'
    compare_alike(expected, actual, lambda result: not result, message)

def compare_alike(expected, actual, modifier, message):
    if isinstance(actual, basestring):
        assert modifier(compare_strings(expected, actual)), message % ("'%s'" % actual, "'%s'" % expected)
    elif isinstance(actual, numbers.Number):
        assert modifier(compare_numbers(expected, actual)), message % (actual, expected)
    elif isinstance(actual, (list, tuple)):
        assert modifier(compare_lists(expected, actual)), message % (actual, expected)
    else:
        assert False, "Could not compare %s and %s" % (expected, actual)

def compare_strings(expected, actual):
    replaced_actual = actual.lower().replace(' ', '')
    replaced_expected = expected.lower().replace(' ', '')
    return replaced_expected.lower() == replaced_actual.lower()

def compare_numbers(expected, actual):
    if not isinstance(actual, numbers.Number) or \
       not isinstance(expected, numbers.Number):
        return False
    return float(expected) == float(actual)

def compare_lists(expected, actual):
    return match_lists(expected, actual) and match_lists(actual, expected)

def match_lists(expected, actual):
    for item in expected:
        if isinstance(item, (list, tuple)):
            found = False
            for inner_item in actual:
                if not isinstance(inner_item, (list, tuple)):
                    continue
                if compare_lists(item, inner_item):
                    found = True
                    break
            if not found:
                return False
        elif not item in actual:
            return False

    return True
