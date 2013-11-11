# -*- coding: utf-8 -*-
'''Abstract base class for all PyVows Runner implementations.'''
 
 
# pyvows testing engine
# https://github.com/heynemann/pyvows
 
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com
 
import re, sys, time
 
from pyvows.runner.utils import get_code_for, get_file_info_for, get_topics_for
from pyvows.utils import elapsed

#-------------------------------------------------------------------------------------------------

class VowsRunnerABC(object):
     
    def __init__(self, suites, context_class, on_vow_success, on_vow_error, exclusion_patterns):
        self.suites = suites  # a suite is a file with pyvows tests
        self.context_class = context_class
        self.on_vow_success = on_vow_success
        self.on_vow_error = on_vow_error
        self.exclusion_patterns = exclusion_patterns
        if self.exclusion_patterns:
            self.exclusion_patterns = set([re.compile(x) for x in self.exclusion_patterns])
 
    def is_excluded(self, name):
        '''Return whether `name` is in `self.exclusion_patterns`.'''
        for pattern in self.exclusion_patterns:
            if pattern.search(name):
                return True
        return False
         
    def run(self):
        pass
     
    def run_context(self):
        pass
     
    def run_vow(self, tests_collection, topic, ctx_obj, vow, vow_name, enumerated):
        #   FIXME: Add Docstring
 
        start_time = time.time()
        filename, lineno = get_file_info_for(vow._original)
 
        vow_result = {
            'context_instance': ctx_obj,
            'name': vow_name,
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
            result = vow(ctx_obj, topic)
            vow_result['result'] = result
            vow_result['succeeded'] = True
            if self.on_vow_success:
                self.on_vow_success(vow_result)
 
        except:
            #   FIXME:
            #
            #   Either...
            #       *   Describe why we're catching every exception, or
            #       *   Fix to catch specific kinds of exceptions
            err_type, err_value, err_traceback = sys.exc_info()
            vow_result['error'] = {
                'type': err_type,
                'value': err_value,
                'traceback': err_traceback
            }
            if self.on_vow_error:
                self.on_vow_error(vow_result)
 
        vow_result['elapsed'] = elapsed(start_time)
        tests_collection.append(vow_result)
 
        return vow_result


class VowsTopicError(Exception):
    """Wraps an error in the setup or topic functions."""
    def __init__(self, source, exc_info):
        self.source = source
        self.exc_info = exc_info
