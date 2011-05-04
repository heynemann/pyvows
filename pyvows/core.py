#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyVows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys
import os
from os.path import join, abspath, splitext
import fnmatch
import glob

from pyvows.runner import VowsParallelRunner

def locate(pattern, root=os.curdir, recursive=True):
    root_path = os.path.abspath(root)

    if recursive:
        return_files = []
        for path, dirs, files in os.walk(root_path):
            for filename in fnmatch.filter(files, pattern):
                return_files.append(os.path.join(path, filename))
        return return_files
    else:
        return glob(join(root_path, pattern))

class expect(object):

    def __init__(self, topic):
        self.topic = topic
        self.not_assert = False

    def __getattr__(self, name):
        if name == "topic":
            return super(expect, self).__getattr__(name)

        if name == "Not":
            self.not_assert = not self.not_assert
            return self

        method_name = "not_%s" % name if self.not_assert else name
        if not hasattr(Vows.Assert, method_name):
            raise AttributeError("Assertion %s was not found!" % method_name)

        def assert_topic(*args, **kw):
            return getattr(Vows.Assert, method_name)(self.topic, *args, **kw)

        return assert_topic

class VowsAsyncTopic(object):
    def __init__(self, func, *args, **kw):
        self.func = func
        self.args = args
        self.kw = kw

class VowsAssertion(object):
    class AssertionNotFoundError(AttributeError):
        def __init__(self, name):
            super(VowsAssertion.AssertionNotFoundError, self).__init__("Assertion with name %s was not found!" % name)

    def __getattr__(self, name):
        if not hasattr(self, name):
            raise VowsAssertion.AssertionNotFoundError(name)
        return super(VowsAssertion, self).__getattr__(name)


class Vows(object):
    contexts = {}

    class Context(object):
        def __init__(self, parent):
            self.parent = parent
            self.topic_value = None
            self.index = -1
            self.generated_topic = False

        def _get_first_available_topic(self, index=-1):
            if self.topic_value:
                if index > -1 and isinstance(self.topic_value, (list, set, tuple)):
                    return self.topic_value[index]
                return self.topic_value

            if not self.parent:
                return None

            return self.parent._get_first_available_topic(index)

    AsyncTopic = VowsAsyncTopic

    Assert = VowsAssertion()

    @staticmethod
    def batch(method):
        def method_name(*args, **kw):
            method(*args, **kw)

        Vows.contexts[method.__name__] = method

        return method_name

    @classmethod
    def assertion(cls, method):
        def method_name(*args, **kw):
            method(*args, **kw)
        def exec_assertion(*args, **kw):
            return method_name(*args, **kw)
        setattr(Vows.Assert, method.__name__, exec_assertion)
        return method_name

    @classmethod
    def ensure(cls, vow_success_event, vow_error_event):
        runner = VowsParallelRunner(Vows.contexts, Vows.Context, Vows.AsyncTopic, vow_success_event, vow_error_event)

        result = runner.run()

        return result

    @classmethod
    def gather(cls, path, pattern):
        path = abspath(path)

        files = locate(pattern, path)
        sys.path.insert(0, path)
        for module_path in files:
            module_name = splitext(module_path.replace(path, '').replace('/', '.').lstrip('.'))[0]
            __import__(module_name)


