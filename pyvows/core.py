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

from pyvows import utils
from pyvows.async_topic import VowsAsyncTopic, VowsAsyncTopicValue
from pyvows.decorators import _assertion, _batch, _create_assertions, async_topic
from pyvows.runner import VowsParallelRunner



class expect(object):
    '''This atypical class provides a key part of the PyVows testing syntax.

    For example:

        expect(True).to_be_true()

    '''

    def __init__(self, topic):
        self.topic = topic
        self.not_assert = False

    def __getattr__(self, name):
        if name == 'topic':
            return super(expect, self).__getattr__(name)

        if name == 'Not':
            self.not_assert = not self.not_assert
            return self

        if self.not_assert:
            method_name = 'not_{name}'.format(name=name)
        else:
            method_name = name

        if not hasattr(Vows.Assert, method_name):
            raise AttributeError('Assertion {method_name} was not found!'.format(
                method_name=method_name))

        def assert_topic(*args, **kw):
            '''Allows instances (topics) to chain calls to `VowsAssertion`s.

            In the following PyVows-test snippet:

                expect(topic).to_be_True()

            ...This method is what allows `expect(topic)` to call
            `.to_be_True()` (or some other VowsAssertion).

            '''
            return getattr(Vows.Assert, method_name)(self.topic, *args, **kw)

        return assert_topic


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
    batches = dict()
    exclusion_patterns = set()
    Assert = utils.VowsAssertion()
    AsyncTopic = VowsAsyncTopic
    AsyncTopicValue = VowsAsyncTopicValue
    


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

        def __init__(self, parent=None):
            self.parent = parent
            self.topic_value = None
            self.index = -1
            self.generated_topic = False
            self.ignored_members = set(['topic', 'setup', 'teardown', 'ignore'])
        
        def _get_first_available_topic(self, index=-1):
            if self.topic_value:
                if index > -1 and isinstance(self.topic_value, (list, set, tuple)):
                    topic = self.topic_value[index]
                    if hasattr(self, 'topic_error'):
                        topic.error = self.topic_error
                    return topic

                topic = self.topic_value
                if hasattr(self, 'topic_error'):
                    topic.error = self.topic_error
                return topic

            if not self.parent:
                return None

            return self.parent._get_first_available_topic(index)

        def ignore(self, *args):
            '''Appends `*args` to `ignored_members`.  (Methods listed in
            `ignored_members` are considered "not a test method" by PyVows.)
            '''
            for arg in args:
                self.ignored_members.add(arg)

        def setup(self): pass
        def teardown(self): pass
        
        setup.__doc__    = \
        teardown.__doc__ = \
        '''For use in your PyVows tests.  Define in your `Vows.Context` 
            subclass to define what should happen before that Context's testing begins.

            Remember:
                * sibling Contexts are executed in parallel
                * nested Contexts are executed sequentially
                
        '''

    class NotErrorContext(Context):
        #   FIXME: Add Docstring
        #
        #   *   Why does this class exist?
        #   *   Does this simply delegate the call to `expect`?
        #   *   If this can be used for some clever form of generative
        #       testing, show an example
        def should_not_be_an_error(self, topic):
            expect(topic).not_to_be_an_error()

    class NotEmptyContext(Context):
        #   FIXME: Add Docstring
        #
        #   *   Why does this class exist?
        #   *   Does this simply delegate the call to `expect`?
        #   *   If this can be used for some clever form of generative
        #       testing, show an example
        def should_not_be_empty(self, topic):
            expect(topic).not_to_be_empty()

    @staticmethod
    def async_topic(topic):
        return async_topic(topic)

    @staticmethod
    def asyncTopic(topic):
        #   FIXME: Add Comment
        warnings.warn('The asyncTopic decorator is deprecated. Please use Vows.async_topic instead.',
                      DeprecationWarning,
                      stacklevel=2)
        return async_topic(topic)

    @staticmethod
    def batch(ctx_class):
        '''Class decorator.  Use on subclasses of `Vows.Context`.

        Test batches in PyVows are the largest unit of tests. The convention
        is to have one test batch per file, and have the batch’s class match
        the file name.

        '''
        Vows.batches[ctx_class.__name__] = ctx_class
        _batch(ctx_class)

    @classmethod
    def assertion(cls, method):
        '''Function decorator.  Provides lower-level control for custom
        assertions than `@Vows.create_assertions`.

        If you need more control over your error message, or your assertion
        doesn’t have a corresponding `not_`, use this decorator and
        raise a `VowsAssertionError`.

        By raising a `VowsAssertionError`, you get the benefit of highlighting
        the important values when your vows are broken.

        If you still just wanna raise an `AssertionError` like old times,
        that’s supported, too.

        It’s recommended to always declare both the assertion and the `not_`
        assertion (if applicable), so they can be used like this:

            expect(5).to_be_a_positive_integer()
            expect(-3).Not.to_be_a_positive_integer()

        '''
        #   http://pyvows.org/#-assertions
        return _assertion(method, Vows.Assert)

    @classmethod
    def create_assertions(cls, method):
        '''Function decorator.  Use to create custom assertions for your
        vows.
        ''' '''
        Creating new assertions for use with `expect` is as simple as using
        this decorator on a function. The function expects `topic` as the
        first parameter, and `expectation` second:

            @Vows.create_assertions
            def to_be_greater_than(topic, expected):
                return topic > expected

        Now, the following expectation…

            expect(2).to_be_greater_than(3)

        …will report:

            Expected topic(2) to be greater than 3.

        It will also create the corresponding `not_` assertion:

            expect(4).not_to_be_greater_than(3);

        …will report:

            Expected topic(4) not to be greater than 3.

        '''
        #   http://pyvows.org/#-assertions
        return _create_assertions(method, Vows.Assert)

    @classmethod
    def collect(cls, path, pattern):
        #   FIXME: Add Docstring
        #
        #   *   Only used in `cli.py`
        path = os.path.abspath(path)
        files = utils.locate(pattern, path)
        Vows.suites = set([f for f in files])
        sys.path.insert(0, path)
            
        for module_path in files:
            module_name = os.path.splitext(
                module_path.replace(path, '').replace('/', '.').lstrip('.')
            )[0]
            __import__(module_name)

    @classmethod
    def run(cls, on_vow_success, on_vow_error):
        #   FIXME: Add Docstring
        #
        #       *   Used by `run()` in `cli.py`
        #       *   Please add a useful description if you wrote this! :)
        runner = VowsParallelRunner(Vows.suites,
                                    Vows.batches,
                                    Vows.Context,
                                    on_vow_success,
                                    on_vow_error,
                                    cls.exclusion_patterns)
        return runner.run()

    @classmethod
    def exclude(cls, test_name_pattern):
        cls.exclusion_patterns = test_name_pattern
