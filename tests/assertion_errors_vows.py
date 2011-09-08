#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class AssertionErrors(Vows.Context):
    class WhenRaises(Vows.Context):
        def topic(self):
            raise ValueError('some bogus error')

        class BeAnErrorLike(Vows.Context):

            def we_can_see_it_was_a_value_error(self, topic):
                expect(topic).to_be_an_error_like(ValueError)

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(NotImplementedError('no')).to_be_an_error_like(OSError)

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of(
                            "Expected topic(%s) to be an error of type %s, but it was a %s." % (
                                repr(NotImplementedError('no')), repr(OSError), repr(NotImplementedError)))

        class HaveErrorMessageOf(Vows.Context):

            def we_can_see_that_is_has_error_message_of(self, topic):
                expect(topic).to_have_an_error_message_of("some bogus error")

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(last).to_have_an_error_message_of('some bogus')

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of(
                            "Expected topic(%s) to be an error with message '%s'." % (
                                repr(ValueError('some bogus error')), 'some bogus'))

        class ToBeAnError(Vows.Context):

            def we_can_see_that_is_an_error_instance(self, topic):
                expect(topic).to_be_an_error()

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(2).to_be_an_error()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(2) to be an error.")

        class NotToBeAnError(Vows.Context):
            def topic(self):
                return 2

            def we_can_see_that_is_not_an_error_instance(self, topic):
                expect(topic).not_to_be_an_error()

            class WhenWeGetAnError(Vows.Context):

                def topic(self, last):
                    expect(ValueError).not_to_be_an_error()

                def we_get_an_understandable_message(self, topic):
                    expect(topic).to_have_an_error_message_of("Expected topic(%s) not to be an error." % str(ValueError))
        class TheExceptionClass(Vows.Context):
            def topic(self, error):
                return ValueError

            def we_can_see_that_is_an_error_class(self, topic):
                expect(topic).to_be_an_error()


    class WhenDontRaise(Vows.Context):
        def topic(self):
            return 0

        def we_can_see_that_is_not_an_error(self, topic):
            expect(topic).Not.to_be_an_error()


