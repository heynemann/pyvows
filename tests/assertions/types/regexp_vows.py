#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionRegexp(Vows.Context):
    def topic(self):
        return "some string"

    class WhenItMatches(Vows.Context):

        def we_assert_it_matches_regexp(self, topic):
            expect(topic).to_match(r'^some.+$')

        class WhenWeGetAnError(Vows.Context):

            @Vows.capture_error
            def topic(self, last):
                expect(last).to_match(r'^other.+$')

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of(
                    "Expected topic('some string') to match the regular expression '^other.+$'")

    class WhenItDoesntMatches(Vows.Context):

        def we_assert_it_does_not_match_regexp(self, topic):
            expect(topic).Not.to_match(r'^other.+$')

        class WhenWeGetAnError(Vows.Context):

            @Vows.capture_error
            def topic(self, last):
                expect(last).not_to_match(r'^some.+$')

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of(
                    "Expected topic('some string') not to match the regular expression '^some.+$'")
