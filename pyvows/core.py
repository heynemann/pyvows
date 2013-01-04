#!/usr/bin/env python
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
    '''Recursively locates test files when `pyvows` is run from the command
    line.
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
    '''The `expect` class is used in pyvows tests.  It is passed the topic,
    and allows the chaining of pyvows assertions.  Example:
    
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

        method_name = 'not_{name}'.format(name=name) if self.not_assert else name

        if not hasattr(Vows.Assert, method_name):
            raise AttributeError('Assertion {method_name} was not found!'.format(method_name=method_name))

        def assert_topic(*args, **kw):
            #   FIXME: Add Docstring / Comment description
            return getattr(Vows.Assert, method_name)(self.topic, *args, **kw)

        return assert_topic


class VowsAssertion(object):
    #   FIXME: Add Docstring

    class AssertionNotFoundError(AttributeError):
        #   FIXME: Add Docstring

        def __init__(self, name):
            super(VowsAssertion.AssertionNotFoundError, self).__init__(
                'Assertion with name {name} was not found!'.format(name=name))

    def __getattr__(self, name):
        if not hasattr(self, name):
            raise VowsAssertion.AssertionNotFoundError(name)
        return super(VowsAssertion, self).__getattr__(name)


class VowsAssertionError(AssertionError):
    #   FIXME: Add Docstring

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
            for arg in args:
                self.ignored_members.append(arg)

        def setup(self):
            pass

        def teardown(self):
            pass

    class NotErrorContext(Context):
        #   FIXME: Add Docstring
        def should_not_be_an_error(self, topic):
            expect(topic).not_to_be_an_error()

    class NotEmptyContext(Context):
        #   FIXME: Add Docstring
        def should_not_be_empty(self, topic):
            expect(topic).not_to_be_empty()

    AsyncTopic = VowsAsyncTopic
    AsyncTopicValue = VowsAsyncTopicValue
    Assert = VowsAssertion()

    @staticmethod
    def async_topic(topic):
        #   FIXME: Add Docstring
        def wrapper(*args, **kw):
            return VowsAsyncTopic(topic, args, kw)
        wrapper._original = topic
        wrapper.__name__ = topic.__name__
        return wrapper

    @staticmethod
    def asyncTopic(topic):
        #   FIXME: Add Comment
        warnings.warn('The asyncTopic decorator is deprecated. Please use Vows.async_topic instead.', DeprecationWarning, stacklevel=2)
        return Vows.async_topic(topic)

    @staticmethod
    def batch(method):
        #   FIXME: Add Docstring
        def method_name(*args, **kw):
            method(*args, **kw)

        Vows.contexts[method.__name__] = method

        return method_name

    @classmethod
    def assertion(cls, method):
        #   FIXME: Add Docstring
        def method_name(*args, **kw):
            method(*args, **kw)

        def exec_assertion(*args, **kw):
            return method_name(*args, **kw)

        setattr(Vows.Assert, method.__name__, exec_assertion)
        return method_name

    @classmethod
    def create_assertions(cls, method):
        #   FIXME: Add Docstring
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
        setattr(Vows.Assert, 'not_{method_name}'.format(method_name=method.__name__), exec_not_assertion)

        def wrapper(*args, **kw):
            return method(*args, **kw)

        return wrapper

    @classmethod
    def ensure(cls, vow_success_event, vow_error_event):
        #   FIXME: Add Docstring
        runner = VowsParallelRunner(Vows.contexts,
                                    Vows.Context,
                                    vow_success_event,
                                    vow_error_event)
        return runner.run()

    @classmethod
    def gather(cls, path, pattern):
        #   FIXME: Add Docstring
        path = os.path.abspath(path)

        files = locate(pattern, path)
        sys.path.insert(0, path)
        for module_path in files:
            module_name = os.path.splitext(module_path.replace(path, '').replace('/', '.').lstrip('.'))[0]
            __import__(module_name)
