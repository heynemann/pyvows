# -*- coding: utf-8 -*-
'''The GEvent implementation of PyVows runner.'''


# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from __future__ import absolute_import

import time

from gevent.pool import Pool

from pyvows.utils import elapsed
from pyvows.runner.abc import VowsRunnerABC

#-------------------------------------------------------------------------------------------------

class VowsParallelRunner(VowsRunnerABC):
    #   FIXME: Add Docstring

    # Class is called from `pyvows.core:Vows.run()`,
    # which is called from `pyvows.cli.run()`

    pool = Pool(1000)

    def run(self):
        start_time = time.time()
        super(VowsParallelRunner, self).run()
        self.pool.join()
        self.result.elapsed_time = elapsed(start_time)
        return self.result
        
    def run_context(self, ctx_collection, ctx_obj=None, index=-1, suite=None):
        ctx_obj.pool = self.pool
        run_context = super(VowsParallelRunner, self).run_context
        self.pool.spawn(
            run_context,
            ctx_collection,
            ctx_obj  = ctx_obj,
            index    = -1,
            suite    = suite
        )

    def run_vow(self, tests_collection, topic, ctx_obj, vow, vow_name, enumerated=False):
        #   FIXME: Add Docstring
        
        # Same as the parent class' method, but called via self.pool 
        self.pool.spawn(
            super(VowsParallelRunner, self).run_vow, 
            tests_collection, 
            topic, 
            ctx_obj,
            vow, 
            vow_name, 
            enumerated
        )