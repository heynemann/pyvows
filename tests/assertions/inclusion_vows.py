#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionInclude(Vows.Context):

    class WhenItIsAString(Vows.Context):
        def topic(self):
            return "some big string"

        def we_can_find_some(self, topic):
            expect(topic).to_include('some')

        def we_can_find_big(self, topic):
            expect(topic).to_include('big')

        def we_can_find_string(self, topic):
            expect(topic).to_include('string')

        def we_cant_find_else(self, topic):
            expect(topic).Not.to_include('else')

    class WhenItIsAList(Vows.Context):
        def topic(self):
            return ["some", "big", "string"]

        def we_can_find_some(self, topic):
            expect(topic).to_include('some')

        def we_can_find_big(self, topic):
            expect(topic).to_include('big')

        def we_can_find_string(self, topic):
            expect(topic).to_include('string')

        def we_cant_find_else(self, topic):
            expect(topic).Not.to_include('else')

    class WhenItIsATuple(Vows.Context):
        def topic(self):
            return tuple(["some", "big", "string"])

        def we_can_find_some(self, topic):
            expect(topic).to_include('some')

        def we_can_find_big(self, topic):
            expect(topic).to_include('big')

        def we_can_find_string(self, topic):
            expect(topic).to_include('string')

        def we_cant_find_else(self, topic):
            expect(topic).Not.to_include('else')

    class WhenItIsADict(Vows.Context):
        def topic(self):
            return {"some": 1, "big": 2, "string": 3}

        def we_can_find_some(self, topic):
            expect(topic).to_include('some')

        def we_can_find_big(self, topic):
            expect(topic).to_include('big')

        def we_can_find_string(self, topic):
            expect(topic).to_include('string')

        def we_cant_find_else(self, topic):
            expect(topic).Not.to_include('else')

    class WhenWeGetAnError(Vows.Context):
        @Vows.capture_error
        def topic(self, last):
            expect('a').to_include('b')

        def we_get_an_understandable_message(self, topic):
            expect(topic).to_have_an_error_message_of("Expected topic('a') to include 'b'")

    class WhenWeGetAnErrorOnNot(Vows.Context):
        @Vows.capture_error
        def topic(self, last):
            expect('a').not_to_include('a')

        def we_get_an_understandable_message(self, topic):
            expect(topic).to_have_an_error_message_of("Expected topic('a') not to include 'a'")
