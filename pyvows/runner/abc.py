# -*- coding: utf-8 -*-
'''Abstract base class for all PyVows Runner implementations.'''


# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import re, sys, time
import inspect

from pyvows.utils import elapsed
from pyvows.result import VowsResult
from pyvows.runner.utils import get_code_for, get_file_info_for, get_topics_for

#-------------------------------------------------------------------------------------------------

class VowsRunnerABC(object):
    result = VowsResult()
    
    def __init__(self, suites, context_class, on_vow_hooks, exclusion_patterns=None):
        self.suites = suites  # a suite is a file with pyvows tests
        self.context_class = context_class
        self.on_vow_hooks = on_vow_hooks
        self.exclusion_patterns = exclusion_patterns
        if self.exclusion_patterns:
            self.exclusion_patterns = set([re.compile(x) for x in self.exclusion_patterns])
    
    def _get_vows_and_subcontexts(self, ctx_obj):
        special_names = set(['setup', 'teardown', 'topic', 'ignore'])
        if hasattr(ctx_obj, 'ignored_members'):
            special_names.update(ctx_obj.ignored_members)
            
        # removes any special methods from ctx_members
        filterfunc = lambda member: not (
            member[0] in special_names  or 
            member[0].startswith('_')   or 
            self._is_excluded(member[0])
        )
        ctx_members = filter(filterfunc, inspect.getmembers(type(ctx_obj)))
        ctx_members = tuple(ctx_members)
        
        # now separate out the two types we're concerned with
        vows        = set((vow_name,vow) for vow_name, vow in ctx_members if inspect.ismethod(vow))
        subcontexts = set((subctx_name,subctx) for subctx_name, subctx in ctx_members if inspect.isclass(subctx))
        return vows, subcontexts
        
    def _is_excluded(self, name):
        '''Return whether `name` is in `self.exclusion_patterns`.'''
        for pattern in self.exclusion_patterns:
            if pattern.search(name):
                return True
        return False

    def run(self):
        for suite, batches in self.suites.items():
            for batch in batches:
                self.run_context(
                    ctx_collection = self.result.contexts,
                    ctx_obj        = batch(None),
                    index          = -1,
                    suite          = suite
                )

    def run_context(self, ctx_collection, ctx_obj=None, index=-1, suite=None):
        NotImplemented  # subclasses implement this

    def run_vow(self, tests_collection, topic, ctx_obj, vow, vow_name, enumerated):
        #   FIXME: Add Docstring

        start_time = time.time()
        filename, lineno = get_file_info_for(vow._original)

        vow_result = type(self.result).get_result_for_vow(
            context_instance = ctx_obj,
            name = vow_name,
            enumerated = enumerated,
            topic = topic,
            file = filename,
            lineno = lineno
        )

        try:
            vow_result['result'] = vow(ctx_obj, topic)
            vow_result['succeeded'] = True
            if self.on_vow_hooks[True]:
                self.on_vow_hooks[True](vow_result)

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
            if self.on_vow_hooks[False]:
                self.on_vow_hooks[False](vow_result)

        vow_result['elapsed'] = elapsed(start_time)
        tests_collection.append(vow_result)

        return vow_result