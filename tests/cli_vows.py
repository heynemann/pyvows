#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com
import argparse

from pyvows import Vows, expect
from pyvows.cli import Parser


mock_args = (
    '--cover',
    '--profile',
)


@Vows.batch
class PyVowsCommandLineInterface(Vows.Context):

    class ArgumentParser(Vows.Context):
        def topic(self):
            # suppress the defaults, or the test breaks :/
            parser = Parser(argument_default=argparse.SUPPRESS)
            return parser

        def we_have_a_parser(self, topic):
            expect(topic).to_be_instance_of(argparse.ArgumentParser)

        def we_dont_get_an_error(self, topic):
            expect(topic).not_to_be_an_error()

        class ParsesCorrectly(Vows.Context):
            def topic(self, parser):
                return parser.parse_args(mock_args)

            def should_contain_cover(self, topic):
                expect('cover' in topic).to_be_true()

            def cover_should_be_true(self, topic):
                expect(topic.cover).to_be_true()

            def profile_should_be_true(self, topic):
                expect(topic.profile).to_be_true()
