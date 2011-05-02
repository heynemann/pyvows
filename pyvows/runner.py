#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys
import inspect
import time
import copy

import eventlet

from pyvows.result import VowsResult

class VowsParallelRunner(object):
    def __init__(self, vows, context_class, async_topic_class, vow_successful_event, vow_error_event):
        self.vows = vows
        self.context_class = context_class
        self.async_topic_class = async_topic_class
        self.pool = eventlet.GreenPool()
        self.async_topics= []
        self.vow_successful_event = vow_successful_event
        self.vow_error_event = vow_error_event

    def run(self):
        start_time = time.time()
        result = VowsResult()

        for name, context in self.vows.iteritems():
            self.run_context(result.contexts, name, context, None)

        self.pool.waitall()

        while self.async_topics:
            time.sleep(0.01)

        self.pool.waitall()

        end_time = time.time()
        result.ellapsed_time = float(end_time - start_time)
        return result

    def run_context(self, context_col, name, context, parent):
        def async_run_context(self, context_col, name, context, parent):
            context_col[name] = {
                'contexts': {},
                'tests': []
            }

            context_instance = context(parent)

            topic = None
            if hasattr(context_instance, 'topic'):
                try:
                    topic_func = getattr(context_instance, 'topic')
                    topic_list = self.get_topics_for(topic_func, context_instance)
                    topic = topic_func(*topic_list)
                except Exception:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    topic = exc_value
                    context_instance.topic_error = (exc_type, exc_value, exc_traceback)
            else:
                topic = copy.deepcopy(context_instance._get_first_available_topic())

            def run_with_topic(topic, enumerated=False):
                context_instance.topic_value = topic

                def iterate_members(topic):
                    for member_name, member in inspect.getmembers(context):
                        if inspect.ismethod(member) and member_name == 'topic':
                            continue

                        if not member_name.startswith('_') and inspect.ismethod(member):
                            self.run_vow(context_col[name]['tests'], topic, context_instance, member, member_name, enumerated=True)

                    for member_name, member in inspect.getmembers(context):
                        if inspect.ismethod(member) and member_name == 'topic':
                            continue

                        if inspect.isclass(member) and issubclass(member, self.context_class):
                            self.pool.spawn_n(async_run_context, self, context_col[name]['contexts'], member_name, member, context_instance)
                            continue


                if inspect.isgenerator(topic):
                    for topic_value in topic:
                        iterate_members(topic_value)
                else:
                    iterate_members(topic)

            if isinstance(topic, self.async_topic_class):
                def handle_callback(topic_value):
                    run_with_topic(topic_value, enumerated=True)
                    self.async_topics.pop()

                args = topic.args + (handle_callback, )

                self.async_topics.append(topic)
                self.pool.spawn_n(topic.func, *args, **topic.kw)
            else:
                run_with_topic(topic)


        self.pool.spawn_n(async_run_context, self, context_col, name, context, parent)

    def run_vow(self, tests_col, topic, context_instance, member, member_name, enumerated=False):
        def async_run_vow(self, tests_col, topic, context_instance, member, member_name):
            filename, lineno = self.file_info_for(member)
            result_obj = {
                'context_instance': context_instance,
                'name': member_name if not enumerated else '%s - %s' % (str(topic), member_name),
                'result': None,
                'topic': topic,
                'error': None,
                'succeeded': False,
                'file': filename,
                'lineno': lineno
            }
            try:
                result = member(context_instance, topic)
                result_obj['result'] = result
                result_obj['succeeded'] = True
                if self.vow_successful_event:
                    self.vow_successful_event(result_obj)
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()

                result_obj['error'] = {
                    'type': exc_type,
                    'value': exc_value,
                    'traceback': exc_traceback
                }
                if self.vow_error_event:
                    self.vow_error_event(result_obj)
 
            tests_col.append(result_obj)

        self.pool.spawn_n(async_run_vow, self, tests_col, topic, context_instance, member, member_name)

    def file_info_for(self, member):
        if hasattr(member, '__code__'):
            code = member.__code__
        elif hasattr(member, '__func__'):
            code = member.__func__.__code__

        filename = code.co_filename
        lineno = code.co_firstlineno

        return filename, lineno

    def get_topics_for(self, topic_function, context_instance):
        if not context_instance.parent:
            return []

        if hasattr(topic_function, '__code__'):
            code = topic_function.__code__
        elif hasattr(topic_function, '__func__'):
            code = topic_function.__func__.__code__

        if not code:
            raise RuntimeError('Function %s does not have a code property')

        expected_args = code.co_argcount - 1

        topics = []

        context = context_instance.parent
        for i in range(expected_args):
            topics.append(copy.deepcopy(context.topic_value))

            if not context.parent:
                break
 
            context = context.parent

        return topics

