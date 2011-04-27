#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect

@Vows.batch
class DivisionTests(Vows.Context):

    class WhenDividing42Per1(Vows.Context):

        def topic(self):
            return 42 / 1

        def WeGetANumber(self, topic):
            expect(topic).to_be_numeric()

        def WeGet42(self, topic):
            expect(topic).to_be_equal_to(42)

