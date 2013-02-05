# -*- coding: utf-8 -*-
'''This module is the foundation that allows users to write PyVows-style tests.
'''

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import os
import fnmatch
import glob
import re
import sys
import warnings

from pyvows.async_topic import VowsAsyncTopic, VowsAsyncTopicValue
from pyvows.runner import VowsParallelRunner


def locate(pattern, root=os.curdir, recursive=True):
    '''Recursively locates test files when `pyvows` is run from the
    command line.

    '''
    root_path = os.path.abspath(root)

    if recursive:
        return_files = []
        for path, dirs, files in os.walk(root_path):
            for filename in fnmatch.filter(files, pattern):
                return_files.append(os.path.join(path, filename))
        return return_files
    else:
        return glob(os.path.join(root_path, pattern))


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
            method_name = 'not_{name}'.format(name = name)
        else:
            method_name = name

        if not hasattr(Vows.Assert, method_name):
            raise AttributeError('Assertion {method_name} was not found!'.format(
                method_name = method_name))

        def assert_topic(*args, **kw):
            '''Allows instances (topics) to chain calls to `VowsAssertion`s.

            In the following PyVows-test snippet:

                expect(topic).to_be_True()

            ...This method is what allows `expect(topic)` to call
            `.to_be_True()` (or some other VowsAssertion).

            '''
            return getattr(Vows.Assert, method_name)(self.topic, *args, **kw)

        return assert_topic


class VowsAssertion(object):
    '''Used by the `Vows` class for various assertion-related functionality.'''

    class AssertionNotFoundError(AttributeError):
        '''Raised when a VowsAssertion cannot be found.'''
        def __init__(self, name):
            super(VowsAssertion.AssertionNotFoundError, self).__init__(
                'Assertion "{name!s}" was not found!'.format(name = name))

    def __getattr__(self, name):
        if not hasattr(self, name):
            raise VowsAssertion.AssertionNotFoundError(name)
        return super(VowsAssertion, self).__getattr__(name)


class VowsAssertionError(AssertionError):
    '''Raised when a VowsAssertion returns False.'''

    def __init__(self, *args):
        msg = args[0]
        if not msg.endswith('.'):
            msg += '.'
        self.msg = msg
        self.args = tuple(map(repr, args[1:]))

    def __str__(self):
        return self.msg % self.args

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return "VowsAssertionError('{0!s}',)".format(self)


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
    contexts = {}

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
            self.ignored_members = ['topic', 'setup', 'teardown', 'ignore']

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
                self.ignored_members.append(arg)

        def setup(self):
            '''For use in your PyVows tests.  Define `setup` in your
            `Vows.Context` subclass to define what should happen before
            that Context's testing begins.

            Remember:
                * sibling Contexts are executed in parallel
                * nested Contexts are executed sequentially
                
            '''
            pass

        def teardown(self):
            '''For use in your PyVows tests.  Define `setup` in your
            `Vows.Context` subclass to define what should happen after
            that Context's testing ends.

            Remember:
                * sibling Contexts are executed in parallel
                * nested Contexts are executed sequentially
                
            '''
            pass

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

    AsyncTopic = VowsAsyncTopic
    AsyncTopicValue = VowsAsyncTopicValue
    Assert = VowsAssertion()

    @staticmethod
    def async_topic(topic):
        '''Topic decorator.  Allows PyVows testing of asynchronous topics.

        Use `@Vows.async_topic` on your `topic` method to mark it as
        asynchronous.  This allows PyVows to test topics which use callbacks
        instead of return values.
        
        '''
        def wrapper(*args, **kw):
            return VowsAsyncTopic(topic, args, kw)
        wrapper._original = topic
        wrapper.__name__ = topic.__name__
        return wrapper

    @staticmethod
    def asyncTopic(topic):
        #   FIXME: Add Comment
        warnings.warn( 'The asyncTopic decorator is deprecated. Please use Vows.async_topic instead.', 
                        DeprecationWarning, 
                        stacklevel=2)
        return Vows.async_topic(topic)

    @staticmethod
    def batch(method):
        '''Class decorator.  Use on subclasses of `Vows.Context`.

        Test batches in PyVows are the largest unit of tests. The convention
        is to have one test batch per file, and have the batch’s class match
        the file name.
        
        '''
        def method_name(*args, **kw):
            method(*args, **kw)

        Vows.contexts[method.__name__] = method

        return method_name

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
        def method_name(*args, **kw):
            method(*args, **kw)

        def exec_assertion(*args, **kw):
            return method_name(*args, **kw)

        setattr(Vows.Assert, method.__name__, exec_assertion)
        return method_name

    @classmethod
    def create_assertions(cls, method):
        '''Function decorator.  Use to create custom assertions for your
        vows.

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
        humanized_method_name = re.sub(r'_+', ' ', method.__name__)

        def exec_assertion(*args):
            raw_msg = 'Expected topic(%s) {assertion}'.format(assertion=humanized_method_name)
            if len(args) is 2:
                raw_msg += ' %s'

            if not method(*args):
                raise VowsAssertionError(raw_msg, *args)

        def exec_not_assertion(*args):
            raw_msg = 'Expected topic(%s) not {not_assertion}'.format(not_assertion=humanized_method_name)
            if len(args) is 2:
                raw_msg += ' %s'

            if method(*args):
                raise VowsAssertionError(raw_msg, *args)

        setattr(Vows.Assert, method.__name__, exec_assertion)
        setattr(Vows.Assert, 'not_{method_name}'.format(
            method_name = method.__name__),
            exec_not_assertion)

        def wrapper(*args, **kw):
            return method(*args, **kw)

        return wrapper

    @classmethod
    def ensure(cls, vow_success_event, vow_error_event):
        #   FIXME: Add Docstring
        #
        #       *   Used by `run()` in `console.py`
        #       *   Please add a useful description if you wrote this! :)
        runner = VowsParallelRunner(Vows.contexts,
                                    Vows.Context,
                                    vow_success_event,
                                    vow_error_event)
        return runner.run()

    @classmethod
    def gather(cls, path, pattern):
        #   FIXME: Add Docstring
        #
        #   *   Only used in `console.py`
        path = os.path.abspath(path)

        files = locate(pattern, path)
        sys.path.insert(0, path)
        for module_path in files:
            module_name = os.path.splitext(module_path.replace(path, '').replace('/', '.').lstrip('.'))[0]
            __import__(module_name)
