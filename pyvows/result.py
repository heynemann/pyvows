#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

class VowsResult(object):
    def __init__(self):
        self.contexts = {}
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

        for context in contexts.values():
            test_count += sum(map(count_func, context['tests']))
            test_count += self.count_tests(contexts=context['contexts'], first=False, count_func=count_func)

        return test_count

    def __eval_context(self, context):
        succeeded = True
        for context in context['contexts'].values():
            succeeded = succeeded and self.__eval_context(context)

        for test in context['tests']:
            succeeded = succeeded and test['succeeded']

        return succeeded


