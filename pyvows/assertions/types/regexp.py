#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows regular expression assertions.  For use with `expect()` (see `pyvows.core`).
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import re

from pyvows import Vows, VowsAssertionError


@Vows.assertion
def to_match(topic, expected):
    '''Asserts that `topic` matches the regular expression
    `expected`.

    '''
    if not re.match(expected, topic):
        raise VowsAssertionError('Expected topic({0}) to match the regular expression {1}', topic, expected)


@Vows.assertion
def not_to_match(topic, expected):
    '''Asserts that `topic` DOES NOT match the regular expression
    `expected`.

    '''
    if re.match(expected, topic):
        raise VowsAssertionError('Expected topic({0}) not to match the regular expression {1}', topic, expected)
