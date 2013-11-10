# -*- coding: utf-8 -*-
'''Contains `VowsResult` class, which collects the results of
each vow.

'''

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

#-------------------------------------------------------------------------------------------------

class VowsResult(object):
    '''Collects success/failure/total statistics (as well as elapsed
    time) for the outcomes of tests.

    Only one instance of this class is created when PyVows is run.

    '''

    def __init__(self):
        self.contexts = []
        self.elapsed_time = 0.0

    def _count_tests(self, contexts=None, first=True, count_func=lambda test: 1):
        '''Used interally for class properties
        `total_test_count`, `successful_tests`, and `errored_tests`.

        '''
        #   TODO
        #       Reevaluate whether `count_func` should have a default value
        #       (AFAICT the default is never used. It makes more sense
        #       to me if it had no default, or defaulted to `None`.
        test_count = 0

        if first:
            contexts = self.contexts

        for context in contexts:
            test_count += sum([count_func(i) for i in context['tests']])
            test_count += self._count_tests(contexts=context['contexts'],
                                            first=False,
                                            count_func=count_func)

        return test_count

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
        return self.successful_tests == self.total_test_count

    @property
    def total_test_count(self):
        '''Returns the total number of tests.'''
        return self._count_tests(contexts=None, first=True, count_func=lambda test: 1)

    @property
    def successful_tests(self):
        '''Returns the number of tests that passed.'''
        return self._count_tests(contexts=None, first=True, count_func=lambda test: 1 if test['succeeded'] else 0)

    @property
    def errored_tests(self):
        '''Returns the number of tests that failed.'''
        return self._count_tests(contexts=None, first=True, count_func=lambda test: 0 if test['succeeded'] else 1)

    def eval_context(self, context):
        '''Returns a boolean indicating whether `context` tested
        successfully.

        '''
        # Didn't succeed if there was an error in setup, topic or teardown
        if context.get('error', None):
            return False

        for context in context['contexts']:
            if not self.eval_context(context): return False

        for test in context['tests']:
            if not test['succeeded']: return False

        return True

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
