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

try:
    from StringIO import StringIO
except:
    from io import StringIO

# These tests check that the reporting, which happens after all tests
# have run, correctly shows the errors raised in topic functions.

@Vows.batch
class ErrorReporting(Vows.Context):

    class TracebackOfTopicError:

        def setup(self):
            # The eval_context() method of the result object is called by
            # the reporter to decide if a context was successful or
            # not. Here we are testing the reporting of errors, so provide
            # a mock result which always says it has failed.
            class MockResult:
                def eval_context(self, context):
                    return False
            self.reporter = VowsDefaultReporter(MockResult(), 0)

            # Patch the print_traceback() method to just record its
            # arguments.
            self.print_traceback_args = None

            def print_traceback(*args, **kwargs):
                self.print_traceback_args = args
            self.reporter.print_traceback = print_traceback

        class AContextWithATopicError:
            def topic(self):
                # Simulate a context whose topic() function raised an error
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
                self.parent.print_traceback_args = None
                self.parent.reporter.print_context('TestContext', context, file=StringIO())
                expect(self.parent.print_traceback_args).to_equal(('type', 'value', 'traceback'))

        class ASuccessfulContext:
            def topic(self):
                # Simulate a context whose topic() didn't raise an error
                context = {
                    'contexts': [],
                    'error': None,
                    'filename': '/path/to/vows.py',
                    'name': 'TestContext',
                    'tests': [],
                    'topic_elapsed': 0
                }
                return context

            def reporter_should_not_call_print_traceback(self, context):
                self.parent.print_traceback_args = None
                self.parent.reporter.print_context('TestContext', context, file=StringIO())
                expect(self.parent.print_traceback_args).to_equal(None)
