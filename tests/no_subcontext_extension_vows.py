#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class ContextClass(Vows.Context):
    entered = False

    def topic(self):
        return 1

    def should_be_working_fine(self, topic):
        expect(topic).to_equal(1)

    def teardown(self):
        # note to readers: 'expect's are not recommended on teardown methods
        expect(self.entered).to_equal(True)

    class SubcontextThatDoesntNeedToExtendAgainFromContext:
        entered = False

        def topic(self):
            return 2

        def should_be_working_fine_too(self, topic):
            self.parent.entered = True
            expect(topic).to_equal(2)

        def teardown(self):
            # note to readers: 'expect's are not recommended on teardown methods
            expect(self.entered).to_equal(True)

        class SubcontextThatDoesntNeedToExtendAgainFromContext:
            def topic(self):
                return 3

            def should_be_working_fine_too(self, topic):
                self.parent.entered = True
                expect(topic).to_equal(3)
