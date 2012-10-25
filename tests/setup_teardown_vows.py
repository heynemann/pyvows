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

    def teardown(self):
        print '1st level teardown'
        expect(self.exec_order).to_equal([1, 2, 3, -2, -1])

    class OrderOfExecution(Vows.Context):
        def setup(self):
            print '2nd level setup'
            self.parent.exec_order.append(1)

        def topic(self):
            print '2nd level topic'
            self.parent.exec_order.append(2)
            return 20

        def teardown(self):
            print '2nd level teardown'
            self.parent.exec_order.append(-1) #last
            expect(self.parent.exec_order).to_equal([1, 2, 3, -2, -1])

        def check_order(self, topic):
            print '2nd level expectation'
            expect(self.parent.exec_order).to_equal([1, 2])

        class TeardownOrderOfExecution(Vows.Context):
            def setup(self):
                print '3rd level setup'
                self.parent.parent.exec_order.append(3)

            def teardown(self):
                print '3rd level teardown'
                self.parent.parent.exec_order.append(-2) #right before the parent's teardown
                expect(self.parent.parent.exec_order).to_equal([1, 2, 3, -2])

            def check_order(self, topic):
                print '3rd level expectation'
                expect(self.parent.parent.exec_order).to_equal([1, 2, 3])


