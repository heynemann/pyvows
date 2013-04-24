# -*- coding: utf-8 -*-
'''Abstract base class for all PyVows Runner implementations.'''


# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import re


class VowsRunnerABC(object):
    
    def __init__(self, suites, batches, context_class, on_vow_success, on_vow_error, exclusion_patterns):
        self.batches = batches  # a batch is just a "top-level context"
        self.context_class = context_class
        self.on_vow_success = on_vow_success
        self.on_vow_error = on_vow_error
        self.exclusion_patterns = exclusion_patterns
        if self.exclusion_patterns:
            self.exclusion_patterns = set([re.compile(x) for x in self.exclusion_patterns])
        self.suites = suites  # a suite is a file with pyvows tests
    
    def is_excluded(self, name):
        for pattern in self.exclusion_patterns:
            if pattern.search(name):
                return True
        return False
        
    def run(self):
        NotImplemented
    
    def run_context(self, ctx_name, *args, **kwargs):
        pass
    
    def run_vow(self):
        NotImplemented