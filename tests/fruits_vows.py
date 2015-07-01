#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


class Strawberry(object):
    def __init__(self):
        self.color = '#ff0000'

    def isTasty(self):
        return True


class PeeledBanana(object):
    pass


class Banana(object):
    def __init__(self):
        self.color = '#fff333'

    def peel(self):
        return PeeledBanana()


@Vows.batch
class TheGoodThings(Vows.Context):
    class AStrawberry(Vows.Context):
        def topic(self):
            return Strawberry()

        def is_red(self, topic):
            expect(topic.color).to_equal('#ff0000')

        def and_tasty(self, topic):
            expect(topic.isTasty()).to_be_true()

    class ABanana(Vows.Context):
        def topic(self):
            return Banana()

        class WhenPeeled(Vows.Context):
            def topic(self, banana):
                return banana.peel()

            def returns_a_peeled_banana(self, topic):
                expect(topic).to_be_instance_of(PeeledBanana)
