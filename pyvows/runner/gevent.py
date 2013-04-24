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
from pyvows.runner.utils import get_code_for, get_file_info_for, get_topics_for
from pyvows.result import VowsResult
from pyvows.utils import elapsed
from pyvows.runner.abc import VowsRunnerABC

class VowsParallelRunner(VowsRunnerABC):
    #   FIXME: Add Docstring

    # Class is called from `pyvows.core:Vows.run()`,
    # which is called from `pyvows.cli.run()`

    pool = Pool(1000)

    def run(self):
        #   FIXME: Add Docstring

        # called from `pyvows.core:Vows.run()`,
        # which is called from `pyvows.cli.run()`

        start_time = time.time()
        result = VowsResult()
        for ctx_name, context in self.batches.iteritems():
            self._run_context(result.contexts, ctx_name, context(None))
        self.pool.join()
        result.elapsed_time = elapsed(start_time)
        return result

    def _run_context(self, ctx_collection, ctx_name, ctx_instance):
        #   FIXME: Add Docstring
        self.pool.spawn(self.run_context, ctx_collection, ctx_name, ctx_instance)

    def run_context(self, ctx_collection, ctx_name, ctx_instance, index=-1):
        #   FIXME: Add Docstring
        
        if self.is_excluded(ctx_name):
            return

        #-----------------------------------------------------------------------
        # Local variables and defs
        #-----------------------------------------------------------------------
        ctx_result = {
            'name': ctx_name,
            'topic_elapsed': 0,
            'contexts': [],
            'tests': [],
            'filename': inspect.getsourcefile(ctx_instance.__class__)
        }

        ctx_collection.append(ctx_result)
        ctx_instance.index = index
        ctx_instance.pool = self.pool
        
        def _run_setup():
            # execute ctx_instance.setup()
            try:
                ctx_instance.setup()
            except Exception as e:
                topic = e
                error = ('setup', sys.exc_info())
                topic.error = ctx_instance.topic_error = error
            else:  # when no errors are raised
                topic = None

                if hasattr(ctx_instance, 'topic'):
                    start_time = time.time()
                    try:
                        topic_func = getattr(ctx_instance, 'topic')
                        topic_list = get_topics_for(topic_func, ctx_instance)
                        topic = topic_func(*topic_list)
                    except Exception as e:
                        topic = e
                        topic.error = ctx_instance.topic_error = sys.exc_info()
                    ctx_result['topic_elapsed'] = elapsed(start_time)
                else:  # ctx_instance has no topic
                    topic = ctx_instance._get_first_available_topic(index)
            finally:
                return topic
        def _run_tests():
            # run the topic/async topic
            if isinstance(topic, VowsAsyncTopic):
                def handle_callback(*args, **kw):
                    _run_with_topic(VowsAsyncTopicValue(args, kw))
                topic(handle_callback)
            else:
                _run_with_topic(topic)
        def _run_teardown():
            try:
                teardown()
            except Exception as e:
                topic = e
                topic.error = ctx_instance.topic_error = ('teardown', sys.exc_info())

        def _run_with_topic(topic):
            ctx_instance.topic_value = topic

            # setup generated topics if needed
            is_generator = inspect.isgenerator(topic)
            if is_generator:
                try:
                    ctx_instance.topic_value = list(topic)
                    ctx_instance.generated_topic = True
                except Exception as e:
                    is_generator = False
                    topic = e
                    topic.error = ctx_instance.topic_error = sys.exc_info()
                    ctx_instance.topic_value = topic

            topic = ctx_instance.topic_value
            special_names = set(('setup', 'teardown', 'topic'))

            if hasattr(ctx_instance, 'ignored_members'):
                special_names.update(ctx_instance.ignored_members)

            # remove any special methods from context_members
            context_members = filter(
                lambda member: not (member[0] in special_names or member[0].startswith('_')),
                inspect.getmembers(type(ctx_instance))
            )

            def _iterate_members(topic, index=-1, enumerated=False):
                vows        = set((vow_name,vow)       for vow_name, vow       in context_members if inspect.ismethod(vow))
                subcontexts = set((subctx_name,subctx) for subctx_name, subctx in context_members if inspect.isclass(subctx))
                
                # methods
                for vow_name, vow in vows:
                    self._run_vow(
                        ctx_result['tests'],
                        topic,
                        ctx_instance,
                        teardown.wrap(vow),
                        vow_name,
                        enumerated=enumerated)
                
                # classes
                for subctx_name, subctx in subcontexts:
                    # resolve user-defined Context classes
                    if not issubclass(subctx, self.context_class):
                        subctx = type(ctx_name, (subctx, self.context_class), {})

                    subctx_instance = subctx(ctx_instance)
                    subctx_instance.pool = self.pool
                    subctx_instance.teardown = teardown.wrap(subctx_instance.teardown)
                    
                    self.pool.spawn(
                        self.run_context,
                        ctx_result['contexts'], 
                        subctx_name, 
                        subctx_instance, 
                        index
                    )

            if is_generator:
                for index, topic_value in enumerate(topic):
                    _iterate_members(topic_value, index, enumerated=True)
            else:
                _iterate_members(topic)

            if hasattr(topic, 'error'):
                ctx_instance.topic_error = topic.error

        #-----------------------------------------------------------------------
        # Begin
        #-----------------------------------------------------------------------
        topic = _run_setup()
        # Wrap teardown so it gets called at the appropriate time
        teardown = FunctionWrapper(ctx_instance.teardown)
        _run_tests()
        # execute teardown()
        _run_teardown()

    def _run_vow(self, tests_collection, topic, ctx_instance, vow, vow_name, enumerated=False):
        #   FIXME: Add Docstring
        if self.is_excluded(vow_name):    
            return
        self.pool.spawn(self.run_vow, tests_collection, topic, ctx_instance, vow, vow_name, enumerated)

    def run_vow(self, tests_collection, topic, ctx_instance, vow, vow_name, enumerated):
        #   FIXME: Add Docstring

        start_time = time.time()
        filename, lineno = get_file_info_for(vow._original)

        vow_result = {
            'context_instance': ctx_instance,
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
            result = vow(ctx_instance, topic)
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
