#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


def a_function(): pass

@Vows.batch
class AssertionIsFunction(Vows.Context):

    class WhenItIsAFunction(Vows.Context):
        def topic(self):
            def my_func():
                pass
            return my_func

        def we_assert_it_is_a_function(self, topic):
            expect(topic).to_be_a_function()

        class WhenWeGetAnError(Vows.Context):

            def topic(self):
                expect(4).to_be_a_function()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of(
                        "Expected topic(4) to be a function or a method, but it was a %s." % str(int))


    class WhenItNotAFunction(Vows.Context):
        def topic(self):
            return 42

        def we_assert_it_is_not_a_function(self, topic):
            expect(topic).Not.to_be_a_function()

        class WhenWeGetAnError(Vows.Context):

            def topic(self):
                expect(a_function).not_to_be_a_function()

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of(
                        "Expected topic(%s) not to be a function or a method." % str(a_function))


