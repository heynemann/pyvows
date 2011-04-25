#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import inspect
import time

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

    def run_context(self, context_col, key, value):
        context_col[key] = {
            'contexts': {},
            'tests': []
        }

        value_instance = value()

        topic = value_instance.topic() if hasattr(value_instance, 'topic') else None

        for member_name, member in inspect.getmembers(value):
            if inspect.isclass(member) and issubclass(member, self.context_class):
                self.run_context(context_col[key]['contexts'], member_name, member)
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

        for i in range(4):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

        for name, context in self.vows.iteritems():
            self.queue.put(('context', result.contexts, name, context))

        self.queue.join()

        end_time = time.time()
        result.ellapsed_time = float(end_time - start_time)
        return result

    def run_context(self, item):
        operation, context_col, key, value = item

        context_col[key] = {
            'contexts': {},
            'tests': []
        }

        value_instance = value()

        try:
            topic = value_instance.topic() if hasattr(value_instance, 'topic') else None
        except Exception, err:
            topic = err

        for member_name, member in inspect.getmembers(value):
            if inspect.isclass(member) and issubclass(member, self.context_class):
                self.queue.put(('context', context_col[key]['contexts'], member_name, member))
                continue

            if inspect.ismethod(member) and member_name == 'topic':
                continue

            if inspect.ismethod(member):
                if not topic:
                    continue
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

