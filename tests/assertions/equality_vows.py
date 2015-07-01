#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionEquality(Vows.Context):
    def topic(self):
        return "test"

    class WhenIsEqual(Vows.Context):

        def we_get_test(self, topic):
            expect(topic).to_equal('test')

        class WhenWeGetAnError(Vows.Context):

            @Vows.capture_error
            def topic(self, last):
                expect(1).to_equal(2)

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(1) to equal 2")

    class WhenIsNotEqual(Vows.Context):

        def we_do_not_get_else(self, topic):
            expect(topic).Not.to_equal('else')

        class WhenWeGetAnError(Vows.Context):

            @Vows.capture_error
            def topic(self, last):
                expect(1).not_to_equal(1)

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of("Expected topic(1) not to equal 1")

    class WhenHaveASubClassThatHaveAExtraParamInTopic(Vows.Context):
        def topic(self, last):
            return last

        def we_get_the_last_topic_value_without_modifications(self, topic):
            expect(topic).to_equal('test')

    class WhenSubContextNotHaveTopic(Vows.Context):

        def we_get_the_last_topic(self, topic):
            expect(topic).to_equal('test')
