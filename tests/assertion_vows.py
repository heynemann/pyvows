#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


@Vows.batch
class Assertion(Vows.Context):

    class WhenUTF8Topic(Vows.Context):
        def topic(self):
            return u"some á é í ó ç"

        def should_not_fail(self, topic):
            expect(topic).to_equal(u'some á é í ó ç')

    class NonErrorContext(Vows.NotErrorContext):
        def topic(self):
            return 42

    class NotEmptyContext(Vows.NotEmptyContext):
        def topic(self):
            return "harmless"

    class WhenNotHaveTopic(Vows.Context):
        def we_can_see_topic_as_none(self, topic):
            expect(topic).to_be_null()

