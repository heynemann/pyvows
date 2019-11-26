#!/usr/bin/env python
# -*- coding: utf-8 -*-

# unbreaking some pyvows

# This file is MIT licensed
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 nathan dotz

from pyvows import Vows, expect
from pyvows.result import VowsResult
from pyvows.reporting import VowsTestReporter  # , VowsDefaultReporter

try:
    from StringIO import StringIO
except:
    from io import StringIO


@Vows.batch
class VowsTestReporterExceptions(Vows.Context):

    def topic(self):
        v = VowsTestReporter(VowsResult(), 0)
        return v

    def should_not_raise_TypeError_on_tests_without_a_topic(self, topic):
        try:
            # Notice that the test dict here has no 'topic' key.
            test = {'name':             'Mock Test Result',
                    'succeeded':        False,
                    'context_instance': Vows.Context(),
                    'error': {'type': '',
                              'value': '',
                              'traceback': ''},
                    'skip': None
                    }
            context = {'tests': [test],
                       'contexts': []
                       }
            output = StringIO()
            topic.print_context('Derp', context, file=output)
        except AssertionError as e:
            expect(e).to_be_an_error_like(AssertionError)
            expect(e).Not.to_be_an_error_like(TypeError)
