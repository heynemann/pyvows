#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect
from pyvows.reporting.xunit import XUnitReporter


class ResultMock():
    pass


@Vows.batch
class XUnitReporterVows(Vows.Context):

    class WhenShowingZeroTests(Vows.Context):
        def topic(self):
            result = ResultMock()
            result.successful_tests = 0
            result.errored_tests = 0
            result.elapsed_time = 0
            result.contexts = []
            reporter = XUnitReporter(result)
            return reporter

        def should_create_xml_header(self, topic):
            expect(topic.to_xml().find('<?xml version="1.0" encoding="utf-8"?>')).to_equal(0)

        def should_have_a_testsuite_node(self, topic):
            expect(topic.to_xml()).to_match(r'.*<testsuite errors="0" failures="0" hostname=".+?" ' +
                                            'name="pyvows" tests="0" time="0\.000" timestamp=".+?"/>')

        class WithDocument(Vows.Context):
            def topic(self, topic):
                return topic.create_report_document()

            def should_have_a_testsuite_node(self, topic):
                expect(topic.firstChild.nodeName).to_equal('testsuite')

    class WhenShowingASuccessfulResult(Vows.Context):
        def topic(self):
            result = ResultMock()
            result.successful_tests = 1
            result.errored_tests = 0
            result.elapsed_time = 0
            result.contexts = [
                {
                    'name': 'Context1',
                    'tests': [
                        {
                            'name': 'Test1',
                            'succeeded': True
                        }
                    ],
                    'contexts': []
                }
            ]
            reporter = XUnitReporter(result)
            return reporter.create_report_document().firstChild.firstChild

        def should_create_a_testcase_node(self, topic):
            expect(topic.nodeName).to_equal('testcase')

        def should_set_classname_for_context(self, topic):
            expect(topic.getAttribute('classname')).to_equal('Context1')

        def should_set_name_for_context(self, topic):
            expect(topic.getAttribute('name')).to_equal('Test1')
