# -*- coding: utf-8 -*-
'''This module contains the magic that makes PyVows run its tests *fast*.

Contains the classes `VowsParallelRunner` and `FunctionWrapper`.
'''


# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import inspect
import sys
import time
from functools import wraps

#import eventlet
from gevent.pool import Pool

from pyvows.result import VowsResult
from pyvows.async_topic import VowsAsyncTopic, VowsAsyncTopicValue


class VowsParallelRunner(object):
    #   FIXME: Add Docstring

    def __init__(self, vows, context_class, vow_successful_event, vow_error_event):
        self.vows = vows
        self.context_class = context_class
        self.pool = Pool(1000)
        self.vow_successful_event = vow_successful_event
        self.vow_error_event = vow_error_event

    def run(self):
        #   FIXME: Add Docstring

        start_time = time.time()
        result = VowsResult()

        for name, context in self.vows.iteritems():
            self.run_context(result.contexts, name, context(None))

        self.pool.join()

        end_time = time.time()
        result.elapsed_time = float(end_time - start_time)
        return result

    def run_context(self, context_col, name, context_instance):
        #   FIXME: Add Docstring
        self.pool.spawn(self.async_run_context, context_col, name, context_instance)

    def async_run_context(self, context_col, name, context_instance, index=-1):
        #   FIXME: Add Docstring

        context_obj = {
            'name': name,
            'topic_elapsed': 0,
            'contexts': [],
            'tests': [],
            'filename': inspect.getsourcefile(context_instance.__class__)
        }
        context_col.append(context_obj)

        context_instance.index = index
        context_instance.pool = self.pool
        try:
            context_instance.setup()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            topic = exc_value
            error = ("setup", exc_type, exc_value, exc_traceback)
            topic.error = error
            context_instance.topic_error = error
        else:
            topic = None
            if hasattr(context_instance, 'topic'):
                start_time = time.time()
                try:
                    topic_func = getattr(context_instance, 'topic')
                    topic_list = self.get_topics_for(topic_func, context_instance)
                    topic = topic_func(*topic_list)
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    topic = exc_value
                    error = (exc_type, exc_value, exc_traceback)
                    topic.error = error
                    context_instance.topic_error = error

                context_obj['topic_elapsed'] = float(round(time.time() - start_time, 6))
            else:
                topic = context_instance._get_first_available_topic(index)

        teardown = FunctionWrapper(context_instance.teardown)

        def run_with_topic(topic):
            context_instance.topic_value = topic

            is_generator = inspect.isgenerator(topic)
            if is_generator:
                try:
                    context_instance.topic_value = list(topic)
                    context_instance.generated_topic = True
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    topic = exc_value
                    error = (exc_type, exc_value, exc_traceback)
                    topic.error = error
                    context_instance.topic_error = error
                    context_instance.topic_value = topic

            topic = context_instance.topic_value

            special_names = set(('setup', 'teardown', 'topic'))
            if hasattr(context_instance, 'ignored_members'):
                special_names.update(context_instance.ignored_members)

            context_members = filter(
                lambda member: not (member[0] in special_names or member[0].startswith('_')),
                inspect.getmembers(type(context_instance))
            )

            def iterate_members(topic, index=-1, enumerated=False):
                for member_name, member in context_members:
                    if inspect.ismethod(member):
                        self.run_vow(context_obj['tests'], topic, context_instance, teardown.wrap(member), member_name, enumerated=enumerated)

                for member_name, member in context_members:
                    if inspect.isclass(member):
                        if not issubclass(member, self.context_class):
                            member = type(name, (member, self.context_class), {})

                        child_context_instance = member(context_instance)
                        child_context_instance.pool = self.pool
                        child_context_instance.teardown = teardown.wrap(child_context_instance.teardown)
                        self.pool.spawn(self.async_run_context,
                            context_obj['contexts'], member_name, child_context_instance, index
                        )

            if is_generator:
                for index, topic_value in enumerate(topic):
                    iterate_members(topic_value, index, enumerated=True)
            else:
                iterate_members(topic)

            if hasattr(topic, 'error'):
                context_instance.topic_error = topic.error

        if isinstance(topic, VowsAsyncTopic):
            def handle_callback(*args, **kw):
                run_with_topic(VowsAsyncTopicValue(args, kw))

            topic(handle_callback)
        else:
            run_with_topic(topic)

        try:
            teardown()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            topic = exc_value
            error = ("teardown", exc_type, exc_value, exc_traceback)
            topic.error = error
            context_instance.topic_error = error

    def run_vow(self, tests_col, topic, context_instance, member, member_name, enumerated=False):
        #   FIXME: Add Docstring
        self.pool.spawn(self.async_run_vow, tests_col, topic, context_instance, member, member_name, enumerated)

    def async_run_vow(self, tests_col, topic, context_instance, member, member_name, enumerated):
        #   FIXME: Add Docstring

        start_time = time.time()
        filename, lineno = self.file_info_for(member._original)
        result_obj = {
            'context_instance': context_instance,
            'name': member_name,
            'enumerated': enumerated,
            'result': None,
            'topic': topic,
            'error': None,
            'succeeded': False,
            'file': filename,
            'lineno': lineno,
            'elapsed': 0
        }

        try:
            result = member(context_instance, topic)
            result_obj['result'] = result
            result_obj['succeeded'] = True
            if self.vow_successful_event:
                self.vow_successful_event(result_obj)

        except Exception:
            #   FIXME:
            #
            #   Either...
            #       *   Describe why we're catching every exception, or
            #       *   Fix to catch specific kinds of exceptions
            exc_type, exc_value, exc_traceback = sys.exc_info()

            result_obj['error'] = {
                'type': exc_type,
                'value': exc_value,
                'traceback': exc_traceback
            }
            if self.vow_error_event:
                self.vow_error_event(result_obj)

        result_obj['elapsed'] = time.time() - start_time
        tests_col.append(result_obj)

        return result_obj

    def _get_code_for(self, obj):
        #   FIXME: Add Comment description
        code = None
        if hasattr(obj, '__code__'):
            code = obj.__code__
        elif hasattr(obj, '__func__'):
            code = obj.__func__.__code__
        return code

    def file_info_for(self, member):
        #   FIXME: Add Docstring
        code = self._get_code_for(member)

        filename = code.co_filename
        lineno = code.co_firstlineno

        return filename, lineno

    def get_topics_for(self, topic_function, context_instance):
        #   FIXME: Add Docstring
        if not context_instance.parent:
            return []

        async = False
        if hasattr(topic_function, '_original'):
            topic_function = topic_function._original
            async = True

        code = self._get_code_for(topic_function)

        if not code:
            raise RuntimeError('Function %s does not have a code property')

        expected_args = code.co_argcount - 1

        # taking the callback argument into consideration
        if async:
            expected_args -= 1

        topics = []

        child = context_instance
        context = context_instance.parent
        for i in range(expected_args):
            if context.generated_topic:
                topics.append(context.topic_value[child.index])
            else:
                topics.append(context.topic_value)

            if not context.parent:
                break

            context = context.parent
            child = child.parent

        return topics


class FunctionWrapper(object):
    ''' Just calls the passed function when all the wrapped
        functions have been called.

    '''
    def __init__(self, func):
        self.waiting = 0
        self.func = func

    def wrap(self, method):
        self.waiting += 1

        @wraps(method)
        def wrapper(*args, **kw):
            try:
                ret = method(*args, **kw)
                return ret
            finally:
                self.waiting -= 1
                self()

        wrapper._original = method
        return wrapper

    def __call__(self):
        if self.waiting == 0:
            self.func()

