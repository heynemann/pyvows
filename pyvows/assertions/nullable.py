#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyVows "null" (None) assertions.  For use with `expect()` (see `pyvows.core`).
'''


# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, VowsAssertionError

@Vows.assertion
def to_be_null(topic):
    if topic is not None:
        raise VowsAssertionError('Expected topic({topic!r}) to be None'.format(
            topic = topic ))

@Vows.assertion
def not_to_be_null(topic):
    if topic is None:
        raise VowsAssertionError('Expected topic({topic!r}) not to be None'.format(
            topic = topic ))

