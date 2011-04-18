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
        succeeded = True
        for context in self.contexts.values():
            succeeded = succeeded and self.__eval_context(context)

        return succeeded

    @property
    def total_test_count(self, contexts=None):
        test_count = 0
        for context in contexts or self.contexts.values():
            test_count += len(context['tests'])
            test_count += self.total_test_count(context['contexts'])
        return test_count

    @property
    def successful_tests(self, contexts=None):
        test_count = 0
        for context in contexts or self.contexts.values():
            test_count += sum((test['successful'] and 1 or 0) for test in context['tests'])
            test_count += self.successful_tests(context['contexts'])
        return test_count

    @property
    def failed_tests(self, contexts=None):
        test_count = 0
        for context in contexts or self.contexts.values():
            test_count += sum((test['successful'] and 0 or 1) for test in context['tests'])
            test_count += self.failed_tests(context['contexts'])
        return test_count

    def __eval_context(self, context):
        succeeded = True
        for context in context['contexts']:
            succeeded = succeeded and self.__eval_context(context)

        for test in context['tests']:
            succeeded = succeeded and test['succeeded']

        return succeeded


