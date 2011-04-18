#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows.runner import VowsRunner

class Vows(object):
    __current_vows__ = {}

    class Context(object):
        pass

    class Assert(object):
        pass

    @classmethod
    def batch(cls, method):
        def method_name(*args, **kw):
            method(*args, **kw)
        Vows.__current_vows__[method.__name__] = method
        return method_name

    @classmethod
    def assertion(cls, method):
        def method_name(*args, **kw):
            method(*args, **kw)
        @classmethod
        def exec_assertion(cls, *args, **kw):
            return method_name(*args, **kw)
        setattr(Vows.Assert, method.__name__, exec_assertion)
        return method_name

    @classmethod
    def ensure(cls):
        runner = VowsRunner(cls.__current_vows__, Vows.Context)

        result = runner.run()

        cls.__current_vows__ = {}

        return result


