#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Richard Lupton r.lupton@gmail.com

from pyvows import Vows, expect
from pyvows.reporting import VowsDefaultReporter
from pyvows.runner.abc import VowsTopicError

@Vows.batch
class ErrorReporting(Vows.Context):

    def setup(self):
        class MockResult:
            def eval_context(self, context):
                return False
        self.reporter = VowsDefaultReporter(MockResult(), 0)

    class PrintingAContextWithATopicError:
        def topic(self):
            mock_exc_info = ('type', 'value', 'traceback')
            context = {
                'contexts': [],
                'error': VowsTopicError('topic', mock_exc_info),
                'filename': '/path/to/vows.py',
                'name': 'TestContext',
                'tests': [],
                'topic_elapsed': 0
            }
            return context

        def reporter_should_call_print_traceback_with_the_exception(self, context):
            reporter = self.parent.reporter
            called = [False]
            def print_traceback(exc_type, exc_value, exc_traceback):
                expect(exc_type).to_equal('type')
                expect(exc_value).to_equal('value')
                expect(exc_traceback).to_equal('traceback')
                called[0] = True
            reporter.print_traceback = print_traceback

            reporter.print_context('TestContext', context)
            expect(called[0]).to_be_true()
