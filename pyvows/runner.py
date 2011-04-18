#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import inspect
import time

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
                if not topic:
                    continue
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

