#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionIsNull(Vows.Context):

    class WhenItIsNull(Vows.Context):
        def topic(self):
            return None

        def we_get_to_check_for_nullability_in_None(self, topic):
            expect(topic).to_be_null()

        class WhenWeGetAnError(Vows.Context):
            @Vows.capture_error
            def topic(self, last):
                expect(1).to_be_null()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(1) to be None")

    class WhenItIsNotNull(Vows.Context):
        def topic(self):
            return "something"

        def we_see_string_is_not_null(self, topic):
            expect(topic).not_to_be_null()

        class WhenWeGetAnError(Vows.Context):
            @Vows.capture_error
            def topic(self, last):
                expect(None).not_to_be_null()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(None) not to be None")
