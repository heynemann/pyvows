#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionLength(Vows.Context):
    class ToLength(Vows.Context):
        class WithString(Vows.Context):
            def topic(self):
                return "some string"

            def we_can_see_it_has_11_characters(self, topic):
                expect(topic).to_length(11)

        class WithList(Vows.Context):
            def topic(self):
                return ["some", "list"]

            def we_can_see_it_has_2_items(self, topic):
                expect(topic).to_length(2)

        class WithTuple(Vows.Context):
            def topic(self):
                return tuple(["some", "list"])

            def we_can_see_it_has_2_items(self, topic):
                expect(topic).to_length(2)

        class WithDict(Vows.Context):
            def topic(self):
                return {"some": "item", "other": "item"}

            def we_can_see_it_has_2_items(self, topic):
                expect(topic).to_length(2)

        class WhenWeGetAnError(Vows.Context):

            @Vows.capture_error
            def topic(self, last):
                expect('a').to_length(2)

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic('a') to have 2 of length, but it has 1")

    class NotToLength(Vows.Context):
        class WhenWeGetAnError(Vows.Context):
            @Vows.capture_error
            def topic(self, last):
                expect('a').not_to_length(1)

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic('a') not to have 1 of length")
