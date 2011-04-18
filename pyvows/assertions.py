#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

def validate(lit):
    if lit == '0': return 0
    litneg = lit[1:] if lit[0] == '-' else lit
    if litneg[0] == '0':
        if litneg[1] in 'xX':
            return int(lit,16)
        elif litneg[1] in 'bB':
            return int(lit,2)
        else:
            try:
                return int(lit,8)
            except ValueError:
                pass
    try:
        return int(lit)
    except ValueError:
        pass
    try:
        return float(lit)
    except ValueError:
        pass
    try:
        return complex(lit)
    except ValueError:
        return None

@Vows.assertion
def are_equal(expected, actual):
    assert expected == actual, "Expected topic to be %s, but it was %s" % (expected, actual)

@Vows.assertion
def is_numeric(actual):
    assert validate(str(actual)), "Expected topic(%s) to be numeric, but it wasn't" % actual

@Vows.assertion
def not_are_equal(expected, actual):
    assert expected != actual, "Expected topic not to be %s, but it was" % (expected)

@Vows.assertion
def not_is_numeric(actual):
    assert validate(str(actual)) is None, "Expected topic(%s) not to be numeric, but it was" % actual
