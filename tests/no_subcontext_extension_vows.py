#!/usr/bin/env python

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
        def topic(self):
            self.parent.entered = True
            return 2

        def should_be_working_fine_too(self, topic):
            self.parent.entered = True
            expect(topic).to_equal(2)
