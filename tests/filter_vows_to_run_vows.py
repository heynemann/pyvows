#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Nathan Dotz nathan.dotz@gmail.com

from pyvows import Vows, expect
from pyvows import cli

from pyvows.runner import VowsRunner


@Vows.batch
class FilterOutVowsFromCommandLine(Vows.Context):

    class Console(Vows.Context):
        def topic(self):
            return cli

        def should_be_not_error_when_called_with_5_args(self, topic):
            try:
                topic.run(None, None, None, None, None)
            except Exception as e:
                expect(e).Not.to_be_instance_of(TypeError)

        def should_hand_off_exclusions_to_Vows_class(self, topic):

            patterns = ['foo', 'bar', 'baz']
            try:
                topic.run(None, '*_vows.py', 2, False, patterns)
            except Exception:
                expect(Vows.exclusion_patterns).to_equal(patterns)

    # TODO: add vow checking that there is a message about vow matching

    class Core(Vows.Context):

        def topic(self):
            return Vows

        def should_have_exclude_method(self, topic):
            expect(topic.exclude).to_be_a_function()

    class VowsRunner(Vows.Context):

        def topic(self):
            return VowsRunner

        def can_be_initialized_with_6_arguments(self, topic):
            try:
                topic(None, None, None, None, None)
            except Exception as e:
                expect(e).Not.to_be_instance_of(TypeError)

        def removes_appropriate_contexts(self, topic):
            r = topic(None, None, None, None, set(['foo', 'bar']))
            col = []
            r.run_context(col, 'footer', r)
            expect(len(col)).to_equal(0)

        def leaves_unmatched_contexts(self, topic):
            VowsRunner.teardown = None
            r = topic(None, None, None, None, ['foo', 'bar'])
            col = []
            r.run_context(col, 'baz', r)
            expect(len(col)).to_equal(1)
            r.run_context(col, 'bip', r)
            expect(len(col)).to_equal(2)
