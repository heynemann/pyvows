#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect

@Vows.batch
class SetupTeardownSpecs(Vows.Context):
    exec_order = []

    class OrderOfExecution(Vows.Context):
        def setup(self):
            self.parent.exec_order.append(1)

        def topic(self):
            self.parent.exec_order.append(2)
            return 20

        def teardown(self):
            self.parent.exec_order.append(3)

        def check_order(self, topic):
            expect(self.parent.exec_order).to_equal([1, 2])

        class TeardownOrderOfExecution(Vows.Context):
            def check_order(self, topic):
                expect(self.parent.parent.exec_order).to_equal([1, 2, 3])

