#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class MultipleTopics(Vows.Context):
    class FirstLevel(Vows.Context):
        def topic(self):
            return 'a'

        def is_a(self, topic):
            expect(topic).to_equal('a')

        class SecondLevel(Vows.Context):
            def topic(self, first):
                return (first, 'b')

            def still_a(self, topic):
                expect(topic[0]).to_equal('a')

            def is_b(self, topic):
                expect(topic[1]).to_equal('b')

            class ThirdLevel(Vows.Context):
                def topic(self, second, first):
                    return (first, second[1], 'c')

                def still_a(self, topic):
                    expect(topic[0]).to_equal('a')

                def still_b(self, topic):
                    expect(topic[1]).to_equal('b')

                def is_c(self, topic):
                    expect(topic[2]).to_equal('c')
