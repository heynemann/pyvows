# -*- coding: utf-8 -*-
'''This is the slowest of PyVows' runner implementations.  But it's also dependency-free; thus, 
it's a universal fallback.  

'''

from pyvows.runner.abc import VowsRunnerABC
from pyvows.runner.utils import get_code_for, get_file_info_for, get_topics_for


class VowsSequentialRunner(object):
    
    def run(self):
        for ctx_name, ctx_obj in self.batches:
            ...
        
    def run_context(self, ctx_name, ctx_instance):
        ctx_collection.append(context_obj)
            

            