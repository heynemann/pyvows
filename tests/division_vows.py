#!/usr/bin/env python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from pyvows import Vows

@Vows.batch
class DivisionTests(Vows.Context):

    #class WhenDividingNumberByZero(Vows.Context):
    def topic(self):
        return 42 / 1

    def we_get_a_number(self, topic):
        Vows.Assert.is_numeric(topic)

    def we_get_42(self, topic):
        Vows.Assert.are_equal(topic, 42)

