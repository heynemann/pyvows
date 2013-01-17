#!/usr/bin/env python
# -*- coding: utf-8 -*-

# unbreaking some pyvows from https://github.com/heynemann/pyvows

# This file is MIT licensed
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 nathan dotz

from pyvows import Vows, expect
from pyvows.core import VowsAssertionError
from pyvows.runner import VowsParallelRunner
from pyvows.result import VowsResult
from pyvows.reporting import VowsTestReporter  # , VowsDefaultReporter


@Vows.batch
class VowsTestReporterExceptions(Vows.Context):

    def topic(self):
        v = VowsTestReporter(VowsResult(), 0)
        v.print_traceback = lambda a, b, c, d: None
        v.humanized_print = lambda a: None
        return v

    def should_not_raise_TypeError_on_tests_without_a_topic(self, topic):
        try:
            # Notice that the test dict here has no 'topic' key.
            test = {'name': 'Mock Test Result',
                                  'succeeded': False,
                                  'context_instance': Vows.Context(),
                                  'error': {'type': '', 'value': '', 'traceback': ''}}

            context = {'tests': [test],
                       'contexts': []}
            topic.print_context("Derp", context)
        except VowsAssertionError as e:
            expect(e).to_be_an_error_like(VowsAssertionError)
            expect(e).Not.to_be_an_error_like(TypeError)
            print e.msg
