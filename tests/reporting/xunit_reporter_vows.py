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
class XunitReporterVows(Vows.Context):

    class WhenShowingZeroTests(Vows.Context):
        def topic(self):
            result = ResultMock()
            result.successful_tests = 0
            result.errored_tests = 0
            result.skipped_tests = 0
            result.total_test_count = 0
            result.elapsed_time = 0
            result.contexts = []
            reporter = XUnitReporter(result)
            return reporter

        def should_create_xml_header(self, topic):
            expect(topic.to_xml().find(b'<?xml version="1.0" encoding="utf-8"?>')).to_equal(0)

        def should_have_a_testsuite_node(self, topic):
            expect(topic.to_xml()).to_match(br'.*<testsuite.*/>')

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
            result.skipped_tests = 0
            result.total_test_count = 1
            result.elapsed_time = 0
            result.contexts = [
                {
                    'name': 'Context1',
                    'tests': [
                        {
                            'name': 'Test1',
                            'succeeded': True,
                            'stdout': 'outline',
                            'stderr': 'errline'
                        }
                    ],
                    'contexts': [],
                    'stdout': 'outline',
                    'stderr': 'errline'
                }
            ]
            reporter = XUnitReporter(result)
            return reporter.create_report_document().firstChild

        def should_create_topic_and_test_node(self, topic):
            expect(len(topic.childNodes)).to_equal(2)

        class TopicTestcase(Vows.Context):
            def topic(self, suiteNode):
                return [node for node in suiteNode.childNodes if node.getAttribute('name') == 'topic'][0]

            def node_name_is_testcase(self, topic):
                expect(topic.nodeName).to_equal('testcase')

            def classname_attribute_is_context1(self, topic):
                expect(topic.getAttribute('classname')).to_equal('Context1')

            class OutputNode(Vows.Context):
                def topic(self, testcaseNode):
                    return [node for node in testcaseNode.childNodes if node.nodeName == 'system-out'][0]

                def has_text_outline(self, topic):
                    expect(topic.firstChild.data).to_equal('outline')

            class ErrorNode(Vows.Context):
                def topic(self, testcaseNode):
                    return [node for node in testcaseNode.childNodes if node.nodeName == 'system-err'][0]

                def has_text_errline(self, topic):
                    expect(topic.firstChild.data).to_equal('errline')

        class Test1Testcase(Vows.Context):
            def topic(self, suiteNode):
                return [node for node in suiteNode.childNodes if node.getAttribute('name') == 'Test1'][0]

            def node_name_is_testcase(self, topic):
                expect(topic.nodeName).to_equal('testcase')

            def classname_attribute_is_context1(self, topic):
                expect(topic.getAttribute('classname')).to_equal('Context1')

            class OutputNode(Vows.Context):
                def topic(self, testcaseNode):
                    return [node for node in testcaseNode.childNodes if node.nodeName == 'system-out'][0]

                def has_text_outline(self, topic):
                    expect(topic.firstChild.data).to_equal('outline')

            class ErrorNode(Vows.Context):
                def topic(self, testcaseNode):
                    return [node for node in testcaseNode.childNodes if node.nodeName == 'system-err'][0]

                def has_text_errline(self, topic):
                    expect(topic.firstChild.data).to_equal('errline')

    class WhenShowingATopicError(Vows.Context):
        def topic(self):
            try:
                raise Exception('asdf')
            except:
                test_exc_info = sys.exc_info()

            result = ResultMock()
            result.successful_tests = 1
            result.errored_tests = 0
            result.skipped_tests = 0
            result.total_test_count = 1
            result.elapsed_time = 0
            result.contexts = [
                {
                    'name': 'Context1',
                    'tests': [],
                    'error': VowsTopicError('topic', test_exc_info),
                    'contexts': [],
                    'stdout': '',
                    'stderr': ''
                }
            ]
            reporter = XUnitReporter(result)
            return reporter.create_report_document().firstChild.firstChild

        class FailureNodeForTopic(Vows.Context):
            def topic(self, testcaseNode):
                return [node for node in testcaseNode.childNodes if node.nodeName == 'failure'][0]

            def should_have_original_exception_type(self, topic):
                expect(topic.getAttribute('type')).to_equal('Exception')

            def should_have_original_exception_message(self, topic):
                expect(topic.getAttribute('message')).to_equal('Error in topic: asdf')

    class WhenATopicIsACapturedExceptionAndAVowFails(Vows.Context):
        def topic(self):
            try:
                raise Exception('fdsa')
            except:
                test_exc_info = sys.exc_info()

            result = ResultMock()
            result.successful_tests = 1
            result.errored_tests = 1
            result.skipped_tests = 0
            result.total_test_count = 2
            result.elapsed_time = 0
            result.contexts = [
                {
                    'name': 'ContextWithCapturedError',
                    'error': None,
                    'contexts': [],
                    'stdout': '',
                    'stderr': '',
                    'tests': [{
                        'context_instance': Vows.Context(),
                        'name': 'failedCheckOnException',
                        'enumerated': False,
                        'result': None,
                        'topic': Exception('fdsa'),
                        'error': dict(zip(['type', 'value', 'traceback'], test_exc_info)),
                        'succeeded': False,
                        'file': 'asdf.py',
                        'lineno': 1,
                        'elapsed': 0,
                        'stdout': '',
                        'stderr': ''
                    }]
                }
            ]
            reporter = XUnitReporter(result)
            return reporter.create_report_document().firstChild

        class TestcaseForTest(Vows.Context):
            def topic(self, suiteNode):
                return [node for node in suiteNode.childNodes if node.getAttribute('name') == 'failedCheckOnException'][0]

            class FailureNodeForTopic(Vows.Context):
                def topic(self, testcaseNode):
                    return [node for node in testcaseNode.childNodes if node.nodeName == 'failure'][0]

                def should_have_original_exception_type(self, topic):
                    expect(topic.getAttribute('type')).to_equal('Exception')

                def should_have_original_exception_message(self, topic):
                    expect(topic.getAttribute('message')).to_equal('fdsa')
