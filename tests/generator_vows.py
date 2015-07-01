#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


def get_test_data():
    for i in [1] * 10:
        yield i


@Vows.batch
class GeneratorTests(Vows.Context):
    def topic(self):
        return get_test_data()

    def should_be_numeric(self, topic):
        expect(topic).to_equal(1)

    class SubContext(Vows.Context):
        def topic(self, parent_topic):
            return parent_topic

        def should_be_executed_many_times(self, topic):
            expect(topic).to_equal(1)

        class SubSubContext(Vows.Context):
            def topic(self, parent_topic, outer_topic):
                return outer_topic

            def should_be_executed_many_times(self, topic):
                expect(topic).to_equal(1)

    class GeneratorAgainContext(Vows.Context):
        def topic(self, topic):
            for i in range(10):
                yield topic * 2

        def should_return_topic_times_two(self, topic):
            expect(topic).to_equal(2)


def add(a, b):
    return a + b

a_samples = range(10)
b_samples = range(10)


@Vows.batch
class Add(Vows.Context):
    class ATopic(Vows.Context):
        def topic(self):
            for a in a_samples:
                yield a

        class BTopic(Vows.Context):
            def topic(self, a):
                for b in b_samples:
                    yield b

            class Sum(Vows.Context):
                def topic(self, b, a):
                    yield (add(a, b), a + b)

                def should_be_numeric(self, topic):
                    value, expected = topic
                    expect(value).to_be_numeric()

                def should_equal_to_expected(self, topic):
                    value, expected = topic
                    expect(value).to_equal(expected)
