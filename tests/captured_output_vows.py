from __future__ import print_function
import sys

from pyvows import Vows, expect
from pyvows.runner.gevent import VowsParallelRunner
from pyvows.runner.executionplan import ExecutionPlanner
from pyvows.runner import VowsRunner


@Vows.batch
class CapturedOutputVows(Vows.Context):

    class ResultsFromContextThatExplicitlyCapturesOutput(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([OutputSomeStuff])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            return runner.run()

        def results_are_successful(self, topic):
            expect(topic.successful).to_equal(True)

        class TopContextStdout(Vows.Context):
            def topic(self, results):
                return results.contexts[0]['stdout']

            def has_setup_topic_teardown(self, topic):
                expect(topic).to_equal('setup\ntopic\nteardown\n')

        class TopContextStderr(Vows.Context):
            def topic(self, results):
                return results.contexts[0]['stderr']

            def has_setup_topic_teardown_err(self, topic):
                expect(topic).to_equal('setup-err\ntopic-err\nteardown-err\n')

        class SubcontextStdout(Vows.Context):
            def topic(self, results):
                return results.contexts[0]['contexts'][0]['stdout']

            def has_subcontext_topic(self, topic):
                expect(topic).to_equal('subcontext-topic\n')

        class SubcontextStderr(Vows.Context):
            def topic(self, results):
                return results.contexts[0]['contexts'][0]['stderr']

            def has_subcontext_topic_err(self, topic):
                expect(topic).to_equal('subcontext-topic-err\n')

        class TopContextVowStdout(Vows.Context):
            def topic(self, results):
                return results.contexts[0]['tests'][0]['stdout']

            def has_vow(self, topic):
                expect(topic).to_equal('vow\n')

        class TopContextVowStderr(Vows.Context):
            def topic(self, results):
                return results.contexts[0]['tests'][0]['stderr']

            def has_vow_err(self, topic):
                expect(topic).to_equal('vow-err\n')

    class ResultsFromContextThatPrintsWhenSysStreamsArePatched(ResultsFromContextThatExplicitlyCapturesOutput):
        def topic(self):
            dummySuite = {'dummySuite': set([PrintSomeStuff])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, True)
            return runner.run()


class OutputSomeStuff(Vows.Context):
    def setup(self):
        VowsParallelRunner.output.stdout.write('setup\n')
        VowsParallelRunner.output.stderr.write('setup-err\n')

    def topic(self):
        VowsParallelRunner.output.stdout.write('topic\n')
        VowsParallelRunner.output.stderr.write('topic-err\n')

    def teardown(self):
        VowsParallelRunner.output.stdout.write('teardown\n')
        VowsParallelRunner.output.stderr.write('teardown-err\n')

    def vow(self, topic):
        VowsParallelRunner.output.stdout.write('vow\n')
        VowsParallelRunner.output.stderr.write('vow-err\n')

    class OutputFromSubcontext(Vows.Context):
        def topic(self):
            VowsParallelRunner.output.stdout.write('subcontext-topic\n')
            VowsParallelRunner.output.stderr.write('subcontext-topic-err\n')


class PrintSomeStuff(Vows.Context):
    def setup(self):
        print('setup')
        print('setup-err', file=sys.stderr)

    def topic(self):
        print('topic')
        print('topic-err', file=sys.stderr)

    def teardown(self):
        print('teardown')
        print('teardown-err', file=sys.stderr)

    def vow(self, topic):
        print('vow')
        print('vow-err', file=sys.stderr)

    class PrintFromSubcontext(Vows.Context):
        def topic(self):
            print('subcontext-topic')
            print('subcontext-topic-err', file=sys.stderr)
