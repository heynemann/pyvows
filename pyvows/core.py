# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import os
import sys
import warnings
import copy

import preggy

from pyvows import utils
from pyvows.decorators import _batch, async_topic, capture_error, skip_if
from pyvows.runner import VowsRunner
from pyvows.runner.executionplan import ExecutionPlanner

#-------------------------------------------------------------------------------------------------

expect = preggy.expect


class Vows(object):
    '''This class contains almost the entire interface for using PyVows.  (The
    `expect` class usually being the only other necessary import.)

        *   Mark test batches with the `Vows.batch` decorator
        *   Build test hierarchies with classes that extend `Vows.Context`
        *   For those who need it, topics with asynchronous code can use the
            `Vows.async_topic` decorator

    Other attributes and methods here are for PyVows' internal use.  They
    aren't necessary for writing tests.

    '''
    suites = dict()
    exclusion_patterns = set()
    inclusion_patterns = set()

    class Context(object):
        '''Extend this class to create your test classes.  (The convention is to
        write `from pyvows import Vows, expect` in your test module, then extend
        `Vows.Context` in your test classes.  If you really wanted, you could
        also import `Context` directly.  But don't do that.)

            *   `Vows.Context` subclasses expect one method named `topic`.
                It should be the first method in any `Vows.Context` subclass,
                by convention.
            *   Sibling `Context`s run in parallel.
            *   Nested `Context`s run sequentially.

        The `setup` and `teardown` methods aren't typically needed.  But
        they are available if your test suite has extra pre- and
        post-testing work to be done in any given `Context`.
        '''

        ignored_members = set(['topic', 'setup', 'teardown', 'ignore'])

        def __init__(self, parent=None):
            self.parent = parent
            self.topic_value = None
            self.index = -1
            self.generated_topic = False
            self.ignored_members = copy.copy(self.ignored_members)

        def _get_first_available_topic(self, index=-1):
            if self.topic_value:
                if index > -1 and isinstance(self.topic_value, (list, set, tuple)):
                    return self.topic_value[index]
                else:
                    return self.topic_value
            elif self.parent:
                return self.parent._get_first_available_topic(index)
            return None

        def ignore(self, *args):
            '''Appends `*args` to `ignored_members`.  (Methods listed in
            `ignored_members` are considered "not a test method" by PyVows.)
            '''
            for arg in args:
                self.ignored_members.add(arg)

        def setup(self):
            pass

        def teardown(self):
            pass

        setup.__doc__ = teardown.__doc__ = \
            '''For use in your PyVows tests.  Define in your `Vows.Context`
                subclass to define what should happen before that Context's testing begins.

                Remember:
                    * sibling Contexts are executed in parallel
                    * nested Contexts are executed sequentially
            '''

    @staticmethod
    def assertion(func):
        return preggy.assertion(func)

    @staticmethod
    def create_assertions(func):
        return preggy.create_assertions(func)

    @staticmethod
    def async_topic(topic):
        return async_topic(topic)

    @staticmethod
    def asyncTopic(topic):
        #   FIXME: Add Comment
        warnings.warn('The asyncTopic decorator is deprecated.  '
                      'Please use Vows.async_topic instead.',
                      DeprecationWarning,
                      stacklevel=2)
        return async_topic(topic)

    @staticmethod
    def capture_error(topic_func):
        return capture_error(topic_func)

    @staticmethod
    def skip_if(condition, reason):
        return skip_if(condition, reason)

    @staticmethod
    def skip(reason):
        return skip_if(True, reason)

    @staticmethod
    def batch(ctx_class):
        '''Class decorator.  Use on subclasses of `Vows.Context`.

        Test batches in PyVows are the largest unit of tests. The convention
        is to have one test batch per file, and have the batch’s class match
        the file name.

        '''
        suite = ctx_class.__module__.replace('.', os.path.sep)
        suite = os.path.abspath(suite)
        suite += '.py'
        if suite not in Vows.suites:
            Vows.suites[suite] = set()
        Vows.suites[suite].add(ctx_class)
        return _batch(ctx_class)

    @classmethod
    def collect(cls, path, pattern):
        #   FIXME: Add Docstring
        #
        #   *   Only used in `cli.py`
        path = os.path.abspath(path)
        sys.path.insert(0, path)
        files = utils.locate(pattern, path)
        for module_path in files:
            module_name = os.path.splitext(
                module_path.replace(path, '').replace(os.sep, '.').lstrip('.')
            )[0]
            __import__(module_name)

    @classmethod
    def exclude(cls, test_name_pattern):
        cls.exclusion_patterns = test_name_pattern

    @classmethod
    def include(cls, test_name_pattern):
        cls.inclusion_patterns = test_name_pattern

    @classmethod
    def run(cls, on_vow_success, on_vow_error, capture_error=False):
        #   FIXME: Add Docstring
        #
        #       *   Used by `run()` in `cli.py`
        #       *   Please add a useful description if you wrote this! :)

        execution_plan = ExecutionPlanner(cls.suites, set(cls.exclusion_patterns), set(cls.inclusion_patterns)).plan()

        runner = VowsRunner(
            cls.suites,
            cls.Context,
            on_vow_success,
            on_vow_error,
            execution_plan,
            capture_error
        )
        return runner.run()
