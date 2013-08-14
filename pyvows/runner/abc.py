# -*- coding: utf-8 -*-
'''Abstract base class for all PyVows Runner implementations.'''

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import re, sys, time
import inspect

from pyvows.async_topic import VowsAsyncTopic, VowsAsyncTopicValue
from pyvows.decorators import FunctionWrapper
from pyvows.result import (
    VowResult,  # yeah, similar names.  will fix.
    VowsResult, 
    ContextResult
)
from pyvows.utils import elapsed
from pyvows.runner import utils as rutils

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

    def run(self):
        for suite, batches in self.suites.items():
            for batch in batches:
                self.run_context(
                    ctx_collection = self.result.contexts,
                    ctx_obj        = batch(None),
                    index          = -1
                )

    def run_context(self, ctx_collection, ctx_obj=None, index=-1):
        #-----------------------------------------------------------------------
        # Local variables and defs
        #-----------------------------------------------------------------------
        ctx_result = ContextResult(ctx_obj)
        ctx_collection.append(ctx_result)
        ctx_name = ctx_result.name
        ctx_obj.index = index
        teardown = FunctionWrapper(ctx_obj.teardown)  # Wrapped teardown so it's called at the appropriate time
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
                        topic_list = rutils.get_topics_for(topic_func, ctx_obj)
                        topic = topic_func(*topic_list)
                    except Exception as e:
                        topic = e
                        topic.error = ctx_obj.topic_error = sys.exc_info()
                    ctx_result.topic_elapsed = elapsed(start_time)
            finally:
                return topic
        def _run_tests(topic):
            def _run_with_topic(topic):
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

                def _run_vows_and_subcontexts(topic, index=-1, enumerated=False):
                    # methods
                    for vow in vows:
                        self.run_vow(
                            ctx_result.tests,
                            topic,
                            ctx_obj,
                            teardown.wrap(vow),
                            enumerated=enumerated)

                    # classes
                    for subctx in subcontexts:
                        # resolve user-defined Context classes
                        if not issubclass(subctx, self.context_class):
                            subctx = type(ctx_name, (subctx, self.context_class), {})

                        subctx_obj = subctx(ctx_obj)
                        subctx_obj.teardown = teardown.wrap(subctx_obj.teardown)

                        self.run_context(
                            ctx_result.contexts,
                            ctx_obj=subctx_obj,
                            index=index                        )                

                if is_generator:
                    for index, topic_value in enumerate(topic):
                        _run_vows_and_subcontexts(topic_value, index=index, enumerated=True)
                else:
                    _run_vows_and_subcontexts(topic)

                if hasattr(topic, 'error'):
                    ctx_obj.topic_error = topic.error

            vows, subcontexts = rutils.get_vows_and_subcontexts(ctx_obj, self.exclusion_patterns)

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
        topic = _run_setup_and_topic(ctx_obj)
        _run_tests(topic)
        _run_teardown(topic)

    def run_vow(self, tests_collection, topic, ctx_obj, vow, enumerated=False):
        #   FIXME: Add Docstring

        start_time = time.time()
        vow_result = VowResult(
            ctx_obj,
            vow,
            topic,
            enumerated=enumerated
        )

        try:
            vow_result.result = vow(ctx_obj, topic)
            vow_result.succeeded = True
            if self.on_vow_hooks[True]:
                self.on_vow_hooks[True](vow_result)
        except:
            #   FIXME:
            #
            #   Either...
            #       *   Describe why we're catching every exception, or
            #       *   Fix to catch specific kinds of exceptions
            err_type, err_value, err_traceback = sys.exc_info()
            vow_result.error = {
                'type': err_type,
                'value': err_value,
                'traceback': err_traceback
            }
            if self.on_vow_hooks[False]:
                self.on_vow_hooks[False](vow_result)

        vow_result.elapsed = elapsed(start_time)
        tests_collection.append(vow_result)
