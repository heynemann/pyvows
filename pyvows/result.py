# -*- coding: utf-8 -*-
'''Contains `VowsResult` class, which collects the results of
each vow.

'''


# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

class VowsResult(object):
    '''Collects success/failure/total statistics (as well as elapsed
    time) for the outcomes of tests.

    '''

    def __init__(self):
        self.contexts = []
        self.elapsed_time = 0.0

    @property
    def successful(self):
        '''Returns a boolean, indicating whether the current
        `VowsResult` was 100% successful.

        '''
        return self.successful_tests == self.total_test_count

    @property
    def total_test_count(self):
        '''Returns the total number of tests.'''
        return self.count_tests(contexts=None, first=True, count_func=lambda test: 1)

    @property
    def successful_tests(self):
        '''Returns the number of tests that passed.'''
        return self.count_tests(contexts=None, first=True, count_func=lambda test: 1 if test['succeeded'] else 0)

    @property
    def errored_tests(self):
        '''Returns the number of tests that failed.'''
        return self.count_tests(contexts=None, first=True, count_func=lambda test: 0 if test['succeeded'] else 1)

    def count_tests(self, contexts=None, first=True, count_func=lambda test: 1):
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
            test_count += sum(map(count_func, context['tests']))
            test_count += self.count_tests(contexts=context['contexts'], first=False, count_func=count_func)

        return test_count

    def eval_context(self, context):
        '''Returns a boolean indicating whether `context` tested
        successfully.

        '''
        succeeded = True
        for context in context['contexts']:
            succeeded = succeeded and self.eval_context(context)

        for test in context['tests']:
            succeeded = succeeded and test['succeeded']

        return succeeded

    def get_topic_times(self, contexts=None):
        '''Returns a dict describing how long testing took for
        each topic in `contexts`.

        '''
        topic_times = []

        if contexts is None:
            contexts = self.contexts

        for context in contexts:
            topic_times.append({
                'context': context['name'],
                'path': context['filename'],
                'elapsed': context['topic_elapsed']
            })

            topic_times.extend(self.get_topic_times(context['contexts']))

        return topic_times

    def get_worst_topics(self, number=10, threshold=0.1):
        '''Returns the top `number` slowest topics which took longer
        than `threshold` to test.

        '''
        times = [time for time in self.get_topic_times() if time['elapsed'] > 0 and time['elapsed'] >= threshold]
        return list(reversed(sorted(times, key=lambda x: x['elapsed'])))[:number]

