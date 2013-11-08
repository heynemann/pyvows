#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionIsNumeric(Vows.Context):

    class WhenItIsANumber(Vows.Context):
        def topic(self):
            return 42

        def we_assert_it_is_numeric(self, topic):
            expect(topic).to_be_numeric()

        class WhenWeGetAnError(Vows.Context):

            @Vows.capture_error
            def topic(self):
                expect('s').to_be_numeric()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic('s') to be numeric")

    class WhenItIsNotANumber(Vows.Context):
        def topic(self):
            return 'test'

        def we_assert_it_is_not_numeric(self, topic):
            expect(topic).Not.to_be_numeric()

        class WhenWeGetAnError(Vows.Context):

            @Vows.capture_error
            def topic(self):
                expect(2).not_to_be_numeric()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(2) not to be numeric")
