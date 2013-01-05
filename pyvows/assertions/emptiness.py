#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows emptiness assertion.  For use with `expect()` (see `pyvows.core`).
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows

@Vows.create_assertions
def to_be_empty(topic):
    '''Asserts that the `len` of `topic` is `0`.'''
    return len(topic) == 0

