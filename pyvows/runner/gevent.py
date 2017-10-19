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
try:
    from StringIO import StringIO
except:
    from io import StringIO
try:
    from colorama.ansitowin32 import AnsiToWin32
except ImportError:
    def AnsiToWin32(*args, **kwargs):
        return args[0]

from gevent.pool import Pool
import gevent.local

from pyvows.async_topic import VowsAsyncTopic, VowsAsyncTopicValue
from pyvows.runner.utils import get_topics_for
from pyvows.result import VowsResult
from pyvows.utils import elapsed
from pyvows.runner.abc import VowsRunnerABC, VowsTopicError
from pyvows.runner import SkipTest

#-----------------------------------------------------------------------------


class _LocalOutput(gevent.local.local):
    def __init__(self):
        self.__dict__['stdout'] = StringIO()
        self.__dict__['stderr'] = StringIO()


class _StreamCapture(object):
    def __init__(self, streamName):
        self.__streamName = streamName

    def __getattr__(self, name):
        return getattr(getattr(VowsParallelRunner.output, self.__streamName), name)


class VowsParallelRunner(VowsRunnerABC):
    #   FIXME: Add Docstring

    # Class is called from `pyvows.core:Vows.run()`,
    # which is called from `pyvows.cli.run()`

    output = _LocalOutput()
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    def __init__(self, *args, **kwargs):
        super(VowsParallelRunner, self).__init__(*args, **kwargs)
        self.pool = Pool(1000)

    def run(self):
        #   FIXME: Add Docstring

        # called from `pyvows.core:Vows.run()`,
        # which is called from `pyvows.cli.run()`

        start_time = time.time()
        result = VowsResult()
        if self.capture_output:
            self._capture_streams(True)
        try:
            for suiteName, suitePlan in self.execution_plan.items():
                batches = [batch for batch in self.suites[suiteName] if batch.__name__ in suitePlan['contexts']]
                for batch in batches:
                    self.pool.spawn(
                        self.run_context,
                        result.contexts,
                        batch.__name__,
                        batch(None),
                        suitePlan['contexts'][batch.__name__],
                        index=-1,
                        suite=suiteName
                    )

            self.pool.join()
        finally:
            if self.capture_output:
                self._capture_streams(False)

        result.elapsed_time = elapsed(start_time)
        return result

    def run_context(self, ctx_collection, ctx_name, ctx_obj, execution_plan, index=-1, suite=None, skipReason=None):
        #   FIXME: Add Docstring

        #-----------------------------------------------------------------------
        # Local variables and defs
        #-----------------------------------------------------------------------
        ctx_result = {
            'filename': suite or inspect.getsourcefile(ctx_obj.__class__),
            'name': ctx_name,
            'tests': [],
            'contexts': [],
            'topic_elapsed': 0,
            'error': None,
            'skip': skipReason
        }

        ctx_collection.append(ctx_result)
        ctx_obj.index = index
        ctx_obj.pool = self.pool
        teardown_blockers = []

        def _run_setup_and_topic(ctx_obj, index):
            # If we're already mid-skip, don't run anything
            if skipReason:
                raise skipReason

            # Run setup function
            try:
                ctx_obj.setup()
            except Exception:
                raise VowsTopicError('setup', sys.exc_info())

            try:
                # Find & run topic function
                if not hasattr(ctx_obj, 'topic'):  # ctx_obj has no topic
                    return ctx_obj._get_first_available_topic(index)

                topic_func = ctx_obj.topic
                topic_list = get_topics_for(topic_func, ctx_obj)

                start_time = time.time()

                if topic_func is None:
                    return None

                topic = topic_func(*topic_list)
                ctx_result['topic_elapsed'] = elapsed(start_time)
                return topic
            except SkipTest:
                raise
            except Exception:
                raise VowsTopicError('topic', sys.exc_info())

        def _run_tests(topic):
            def _run_with_topic(topic):
                def _run_vows_and_subcontexts(topic, index=-1, enumerated=False):
                    # methods
                    for vow_name, vow in vows:
                        if skipReason:
                            skipped_result = self.get_vow_result(vow, topic, ctx_obj, vow_name, enumerated)
                            skipped_result['skip'] = skipReason
                            ctx_result['tests'].append(skipped_result)
                        else:
                            vow_greenlet = self._run_vow(
                                ctx_result['tests'],
                                topic,
                                ctx_obj,
                                vow,
                                vow_name,
                                enumerated=enumerated)
                            teardown_blockers.append(vow_greenlet)

                    # classes
                    for subctx_name, subctx in subcontexts:
                        # resolve user-defined Context classes
                        if not issubclass(subctx, self.context_class):
                            subctx = type(ctx_name, (subctx, self.context_class), {})

                        subctx_obj = subctx(ctx_obj)
                        subctx_obj.pool = self.pool

                        subctx_greenlet = self.pool.spawn(
                            self.run_context,
                            ctx_result['contexts'],
                            subctx_name,
                            subctx_obj,
                            execution_plan['contexts'][subctx_name],
                            index=index,
                            suite=suite or ctx_result['filename'],
                            skipReason=skipReason
                        )
                        teardown_blockers.append(subctx_greenlet)

                # setup generated topics if needed
                is_generator = inspect.isgenerator(topic)
                if is_generator:
                    try:
                        ctx_obj.generated_topic = True
                        topic = ctx_obj.topic_value = list(topic)
                    except Exception:
                        # Actually getting the values from the generator may raise exception
                        raise VowsTopicError('topic', sys.exc_info())
                else:
                    ctx_obj.topic_value = topic

                if is_generator:
                    for index, topic_value in enumerate(topic):
                        _run_vows_and_subcontexts(topic_value, index=index, enumerated=True)
                else:
                    _run_vows_and_subcontexts(topic)

            vows = set((vow_name, getattr(type(ctx_obj), vow_name)) for vow_name in execution_plan['vows'])
            subcontexts = set((subctx_name, getattr(type(ctx_obj), subctx_name)) for subctx_name in execution_plan['contexts'])

            if not isinstance(topic, VowsAsyncTopic):
                _run_with_topic(topic)
            else:
                def handle_callback(*args, **kw):
                    _run_with_topic(VowsAsyncTopicValue(args, kw))
                topic(handle_callback)

        def _run_teardown():
            try:
                for blocker in teardown_blockers:
                    blocker.join()
                ctx_obj.teardown()
            except Exception:
                raise VowsTopicError('teardown', sys.exc_info())

        def _update_execution_plan():
            '''Since Context.ignore can modify the ignored_members during setup or topic,
                update the execution_plan to reflect the new ignored_members'''

            for name in ctx_obj.ignored_members:
                if name in execution_plan['vows']:
                    execution_plan['vows'].remove(name)
                if name in execution_plan['contexts']:
                    del execution_plan['contexts'][name]

        #-----------------------------------------------------------------------
        # Begin
        #-----------------------------------------------------------------------
        try:
            try:
                topic = _run_setup_and_topic(ctx_obj, index)
                _update_execution_plan()
            except SkipTest as se:
                ctx_result['skip'] = se
                skipReason = se
                topic = None
            except VowsTopicError as e:
                ctx_result['error'] = e
                skipReason = SkipTest('topic dependency failed')
                topic = None
            _run_tests(topic)
            if not ctx_result['error']:
                try:
                    _run_teardown()
                except Exception as e:
                    ctx_result['error'] = e
        finally:
            ctx_result['stdout'] = VowsParallelRunner.output.stdout.getvalue()
            ctx_result['stderr'] = VowsParallelRunner.output.stderr.getvalue()

    def _capture_streams(self, capture):
        if capture:
            sys.stdout = AnsiToWin32(_StreamCapture('stdout'), convert=False, strip=True)
            sys.stderr = AnsiToWin32(_StreamCapture('stderr'), convert=False, strip=True)
        else:
            sys.stdout = VowsParallelRunner.orig_stdout
            sys.stderr = VowsParallelRunner.orig_stderr

    def _run_vow(self, tests_collection, topic, ctx_obj, vow, vow_name, enumerated=False):
        #   FIXME: Add Docstring
        return self.pool.spawn(self.run_vow, tests_collection, topic, ctx_obj, vow, vow_name, enumerated)

    def run_vow(self, tests_collection, topic, ctx_obj, vow, vow_name, enumerated=False):
        results = super(VowsParallelRunner, self).run_vow(tests_collection, topic, ctx_obj, vow, vow_name, enumerated=enumerated)
        results['stdout'] = VowsParallelRunner.output.stdout.getvalue()
        results['stderr'] = VowsParallelRunner.output.stderr.getvalue()
