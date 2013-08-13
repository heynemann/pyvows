# -*- coding: utf-8 -*-

# unbreaking some pyvows

# This file is MIT licensed
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 nathan dotz

from pyvows import Vows, expect
from pyvows.result import VowsResult, ContextResult, VowResult
from pyvows.reporting import VowsTestReporter  # , VowsDefaultReporter


def mock_context():
    class MockContext(Vows.Context): pass
    return MockContext


@Vows.batch
class VowsTestReporterExceptions(Vows.Context):

    def topic(self):
        v = VowsTestReporter(VowsResult(), 0)
        v.humanized_print = lambda a: None
        return v

    def should_not_raise_TypeError_on_tests_without_a_topic(self, topic):
        try:
            context = ContextResult(mock_context()() ) # has no 'topic'
            topic.print_context(context)
        except AssertionError as e:
            expect(e).to_be_an_error_like(AssertionError)
            expect(e).Not.to_be_an_error_like(TypeError)
