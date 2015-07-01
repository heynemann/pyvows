#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Richard Lupton r.lupton@gmail.com

from pyvows import Vows, expect
from pyvows.runner import VowsRunner, SkipTest
from pyvows.runner.executionplan import ExecutionPlanner


# These tests demonstrate what happens when the topic function raises
# or returns an exception.

@Vows.batch
class ErrorsInTopicFunction(Vows.Context):

    class WhenTopicRaisesAnExceptionWithCaptureErrorDecorator:
        @Vows.capture_error
        def topic(self):
            return 42 / 0

        def it_is_passed_to_tests_as_normal(self, topic):
            expect(topic).to_be_an_error_like(ZeroDivisionError)

    class WhenTopicReturnsAnException(Vows.Context):
        def topic(self):
            try:
                return 42 / 0
            except Exception as e:
                return e

        def it_is_passed_to_tests_as_normal(self, topic):
            expect(topic).to_be_an_error_like(ZeroDivisionError)

    class WhenTopicRaisesAnUnexpectedException(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([WhenTopicRaisesAnException])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            return runner.run()

        def results_are_not_successful(self, topic):
            expect(topic.successful).to_equal(False)

        class ResultForTopContextVows(Vows.Context):
            def topic(self, results):
                return results.contexts[0]['tests'][0]

            def skip_is_set_to_a_skiptest_exception(self, topic):
                expect(topic['skip']).to_be_an_error_like(SkipTest)

            def skip_message_relates_reason_as_topic_failure(self, topic):
                expect(str(topic['skip'])).to_include('topic dependency failed')

        class ResultForSubContext(Vows.Context):
            def topic(self, results):
                return results.contexts[0]['contexts'][0]

            def skip_is_set_to_a_skiptest_exception(self, topic):
                expect(topic['skip']).to_be_an_error_like(SkipTest)

            def skip_message_relates_reason_as_topic_failure(self, topic):
                expect(str(topic['skip'])).to_include('topic dependency failed')

        def vows_and_subcontexts_and_teardown_are_not_called(self, topic):
            expect(WhenTopicRaisesAnException.functionsCalled).to_equal(0)

    class WhenSubcontextTopicRaisesAnException(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([WhenTeardownIsDefined])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set(['excluded_vows_do_not_block'])).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            return runner.run()

        def results_are_not_successful(self, topic):
            expect(topic.successful).to_equal(False)

        def ancestor_teardowns_are_all_called(self, topic):
            expect(WhenTeardownIsDefined.teardownCalled).to_equal(True)
            expect(
                WhenTeardownIsDefined.WhenSubcontextTeardownIsDefined.
                teardownCalled
            ).to_equal(True)

    class WhenTeardownRaisesAnException(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([WhenTeardownRaisesException])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            return runner.run()

        def results_are_not_successful(self, topic):
            expect(topic.successful).to_equal(False)


class WhenTopicRaisesAnException(Vows.Context):
    functionsCalled = 0

    def topic(self):
        return 42 / 0

    def teardown(self):
        WhenTopicRaisesAnException.functionsCalled += 1

    def tests_should_not_run(self, topic):
        WhenTopicRaisesAnException.functionsCalled += 1

    class SubContext(Vows.Context):
        def subcontexts_should_also_not_run(self, topic):
            WhenTopicRaisesAnException.functionsCalled += 1


class WhenTeardownIsDefined(Vows.Context):
    teardownCalled = False

    def teardown(self):
        WhenTeardownIsDefined.teardownCalled = True

    class WhenSubcontextTeardownIsDefined(Vows.Context):
        teardownCalled = False

        def teardown(self):
            WhenTeardownIsDefined.\
                WhenSubcontextTeardownIsDefined.teardownCalled = True

        def excluded_vows_do_not_block(self, topic):
            raise Exception('This will never pass')

        class WhenTopicRaisesAnException(Vows.Context):
            def topic(self):
                return 42 / 0


class WhenTeardownRaisesException(Vows.Context):
    def teardown(self):
        raise Exception('omg')
