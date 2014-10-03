#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect
from pyvows.reporting.xunit import XUnitReporter
from pyvows.runner.abc import VowsTopicError
import sys


class ResultMock():
    pass


@Vows.batch
class XUnitReporterVows(Vows.Context):

    class WhenShowingZeroTests(Vows.Context):
        def topic(self):
            result = ResultMock()
            result.successful_tests = 0
            result.errored_tests = 0
            result.total_test_count = 0
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
            result.total_test_count = 1
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
            return reporter.create_report_document().firstChild

        def should_create_a_testcase_node(self, topic):
            expect(topic.firstChild.nodeName).to_equal('testcase')

        def should_create_topic_and_test_node(self, topic):
            expect(len(topic.childNodes)).to_equal(2)

        def should_set_classname_for_context(self, topic):
            classnames = [node.getAttribute('classname') for node in topic.childNodes]
            expect(classnames).to_equal(['Context1', 'Context1'])

        def should_set_name_for_context(self, topic):
            names = sorted([node.getAttribute('name') for node in topic.childNodes])
            expect(names).to_equal(['Test1', 'topic'])

    class WhenShowingATopicError(Vows.Context):
        def topic(self):
            result = ResultMock()
            result.successful_tests = 1
            result.errored_tests = 0
            result.total_test_count = 1
            result.elapsed_time = 0
            result.contexts = [
                {
                    'name': 'Context1',
                    'tests': [],
                    'error': VowsTopicError('topic', sys.exc_info()),
                    'contexts': []
                }
            ]
            reporter = XUnitReporter(result)
            return reporter.create_report_document().firstChild.firstChild

        def should_create_a_failing_test_for_topic(self, topic):
            expect(len(topic.childNodes)).to_equal(1)

        class FailureNodeForTopic(Vows.Context):
            def topic(self, testcase):
                return testcase.firstChild

            def should_have_exception_attributes(self, topic):
                expect(topic.getAttribute('type')).to_equal('VowsTopicError')
                expect(topic.getAttribute('message')).to_equal('Error in topic')
