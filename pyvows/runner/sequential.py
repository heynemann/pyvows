# -*- coding: utf-8 -*-
'''This is the slowest of PyVows' runner implementations.  But it's also dependency-free; thus, 
it's a universal fallback.  
 
'''

from pyvows.runner.abc import VowsRunnerABC
from pyvows.runner.utils import get_code_for, get_file_info_for, get_topics_for

#-------------------------------------------------------------------------------------------------

class VowsSequentialRunner(object):
     
    def run(self):
        pass
        #for suite, batches in self.suites.items():
        #    for batch in batches:
        #        self.run_context(batch.__name__, batch(None))
         
    def run_context(self, ctx_name, ctx_instance):
        pass
        # setup
        # teardown
        # topic
        # vows
        # subcontexts
        # teardown