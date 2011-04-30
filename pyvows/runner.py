#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import inspect
import time
import copy

import eventlet

from pyvows.result import VowsResult

class VowsParallelRunner(object):
    def __init__(self, vows, context_class, async_topic_class):
        self.vows = vows
        self.context_class = context_class
        self.async_topic_class = async_topic_class
        self.pool = eventlet.GreenPool()

    def run(self):
        start_time = time.time()
        result = VowsResult()

        for name, context in self.vows.iteritems():
            self.run_context(result.contexts, name, context, None)

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
                except Exception, err:
                    topic = err
            else:
                topic = copy.deepcopy(context_instance._get_first_available_topic())

            def run_with_topic(topic):
                context_instance.topic_value = topic

                for member_name, member in inspect.getmembers(context):
                    if inspect.isclass(member) and issubclass(member, self.context_class):
                        self.pool.spawn_n(async_run_context, self, context_col[name]['contexts'], member_name, member, context_instance)
                        continue

                    if inspect.ismethod(member) and member_name == 'topic':
                        continue

                    if not member_name.startswith('_') and inspect.ismethod(member):
                        self.run_vow(context_col[name]['tests'], topic, context_instance, member, member_name)

            if isinstance(topic, self.async_topic_class):
                args = topic.args + (run_with_topic, )
                self.pool.spawn(topic.func, *args, **topic.kw)
            else:
                run_with_topic(topic)

        self.pool.spawn_n(async_run_context, self, context_col, name, context, parent)

    def run_vow(self, tests_col, topic, context_instance, member, member_name):
        def async_run_vow(self, tests_col, topic, context_instance, member, member_name):
            filename, lineno = self.file_info_for(member)
            result_obj = {
                'name': member_name,
                'result': None,
                'error': None,
                'succeeded': False,
                'file': filename,
                'lineno': lineno
            }
            try:
                result = member(context_instance, topic)
                result_obj['result'] = result
                result_obj['succeeded'] = True
            except Exception, err:
                result_obj['error'] = err

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
            if not context.parent:
                break
            topics.append(copy.deepcopy(context.topic_value))
            context = context.parent

        return topics

