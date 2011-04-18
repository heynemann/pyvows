#!/usr/bin/env python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import inspect

class Vows(object):
    __current_vows__ = {}

    class Context(object):
        pass

    class Assert(object):
        pass

    @classmethod
    def batch(cls, method):
        def method_name(*args, **kw):
            method(*args, **kw)
        Vows.__current_vows__[method.__name__] = method
        return method_name

    @classmethod
    def assertion(cls, method):
        def method_name(*args, **kw):
            method(*args, **kw)
        @classmethod
        def exec_assertion(cls, *args, **kw):
            return method_name(*args, **kw)
        setattr(Vows.Assert, method.__name__, exec_assertion)
        return method_name

    @classmethod
    def ensure(cls):
        runner = VowsRunner(cls.__current_vows__)

        result = runner.run()

        cls.__current_vows__ = {}

        return result

class VowsRunner(object):
    def __init__(self, vows):
        self.vows = vows

    def run(self):
        result = VowsResult()
        context_col = result.contexts
        for key, value in self.vows.iteritems():
            self.run_context(context_col, key, value)
        return result

    def run_context(self, context_col, key, value):
        context_col[key] = {
            'contexts': {},
            'tests': []
        }

        topic = None
        value_instance = value()
        for member_name, member in inspect.getmembers(value):
            if inspect.isclass(member) and issubclass(member, Vows.Context):
                self.run_context(context_col, member_name, member)
                continue

            if inspect.ismethod(member) and member_name == 'topic':
                topic = member(value_instance)
                continue

            if inspect.ismethod(member):
                result_obj = {
                    'method': member_name,
                    'result': None,
                    'error': None,
                    'succeeded': False
                }
                try:
                    result = member(value_instance, topic)
                    result_obj['result'] = result
                    result_obj['succeeded'] = True
                except Exception, err:
                    result_obj['error'] = err
                    result_obj['succeeded'] = False

                context_col[key]['tests'].append(result_obj)

class VowsResult(object):
    def __init__(self):
        self.contexts = {}

    @property
    def successful(self):
        succeeded = True
        for context in self.contexts.values():
            succeeded = succeeded and self.__eval_context(context)

        return succeeded

    def __eval_context(self, context):
        succeeded = True
        for context in context['contexts']:
            succeeded = succeeded and self.__eval_context(context)

        for test in context['tests']:
            succeeded = succeeded and test['succeeded']

        return succeeded
