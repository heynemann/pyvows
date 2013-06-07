# -*- coding: utf-8 -*-
'''This is the slowest of PyVows' runner implementations.  But it's also dependency-free; thus,
it's a universal fallback.

'''
import time

from pyvows.utils import elapsed
from pyvows.runner.abc import VowsRunnerABC

#-------------------------------------------------------------------------------------------------

class VowsSequentialRunner(VowsRunnerABC):
    ### FIXME:
    ###
    ###   Not working yet. Known issues:
    ###
    ###     - Breaks for async topics (async_vows.py also REQUIRES the gevent runner; is that a bug???)
    ###     - Possible teardown issues (tests/no_subcontext_extension_vows.py)
    ###     - <add more as discovered>
    ###
    
    # def __init__(self, *args, **kw):
    #     # Debugging
    #     print 'Starting sequential runner...'
    #     super(VowsSequentialRunner, self).__init__(*args, **kw)
    
    def run(self):
        start_time = time.time()
        super(VowsSequentialRunner, self).run()
        self.result.elapsed_time = elapsed(start_time)
        return self.result
    