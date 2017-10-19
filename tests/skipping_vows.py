from pyvows import Vows, expect
from pyvows.runner import VowsRunner
from pyvows.runner.executionplan import ExecutionPlanner
from pyvows.runner import SkipTest
from pyvows.reporting.test import VowsTestReporter
from pyvows.reporting.xunit import XUnitReporter
from pyvows.reporting.common import V_VERBOSE

try:
    from StringIO import StringIO
except:
    from io import StringIO


@Vows.batch
class SkippingThings(Vows.Context):

    class ResultsWhenTopicRaisesASkipTestException(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([SkipIsRaisedFromTopic])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            results = runner.run()
            return results

        def results_are_successful(self, topic):
            expect(topic.successful).to_equal(True)

        def teardown_is_still_called(self, topic):
            expect(SkipIsRaisedFromTopic.teardownCalled).to_equal(True)

        def test_is_not_run(self, topic):
            expect(SkipIsRaisedFromTopic.testRun).to_equal(False)

        def subcontext_topic_is_not_run(self, topic):
            expect(SkipIsRaisedFromTopic.subcontextTopicRun).to_equal(False)

        def subcontext_test_is_not_run(self, topic):
            expect(SkipIsRaisedFromTopic.subcontextTestRun).to_equal(False)

        def there_are_four_skipped_tests(self, topic):
            expect(topic.skipped_tests).to_equal(4)

        def there_are_zero_successful_tests(self, topic):
            expect(topic.successful_tests).to_equal(0)

        def there_are_zero_errored_tests(self, topic):
            expect(topic.errored_tests).to_equal(0)

        def there_are_four_total_tests(self, topic):
            expect(topic.total_test_count).to_equal(4)

        class TestReporterVerbose(Vows.Context):
            def topic(self, results):
                return VowsTestReporter(results, V_VERBOSE)

            class TestReporterVerboseOutput(Vows.Context):
                def topic(self, reporter):
                    output = StringIO()
                    reporter.pretty_print(file=output)
                    return output.getvalue()

                def shows_skipped_count(self, topic):
                    expect(topic).to_include('4 skipped')

                def top_context_shows_skipped_message(self, topic):
                    expect(topic).to_include('Skip is raised from topic (SKIPPED: just because)')

                def subcontext_shows_skipped_message(self, topic):
                    expect(topic).to_include('Sub context (SKIPPED: just because)')

                def tests_should_not_run_vow_shows_skipped(self, topic):
                    expect(topic).to_include('? tests should not run\n')

                def subcontext_tests_should_also_not_run_vow_shows_skipped(self, topic):
                    expect(topic).to_include('? subcontext tests should also not run\n')

        class TestReporterNonVerbose(Vows.Context):
            def topic(self, results):
                return VowsTestReporter(results, 0)

            class TestReporterNonVerboseOutput(Vows.Context):
                def topic(self, reporter):
                    output = StringIO()
                    reporter.pretty_print(file=output)
                    return output.getvalue()

                def no_skipped_contexts_or_vows(self, topic):
                    expect(topic).Not.to_include('SKIPPED')
                    expect(topic).Not.to_include('?')

        class XunitReporterDocument(Vows.Context):
            def topic(self, results):
                return XUnitReporter(results).create_report_document()

            def suite_node_has_attribute_skip_set_to_four(self, topic):
                expect(topic.firstChild.getAttribute('skip')).to_equal('4')

            class TopContextNode(Vows.Context):
                def topic(self, doc):
                    return [testNode for testNode in doc.firstChild.childNodes if testNode.getAttribute('name') == 'topic'][0]

                class TopicSkipNode(Vows.Context):
                    def topic(self, testcaseNode):
                        return [node for node in testcaseNode.childNodes if node.nodeName == 'skipped'][0]

                    def message_is_just_because(self, topic):
                        expect(topic.getAttribute('message')).to_equal('just because')

            class TopContextVowNode(Vows.Context):
                def topic(self, doc):
                    return [testNode for testNode in doc.firstChild.childNodes
                            if testNode.getAttribute('name') == 'tests_should_not_run'][0]

                class VowSkipNode(Vows.Context):
                    def topic(self, testcaseNode):
                        return [node for node in testcaseNode.childNodes if node.nodeName == 'skipped'][0]

                    def message_is_just_because(self, topic):
                        expect(topic.getAttribute('message')).to_equal('just because')

    class ResultsWhenVowsRaiseExceptions(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([SkipIsRaisedFromVow])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            results = runner.run()
            return results

        def results_are_successful(self, topic):
            expect(topic.successful).to_equal(True)

        def teardown_is_still_called(self, topic):
            expect(SkipIsRaisedFromVow.teardownCalled).to_equal(True)

        def subcontext_topic_is_run(self, topic):
            expect(SkipIsRaisedFromVow.subcontextTopicRun).to_equal(True)

        def there_are_two_skipped_tests(self, topic):
            expect(topic.skipped_tests).to_equal(2)

        def there_are_two_successful_tests(self, topic):
            expect(topic.successful_tests).to_equal(2)

        def there_are_zero_errored_tests(self, topic):
            expect(topic.errored_tests).to_equal(0)

        def there_are_four_total_tests(self, topic):
            expect(topic.total_test_count).to_equal(4)

        class TestReporterVerbose(Vows.Context):
            def topic(self, results):
                return VowsTestReporter(results, V_VERBOSE)

            class TestReporterVerboseOutput(Vows.Context):
                def topic(self, reporter):
                    output = StringIO()
                    reporter.pretty_print(file=output)
                    return output.getvalue()

                def shows_skipped_count(self, topic):
                    expect(topic).to_include('2 skipped')

                def top_context_shows_no_skip_message(self, topic):
                    expect(topic).to_include('Skip is raised from vow\n')

                def subcontext_shows_no_skip_message(self, topic):
                    expect(topic).to_include('Sub context\n')

                def tests_should_not_run_vow_shows_skipped_with_message(self, topic):
                    expect(topic).to_include('? tests should not run (SKIPPED: just because)\n')

                def subcontext_tests_should_also_not_run_vow_shows_skipped_with_message(self, topic):
                    expect(topic).to_include('? subcontext tests should also not run (SKIPPED: just because)\n')

    class ResultsWhenTopicHasSkipIfTrueDecorator(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([TopicHasSkipIfTrueDecorator])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            results = runner.run()
            return results

        def results_are_successful(self, topic):
            expect(topic.successful).to_equal(True)

        def teardown_is_still_called(self, topic):
            expect(TopicHasSkipIfTrueDecorator.teardownCalled).to_equal(True)

        def test_is_not_run(self, topic):
            expect(TopicHasSkipIfTrueDecorator.testRun).to_equal(False)

        def subcontext_topic_is_not_run(self, topic):
            expect(TopicHasSkipIfTrueDecorator.subcontextTopicRun).to_equal(False)

        def subcontext_test_is_not_run(self, topic):
            expect(TopicHasSkipIfTrueDecorator.subcontextTestRun).to_equal(False)

        def there_are_four_skipped_tests(self, topic):
            expect(topic.skipped_tests).to_equal(4)

        def there_are_zero_successful_tests(self, topic):
            expect(topic.successful_tests).to_equal(0)

        def there_are_zero_errored_tests(self, topic):
            expect(topic.errored_tests).to_equal(0)

        def there_are_four_total_tests(self, topic):
            expect(topic.total_test_count).to_equal(4)

    class ResultsWhenTopicHasSkipDecorator(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([TopicHasSkipDecorator])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            results = runner.run()
            return results

        def results_are_successful(self, topic):
            expect(topic.successful).to_equal(True)

        def teardown_is_still_called(self, topic):
            expect(TopicHasSkipDecorator.teardownCalled).to_equal(True)

        def test_is_not_run(self, topic):
            expect(TopicHasSkipDecorator.testRun).to_equal(False)

        def subcontext_topic_is_not_run(self, topic):
            expect(TopicHasSkipDecorator.subcontextTopicRun).to_equal(False)

        def subcontext_test_is_not_run(self, topic):
            expect(TopicHasSkipDecorator.subcontextTestRun).to_equal(False)

        def there_are_four_skipped_tests(self, topic):
            expect(topic.skipped_tests).to_equal(4)

        def there_are_zero_successful_tests(self, topic):
            expect(topic.successful_tests).to_equal(0)

        def there_are_zero_errored_tests(self, topic):
            expect(topic.errored_tests).to_equal(0)

        def there_are_four_total_tests(self, topic):
            expect(topic.total_test_count).to_equal(4)

    class ResultsWhenTopicHasSkipIfFalseDecorator(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([TopicHasSkipIfFalseDecorator])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            results = runner.run()
            return results

        def results_are_successful(self, topic):
            expect(topic.successful).to_equal(True)

        def teardown_is_still_called(self, topic):
            expect(TopicHasSkipIfFalseDecorator.teardownCalled).to_equal(True)

        def test_is_not_run(self, topic):
            expect(TopicHasSkipIfFalseDecorator.testRun).to_equal(True)

        def subcontext_topic_is_not_run(self, topic):
            expect(TopicHasSkipIfFalseDecorator.subcontextTopicRun).to_equal(True)

        def subcontext_test_is_not_run(self, topic):
            expect(TopicHasSkipIfFalseDecorator.subcontextTestRun).to_equal(True)

        def there_are_zero_skipped_tests(self, topic):
            expect(topic.skipped_tests).to_equal(0)

        def there_are_four_successful_tests(self, topic):
            expect(topic.successful_tests).to_equal(4)

        def there_are_zero_errored_tests(self, topic):
            expect(topic.errored_tests).to_equal(0)

        def there_are_four_total_tests(self, topic):
            expect(topic.total_test_count).to_equal(4)

    class ResultsWhenSubcontextHasSkipDecorator(Vows.Context):
        def topic(self):
            dummySuite = {'dummySuite': set([SubcontextHasSkipDecorator])}
            execution_plan = ExecutionPlanner(dummySuite, set(), set()).plan()
            runner = VowsRunner(dummySuite, Vows.Context, None, None, execution_plan, False)
            results = runner.run()
            return results

        def results_are_successful(self, topic):
            expect(topic.successful).to_equal(True)

        def teardown_is_still_called(self, topic):
            expect(SubcontextHasSkipDecorator.teardownCalled).to_equal(True)

        def test_is_not_run(self, topic):
            expect(SubcontextHasSkipDecorator.testRun).to_equal(True)

        def subcontext_topic_is_not_run(self, topic):
            expect(SubcontextHasSkipDecorator.subcontextTopicRun).to_equal(False)

        def subcontext_test_is_not_run(self, topic):
            expect(SubcontextHasSkipDecorator.subcontextTestRun).to_equal(False)

        def there_are_two_skipped_tests(self, topic):
            expect(topic.skipped_tests).to_equal(2)

        def there_are_two_successful_tests(self, topic):
            expect(topic.successful_tests).to_equal(2)

        def there_are_zero_errored_tests(self, topic):
            expect(topic.errored_tests).to_equal(0)

        def there_are_four_total_tests(self, topic):
            expect(topic.total_test_count).to_equal(4)

        class TestReporterVerbose(Vows.Context):
            def topic(self, results):
                return VowsTestReporter(results, V_VERBOSE)

            class TestReporterVerboseOutput(Vows.Context):
                def topic(self, reporter):
                    output = StringIO()
                    reporter.pretty_print(file=output)
                    return output.getvalue()

                def shows_skipped_count(self, topic):
                    expect(topic).to_include('2 skipped')

                def top_context_shows_skipped_message(self, topic):
                    expect(topic).to_include('Subcontext has skip decorator\n')

                def subcontext_shows_skipped_message(self, topic):
                    expect(topic).to_include('Sub context (SKIPPED: just because)')

                def tests_should_not_run_vow_shows_run(self, topic):
                    expect(topic).Not.to_include('? tests should not run\n')
                    try:
                        expect(topic).to_include('tests should not run\n')
                    except:
                        expect(topic).to_include("b'tests should not run'\n")

                def subcontext_tests_should_also_not_run_vow_shows_skipped(self, topic):
                    expect(topic).to_include('? subcontext tests should also not run\n')


class SkipIsRaisedFromTopic(Vows.Context):
    teardownCalled = False
    testRun = False
    subcontextTopicRun = False
    subcontextTestRun = False

    def topic(self):
        raise SkipTest('just because')

    def teardown(self):
        SkipIsRaisedFromTopic.teardownCalled = True

    def tests_should_not_run(self, topic):
        SkipIsRaisedFromTopic.testRun = True

    class SubContext(Vows.Context):
        def topic(self):
            SkipIsRaisedFromTopic.subcontextTopicRun = True

        def subcontext_tests_should_also_not_run(self, topic):
            SkipIsRaisedFromTopic.subcontextTestRun = True


class SkipIsRaisedFromVow(Vows.Context):
    teardownCalled = False
    subcontextTopicRun = False

    def topic(self):
        return 0

    def teardown(self):
        SkipIsRaisedFromVow.teardownCalled = True

    def tests_should_not_run(self, topic):
        raise SkipTest('just because')

    class SubContext(Vows.Context):
        def topic(self):
            SkipIsRaisedFromVow.subcontextTopicRun = True

        def subcontext_tests_should_also_not_run(self, topic):
            raise SkipTest('just because')


class TopicHasSkipIfTrueDecorator(Vows.Context):
    teardownCalled = False
    testRun = False
    subcontextTopicRun = False
    subcontextTestRun = False

    @Vows.skip_if(True, 'just because')
    def topic(self):
        return 0

    def teardown(self):
        TopicHasSkipIfTrueDecorator.teardownCalled = True

    def tests_should_not_run(self, topic):
        TopicHasSkipIfTrueDecorator.testRun = True

    class SubContext(Vows.Context):
        def topic(self):
            TopicHasSkipIfTrueDecorator.subcontextTopicRun = True

        def subcontext_tests_should_also_not_run(self, topic):
            TopicHasSkipIfTrueDecorator.subcontextTestRun = True


class TopicHasSkipIfFalseDecorator(Vows.Context):
    teardownCalled = False
    testRun = False
    subcontextTopicRun = False
    subcontextTestRun = False

    @Vows.skip_if(False, 'just because')
    def topic(self):
        return 0

    def teardown(self):
        TopicHasSkipIfFalseDecorator.teardownCalled = True

    def tests_should_not_run(self, topic):
        TopicHasSkipIfFalseDecorator.testRun = True

    class SubContext(Vows.Context):
        def topic(self):
            TopicHasSkipIfFalseDecorator.subcontextTopicRun = True

        def subcontext_tests_should_also_not_run(self, topic):
            TopicHasSkipIfFalseDecorator.subcontextTestRun = True


class TopicHasSkipDecorator(Vows.Context):
    teardownCalled = False
    testRun = False
    subcontextTopicRun = False
    subcontextTestRun = False

    @Vows.skip('just because')
    def topic(self):
        return 0

    def teardown(self):
        TopicHasSkipDecorator.teardownCalled = True

    def tests_should_not_run(self, topic):
        TopicHasSkipDecorator.testRun = True

    class SubContext(Vows.Context):
        def topic(self):
            TopicHasSkipDecorator.subcontextTopicRun = True

        def subcontext_tests_should_also_not_run(self, topic):
            TopicHasSkipDecorator.subcontextTestRun = True


class SubcontextHasSkipDecorator(Vows.Context):
    teardownCalled = False
    testRun = False
    subcontextTopicRun = False
    subcontextTestRun = False

    def topic(self):
        return 0

    def teardown(self):
        SubcontextHasSkipDecorator.teardownCalled = True

    def tests_should_not_run(self, topic):
        SubcontextHasSkipDecorator.testRun = True

    @Vows.skip('just because')
    class SubContext(Vows.Context):
        def topic(self):
            SubcontextHasSkipDecorator.subcontextTopicRun = True

        def subcontext_tests_should_also_not_run(self, topic):
            SubcontextHasSkipDecorator.subcontextTestRun = True
