# -*- coding: utf-8 -*-
'''The GEvent implementation of PyVows runner.'''


# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from __future__ import absolute_import

import inspect
import sys
import time
import re

from gevent.pool import Pool

from pyvows.async_topic import VowsAsyncTopic, VowsAsyncTopicValue
from pyvows.decorators import FunctionWrapper
from pyvows.utils import elapsed
from pyvows.runner.abc import VowsRunnerABC
from pyvows.runner.utils import get_code_for, get_file_info_for, get_topics_for

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
        self.pool.spawn(
            self._run_context,
            ctx_collection,
            ctx_obj  = ctx_obj,
            index    = -1,
            suite    = suite
        )


    def _run_context(self, ctx_collection, ctx_obj=None, index=-1, suite=None):
        #   FIXME: Add Docstring
        
        ctx_name = type(ctx_obj).__name__
        if self._is_excluded(ctx_name):
            return

        #-----------------------------------------------------------------------
        # Local variables and defs
        #-----------------------------------------------------------------------
        ctx_result = {
            'filename': suite or inspect.getsourcefile(ctx_obj.__class__),
            'name': ctx_name,
            'tests': [],
            'contexts': [],
            'topic_elapsed': 0,
        }

        ctx_collection.append(ctx_result)
        ctx_obj.index = index
        ctx_obj.pool = self.pool
        
        def _run_setup_and_topic(ctx_obj):
            try:
                ctx_obj.setup()
            except Exception as e:
                topic = e
                topic.error = ctx_obj.topic_error = ('setup', sys.exc_info())
            else:  # setup() had no errors
                topic = None
                if not hasattr(ctx_obj, 'topic'): # ctx_obj has no topic
                    topic = ctx_obj._get_first_available_topic(index)
                else:
                    start_time = time.time()
                    try:
                        topic_func = getattr(ctx_obj, 'topic')
                        topic_list = get_topics_for(topic_func, ctx_obj)
                        topic = topic_func(*topic_list)
                    except Exception as e:
                        topic = e
                        topic.error = ctx_obj.topic_error = sys.exc_info()
                    ctx_result['topic_elapsed'] = elapsed(start_time)
            finally:
                return topic
        def _run_tests(topic):
            def _run_with_topic(topic):
                def _run_vows_and_subcontexts(topic, index=-1, enumerated=False):
                    # methods
                    for vow_name, vow in vows:
                        self._run_vow(
                            ctx_result['tests'],
                            topic,
                            ctx_obj,
                            teardown.wrap(vow),
                            vow_name,
                            enumerated=enumerated)

                    # classes
                    for subctx_name, subctx in subcontexts:
                        # resolve user-defined Context classes
                        if not issubclass(subctx, self.context_class):
                            subctx = type(ctx_name, (subctx, self.context_class), {})

                        subctx_obj = subctx(ctx_obj)
                        subctx_obj.pool = self.pool
                        subctx_obj.teardown = teardown.wrap(subctx_obj.teardown)

                        self.run_context(
                            ctx_result['contexts'],
                            ctx_obj=subctx_obj,
                            index=index,
                            suite=suite or ctx_result['filename']
                        )

                
                ctx_obj.topic_value = topic
                is_generator = inspect.isgenerator(topic)

                # setup generated topics if needed
                if is_generator:
                    try:
                        ctx_obj.generated_topic = True
                        ctx_obj.topic_value = tuple(topic)
                    except Exception as e:
                        is_generator = False
                        topic = ctx_obj.topic_value = e
                        topic.error = ctx_obj.topic_error = sys.exc_info()

                topic = ctx_obj.topic_value

                if is_generator:
                    for index, topic_value in enumerate(topic):
                        _run_vows_and_subcontexts(topic_value, index=index, enumerated=True)
                else:
                    _run_vows_and_subcontexts(topic)

                if hasattr(topic, 'error'):
                    ctx_obj.topic_error = topic.error
            
            vows, subcontexts = self._get_vows_and_subcontexts(ctx_obj)

            if not isinstance(topic, VowsAsyncTopic):
                _run_with_topic(topic)
            else:
                def handle_callback(*args, **kw):
                    _run_with_topic(VowsAsyncTopicValue(args, kw))
                topic(handle_callback)
        def _run_teardown(topic):
            try:
                teardown()
            except Exception as e:
                topic = e
                topic.error = ctx_obj.topic_error = ('teardown', sys.exc_info())


        #-----------------------------------------------------------------------
        # Begin
        #-----------------------------------------------------------------------
        teardown = FunctionWrapper(ctx_obj.teardown)  # Wrapped teardown so it's called at the appropriate time
        
        topic = _run_setup_and_topic(ctx_obj)
        _run_tests(topic)
        _run_teardown(topic)

    def _run_vow(self, tests_collection, topic, ctx_obj, vow, vow_name, enumerated=False):
        #   FIXME: Add Docstring
        if self._is_excluded(vow_name):
            return
        self.pool.spawn(self.run_vow, tests_collection, topic, ctx_obj, vow, vow_name, enumerated)