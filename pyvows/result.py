#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

class VowsResult(object):
    def __init__(self):
        self.contexts = {}

    @property
    def successful(self):
        succeeded = True
        for context in self.contexts.values():
            succeeded = succeeded and self.__eval_context(context)

        return succeeded

    def __eval_context(self, context):
        succeeded = True
        for context in context['contexts']:
            succeeded = succeeded and self.__eval_context(context)

        for test in context['tests']:
            succeeded = succeeded and test['succeeded']

        return succeeded
