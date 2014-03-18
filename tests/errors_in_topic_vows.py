#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Richard Lupton r.lupton@gmail.com

from pyvows import Vows, expect


# These tests demonstrate what happens when the topic function raises
# or returns an exception.

@Vows.batch
class ErrorsInTopicFunction(Vows.Context):

    class WhenTopicRaisesAnException:
        def topic(self):
            return 42 / 0

        def tests_should_not_run(self, topic):
            raise RuntimeError("Should not reach here")

        class SubContext:
            def subcontexts_should_also_not_run(self, topic):
                raise RuntimeError("Should not reach here")

    class WhenTopicRaisesAnExceptionWithCaptureErrorDecorator:
        @Vows.capture_error
        def topic(self):
            return 42 / 0

        def it_is_passed_to_tests_as_normal(self, topic):
            expect(topic).to_be_an_error_like(ZeroDivisionError)

    class WhenTopicReturnsAnException:
        def topic(self):
            try:
                return 42 / 0
            except Exception as e:
                return e

        def it_is_passed_to_tests_as_normal(self, topic):
            expect(topic).to_be_an_error_like(ZeroDivisionError)
