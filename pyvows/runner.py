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

try:
    from Queue import Queue
    from threading import Thread
    HAS_PARALLEL = True
except ImportError:
    HAS_PARALLEL = False

from pyvows.result import VowsResult

class VowsRunner(object):
    def __init__(self, vows, context_class):
        self.vows = vows
        self.context_class = context_class

    def run(self):
        start_time = time.time()
        result = VowsResult()
        context_col = result.contexts

        for key, value in self.vows.iteritems():
            self.run_context(context_col, key, value)

        end_time = time.time()
        result.ellapsed_time = float(end_time - start_time)
        return result

    def run_context(self, context_col, key, value, topics=[]):
        context_col[key] = {
            'contexts': {},
            'tests': []
        }

        value_instance = value()

        topic = None
        try:
            if hasattr(value_instance, 'topic'):
                topic_func = getattr(value_instance, 'topic')
                topic = topic_func(*copy.deepcopy(self.pop_topics(topics, num=topic_func.func_code.co_argcount - 1)))
                topics.append(topic)
            else:
                last_topic = copy.deepcopy(self.pop_topics(topics))
                topic = last_topic[0] if len(last_topic) else None
                topics.append(None)
        except Exception, err:
            topic = err

        for member_name, member in inspect.getmembers(value):
            if inspect.isclass(member) and issubclass(member, self.context_class):
                self.run_context(context_col[key]['contexts'], member_name, member, copy.deepcopy(topics))
                continue

            if inspect.ismethod(member) and member_name == 'topic':
                continue

            if inspect.ismethod(member):
                result_obj = {
                    'name': member_name,
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

                context_col[key]['tests'].append(result_obj)

    def run_topic(self, value_instance, last_topic=None):
        return topic

    def pop_topics(self, topics, num=1):
        older_topics = []
        if topics:
            for topic in topics[::-1]:
                if topic and len(older_topics) < num:
                    older_topics.append(topic)
        return older_topics

class VowsParallelRunner(object):
    def __init__(self, vows, context_class):
        self.vows = vows
        self.context_class = context_class
        self.queue = Queue()

    def worker(self):
        while True:
            item = self.queue.get()

            if item[0] == 'context':
                self.run_context(item)
            elif item[0] == 'vow':
                self.run_vow(item)

            self.queue.task_done()

    def run(self):
        start_time = time.time()
        result = VowsResult()

        for i in range(1):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

        for name, context in self.vows.iteritems():
            self.queue.put(('context', result.contexts, name, context, None))

        self.queue.join()

        end_time = time.time()
        result.ellapsed_time = float(end_time - start_time)
        return result

    def run_context(self, item):
        operation, context_col, key, value, parent = item

        context_col[key] = {
            'contexts': {},
            'tests': []
        }

        value_instance = value(parent)

        topic = None
        if hasattr(value_instance, 'topic'):
            try:
                topic_func = getattr(value_instance, 'topic')
                topic_list = self.get_topics_for(topic_func, value_instance)
                topic = topic_func(*topic_list)
            except Exception, err:
                topic = err
        else:
            topic = copy.deepcopy(value_instance._get_first_available_topic())

        value_instance.topic_value = topic

        for member_name, member in inspect.getmembers(value):
            if inspect.isclass(member) and issubclass(member, self.context_class):
                self.queue.put(('context', context_col[key]['contexts'], member_name, member, value_instance))
                continue

            if inspect.ismethod(member) and member_name == 'topic':
                continue

            if not member_name.startswith('_') and inspect.ismethod(member):
                self.queue.put(('vow', context_col[key]['tests'], topic, value_instance, member, member_name))

    def run_vow(self, item):
        operation, tests_col, topic, value_instance, member, member_name = item
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
            result = member(value_instance, topic)
            result_obj['result'] = result
            result_obj['succeeded'] = True
        except Exception, err:
            result_obj['error'] = err

        tests_col.append(result_obj)

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
        print expected_args

        topics = []

        context = context_instance.parent
        for i in range(expected_args):
            if not context.parent:
                break
            topics.append(copy.deepcopy(context.topic_value))
            context = context.parent

        return topics

