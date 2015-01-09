# -*- coding: utf-8 -*-
'''Contains `VowsResult` class, which collects the results of
each vow.

'''

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

#-------------------------------------------------------------------------------


class VowsResult(object):
    '''Collects success/failure/total statistics (as well as elapsed
    time) for the outcomes of tests.

    Only one instance of this class is created when PyVows is run.

    '''

    def __init__(self):
        self.contexts = []
        self.elapsed_time = 0.0

    def _count_contexts(self, contexts=None, count_func=lambda context: 1):
        '''Used interally for class properties
        `total_test_count`, `successful_tests`, and `errored_tests`.

        '''
        #   TODO
        #       Reevaluate whether `count_func` should have a default value
        #       (AFAICT the default is never used. It makes more sense
        #       to me if it had no default, or defaulted to `None`.
        context_count = 0

        for context in contexts:
            context_count += count_func(context)
            context_count += self._count_contexts(
                contexts=context['contexts'],
                count_func=count_func
            )

        return context_count

    def _get_topic_times(self, contexts=None):
        '''Returns a dict describing how long testing took for
        each topic in `contexts`.

        '''
        topic_times = []

        if contexts is None:
            contexts = self.contexts

        for context in contexts:
            topic_times.append({
                'context': context['name'],
                'path':    context['filename'],
                'elapsed': context['topic_elapsed']
            })
            ctx_topic_times = self._get_topic_times(context['contexts'])
            topic_times.extend(ctx_topic_times)

        return topic_times

    @property
    def successful(self):
        '''Returns a boolean, indicating whether the current
        `VowsResult` was 100% successful.

        '''
        return self.successful_tests + self.skipped_tests == self.total_test_count

    @property
    def total_test_count(self):
        '''Returns the total number of tests.'''
        return self.successful_tests + self.errored_tests + self.skipped_tests

    @staticmethod
    def test_is_successful(test):
        return not (test['error'] or test['skip'])

    @property
    def successful_tests(self):
        '''Returns the number of tests that passed.'''
        return self._count_contexts(
            contexts=self.contexts,
            count_func=lambda context: (
                len([t for t in context['tests'] if self.test_is_successful(t)])
                + (0 if (context['error'] or context['skip']) else 1)
            )
        )

    @property
    def errored_tests(self):
        '''Returns the number of tests that failed.'''
        return self._count_contexts(
            contexts=self.contexts,
            count_func=lambda context: (
                len([t for t in context['tests'] if t['error']])
                + (1 if context['error'] else 0)
            )
        )

    @property
    def skipped_tests(self):
        '''Returns the number of tests that were skipped'''
        return self._count_contexts(
            contexts=self.contexts,
            count_func=lambda context: (
                len([t for t in context['tests'] if t['skip']])
                + (1 if context['skip'] else 0)
            )
        )

    def eval_context(self, context):
        '''Returns a boolean indicating whether `context` tested
        successfully.

        '''
        succeeded = True

        # Success only if there wasn't an error in setup, topic or teardown
        succeeded = succeeded and (not context.get('error', None))

        # Success only if all subcontexts succeeded
        for context in context['contexts']:
            succeeded = succeeded and self.eval_context(context)

        # Success only if all tests succeeded
        for test in context['tests']:
            succeeded = succeeded and not test['error']

        return succeeded

    def get_worst_topics(self, number=10, threshold=0.1):
        '''Returns the top `number` slowest topics which took longer
        than `threshold` to test.

        '''
        times = [
            time for time in self._get_topic_times()
            if time['elapsed'] > 0 and time['elapsed'] >= threshold
        ]
        times.sort(key=lambda x: x['elapsed'], reverse=True)
        return times[:number]
