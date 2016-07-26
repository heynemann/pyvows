#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect
from preggy import utils


@Vows.batch
class AssertionErrors(Vows.Context):
    class NonErrors(Vows.Context):
        def topic(self):
            return 0

        def we_can_see_that_is_not_an_error(self, topic):
            expect(topic).Not.to_be_an_error()

    class Errors(Vows.Context):
        def topic(self, error):
            return ValueError('some bogus error')

        def we_can_see_that_is_an_error_class(self, topic):
            expect(topic).to_be_an_error()

        def we_can_see_it_was_a_value_error(self, topic):
            expect(topic).to_be_an_error_like(ValueError)

        def we_can_see_that_is_has_error_message_of(self, topic):
            expect(topic).to_have_an_error_message_of('some bogus error')

        class ErrorMessages(Vows.Context):
            @Vows.capture_error
            def topic(self, last):
                raise Exception('1 does not equal 2')

            def we_get_an_understandable_message(self, topic):
                expect(topic).to_have_an_error_message_of('1 does not equal 2')

        class WhenErrorMessagesDoNotMatch(Vows.Context):
            def topic(self, last):
                try:
                    expect(last).to_have_an_error_message_of('some bogus')
                except AssertionError as e:
                    return e

            def we_get_an_understandable_message(self, topic):
                expected_message = "Expected topic({0!r}) to be an error with message {1!r}".format(
                        utils.text_type(ValueError('some bogus error')),
                        'some bogus'
                        )
                expect(topic).to_have_an_error_message_of(expected_message)


        class ToBeAnError(Vows.Context):
            def we_can_see_that_is_an_error_instance(self, topic):
                expect(topic).to_be_an_error()

            class WhenWeGetAnError(Vows.Context):
                @Vows.capture_error
                def topic(self, last):
                    expect(2).to_be_an_error()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(2) to be an error")


        class NotToBeAnError(Vows.Context):
            def topic(self):
                return 2

            def we_can_see_that_is_not_an_error_instance(self, topic):
                expect(topic).not_to_be_an_error()


            class WhenWeGetAnError(Vows.Context):
                def topic(self, last):
                    try:
                        expect(last).to_be_an_error()
                    except AssertionError as e:
                        return e, last

                def we_get_an_understandable_message(self, topic):
                    expect(topic[0]).to_have_an_error_message_of("Expected topic({0}) to be an error".format(topic[1]))




