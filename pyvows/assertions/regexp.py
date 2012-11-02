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
    if not re.match(expected, topic):
        raise VowsAssertionError('Expected topic({topic!r}) to match the regular expression {regex!r}'.format(
            topic  = topic, 
            regex  = expected))

@Vows.assertion
def not_to_match(topic, expected):
    if re.match(expected, topic):
        raise VowsAssertionError('Expected topic({topic!r}) not to match the regular expression {regex!r}'.format(
            topic = topic, 
            regex = expected))

