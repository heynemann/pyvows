# -*- coding: utf-8 -*-
'''Contains `VowsResult` class, which collects the results of
each vow.

'''

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import inspect
import six

from pyvows import utils
from pyvows.runner import utils as runutils
#-------------------------------------------------------------------------------------------------
INDENT = '  '


class ContextResult(object):
    __slots__ = (
        '__name__',
        'ctx_object',
        'filename',
        'name',
        'tests',
        'contexts',
        'topic_elapsed',
        'parent'
    )

    def __init__(self, suite, ctx_obj):
        self.ctx_object = ctx_obj
        self.filename = suite
        self.name = self.__name__ = ctx_obj.__name__
        self.tests = []
        self.contexts = []
        self.topic_elapsed = 0.0
        if hasattr(ctx_obj, 'parent') and ctx_obj.parent is not None:
            self.parent = ctx_obj.parent

    def __bool__(self):
        '''Returns whether vows and contexts tested successfully.  Recursive.'''
        vows_passed = [bool(test) for test in self.tests]
        ctx_passed = [bool(ctx) for ctx in self.contexts]
        if all(vows_passed) and all(ctx_passed):
            return True
        return False

    def __nonzero__(self):
        return self.__bool__()
        
    def __str__(self):
        return self.name


class VowResult(object):
    __slots__ = (
        '__name__',
        'context_instance',
        'elapsed',
        'enumerated',
        'error',
        'file',
        'lineno',
        'name',
        'result',
        'succeeded',
        'topic'
    )

    def __init__(self, ctx_obj, vow, topic, enumerated=False):
        self.context_instance = ctx_obj
        self.name = self.__name__ = vow.__name__
        self.topic = topic
        self.file, self.lineno = runutils.get_file_info_for(vow._original)
        self.enumerated = enumerated
        #---- These begin the same ----#
        self.elapsed = 0.0
        self.error = None
        self.result = None
        self.succeeded = False

    def __bool__(self):
        return self.succeeded

    def __nonzero__(self):
        return self.__bool__()
        
    def __str__(self):
        return self.name


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
            test_count += sum([count_func(test) for test in context.tests])
            test_count += self._count_tests(contexts=context.contexts,
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
                'context'       : context.name,
                'file'          : context.filename,
                'topic_elapsed' : context.topic_elapsed
            })
            ctx_topic_times = self._get_topic_times(context.contexts)
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
        return self._count_tests(contexts=None, first=True, count_func=lambda test: 1 if bool(test) else 0)

    @property
    def errored_tests(self):
        '''Returns the number of tests that failed.'''
        return self._count_tests(contexts=None, first=True, count_func=lambda test: 0 if bool(test) else 1)

    def get_worst_topics(self, number=10, threshold=0.1):
        '''Returns the top `number` slowest topics which took longer
        than `threshold` to test.

        '''
        times = [
            time for time in self._get_topic_times()
            if time['topic_elapsed'] > 0 and time['topic_elapsed'] >= threshold
        ]
        times.sort(key=lambda x: x['topic_elapsed'], reverse=True)
        return times[:number]

    def eval_context(self, context):
        return bool(context)