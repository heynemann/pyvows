#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

class VowsResult(object):
    def __init__(self):
        self.contexts = []
        self.ellapsed_time = 0.0

    @property
    def successful(self):
        return self.successful_tests == self.total_test_count

    @property
    def total_test_count(self):
        return self.count_tests(contexts=None, first=True, count_func=lambda test: 1)

    @property
    def successful_tests(self):
        return self.count_tests(contexts=None, first=True, count_func=lambda test: 1 if test['succeeded'] else 0)

    @property
    def errored_tests(self):
        return self.count_tests(contexts=None, first=True, count_func=lambda test: 0 if test['succeeded'] else 1)

    def count_tests(self, contexts=None, first=True, count_func=lambda test: 1):
        test_count = 0

        if first:
            contexts = self.contexts

        for context in contexts:
            test_count += sum(map(count_func, context['tests']))
            test_count += self.count_tests(contexts=context['contexts'], first=False, count_func=count_func)

        return test_count

    def eval_context(self, context):
        succeeded = True
        for context in context['contexts']:
            succeeded = succeeded and self.eval_context(context)

        for test in context['tests']:
            succeeded = succeeded and test['succeeded']

        return succeeded

    def get_topic_times(self, contexts=None):
        topic_times = []

        if contexts is None:
            contexts = self.contexts

        for context in contexts:
            topic_times.append({
                'context': context['name'],
                'path': context['filename'],
                'ellapsed': context['topic_ellapsed']
            })

            topic_times.extend(self.get_topic_times(context['contexts']))

        return topic_times

    def get_worst_topics(self, number=10):
        times = [time for time in self.get_topic_times() if time['ellapsed'] > 0]
        return list(reversed(sorted(times, key=lambda x: x['ellapsed'])))[:number]

