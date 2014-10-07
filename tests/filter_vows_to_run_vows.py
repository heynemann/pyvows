#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Nathan Dotz nathan.dotz@gmail.com

from pyvows import Vows, expect
from pyvows import cli
from pyvows.runner import VowsRunner
from pyvows.runner.executionplan import ExecutionPlanner


class VowsTestCopy1(Vows):
    exclusion_patterns = set()
    inclusion_patterns = set()
    suites = dict()


class VowsTestCopy2(Vows):
    exclusion_patterns = set()
    inclusion_patterns = set()
    suites = dict()


@Vows.batch
class FilterOutVowsFromCommandLine(Vows.Context):

    class Console(Vows.Context):
        def topic(self):
            return cli

        def should_hand_off_exclusions_to_Vows_class(self, topic):

            patterns = ['foo', 'bar', 'baz']
            try:
                topic.run(None, '*_vows.py', 2, False, patterns)
            except Exception:
                expect(Vows.exclusion_patterns).to_equal(patterns)

        def should_hand_off_inclusions_to_Vows_class(self, topic):

            patterns = ['foo', 'bar', 'baz']
            try:
                topic.run(None, '*_vows.py', 2, False, None, patterns)
            except Exception:
                expect(Vows.inclusion_patterns).to_equal(patterns)

    # TODO: add vow checking that there is a message about vow matching

    class Core(Vows.Context):

        def topic(self):
            return VowsTestCopy1

        class RunMethod(Vows.Context):

            class UsingAnExclusionPattern(Vows.Context):
                def topic(self):
                    VowsTestCopy1.exclusion_patterns = ['asdf']
                    VowsTestCopy1.suites = {
                        'dummySuite': [TestContext]
                    }
                    return VowsTestCopy1.run(None, None)

                def should_not_run_the_excluded_vow(self, topic):
                    expect(topic.contexts[0]['tests']).to_equal([])

            class UsingAnInclusionPattern(Vows.Context):
                def topic(self):
                    VowsTestCopy2.inclusion_patterns = ['asdf']
                    VowsTestCopy2.suites = {
                        'dummySuite': [TestContext2]
                    }
                    return VowsTestCopy2.run(None, None)

                def should_only_run_asdf(self, topic):
                    expect([t['name'] for t in topic.contexts[0]['tests']]).to_equal(['asdf'])

    class ResultsOfRunningTwoContextsWithConflictingIgnores(Vows.Context):

        def topic(self):
            dummySuite = {'dummySuite': set([OverlappingIgnores1, OverlappingIgnores2])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan)
            return runner.run()

        def context1_ran_only_test2(self, topic):
            testsRan = [context for context in topic.contexts if context['name'] == 'OverlappingIgnores1'][0]['tests']
            testNames = [t['name'] for t in testsRan]
            expect(testNames).to_equal(['test2'])

        def context2_ran_only_test1(self, topic):
            testsRan = [context for context in topic.contexts if context['name'] == 'OverlappingIgnores2'][0]['tests']
            testNames = [t['name'] for t in testsRan]
            expect(testNames).to_equal(['test1'])


class TestContext(Vows.Context):
    def topic(self):
        return 'test'

    def asdf(self, topic):
        expect(topic).to_equal('test')


class TestContext2(Vows.Context):
    def topic(self):
        return 'test'

    def asdf(self, topic):
        expect(topic).to_equal('test')

    def fdsa(self, topic):
        expect(topic).to_equal('test')


class OverlappingIgnores1(Vows.Context):
    def topic(self):
        self.ignore('test1')
        return 1

    def test1(self, topic):
        expect(topic).to_equal(1)

    def test2(self, topic):
        expect(topic).to_equal(1)


class OverlappingIgnores2(Vows.Context):
    def topic(self):
        self.ignore('test2')
        return 1

    def test1(self, topic):
        expect(topic).to_equal(1)

    def test2(self, topic):
        expect(topic).to_equal(1)
