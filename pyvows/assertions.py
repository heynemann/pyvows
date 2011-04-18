#!/usr/bin/env python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from pyvows import Vows

@Vows.assertion
def are_equal(expected, actual):
    assert expected == actual, "Expected %s, got %s" % (expected, actual)

@Vows.assertion
def is_numeric(actual):
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
        return complex(lit)

    assert validate(str(actual)), "Expected %s to be numeric, but it wasn't" % actual
