#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionIsEmpty(Vows.Context):
    class WhenEmpty(Vows.Context):
        class WhenString(Vows.Context):
            def topic(self):
                return ''

            def we_get_an_empty_string(self, topic):
                expect(topic).to_be_empty()

        class WhenList(Vows.Context):
            def topic(self):
                return []

            def we_get_an_empty_list(self, topic):
                expect(topic).to_be_empty()

        class WhenTuple(Vows.Context):
            def topic(self):
                return tuple([])

            def we_get_an_empty_tuple(self, topic):
                expect(topic).to_be_empty()

        class WhenDict(Vows.Context):
            def topic(self):
                return {}

            def we_get_an_empty_dict(self, topic):
                expect(topic).to_be_empty()

        class WhenWeGetAnError(Vows.Context):

            @Vows.capture_error
            def topic(self, last):
                expect([1]).to_be_empty()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic([1]) to be empty")

    class WhenNotEmpty(Vows.Context):
        class WhenString(Vows.Context):
            def topic(self):
                return 'whatever'

            def we_get_a_not_empty_string(self, topic):
                expect(topic).Not.to_be_empty()

        class WhenList(Vows.Context):
            def topic(self):
                return ['something']

            def we_get_a_not_empty_list(self, topic):
                expect(topic).Not.to_be_empty()

        class WhenTuple(Vows.Context):
            def topic(self):
                return tuple(['something'])

            def we_get_a_not_empty_tuple(self, topic):
                expect(topic).Not.to_be_empty()

        class WhenDict(Vows.Context):
            def topic(self):
                return {"key": "value"}

            def we_get_a_not_empty_dict(self, topic):
                expect(topic).Not.to_be_empty()

        class WhenWeGetAnError(Vows.Context):

            @Vows.capture_error
            def topic(self, last):
                expect([]).not_to_be_empty()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic([]) not to be empty")
