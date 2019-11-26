#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import time

from pyvows import Vows, expect

#-------------------------------------------------------------------------------------------------

def asyncFunc(pool, callback):
    def _async():
        time.sleep(0.1)
        return 10

    def get_value(value):
        callback(value, 20, kwarg=30, kw2=40)
    pool.apply_async(_async, callback=get_value)

#-------------------------------------------------------------------------------------------------

@Vows.batch
class AsyncTopic(Vows.Context):
    @Vows.async_topic
    def topic(self, callback):
        asyncFunc(self.pool, callback)

    def should_check_the_first_parameter(self, topic):
        expect(topic[0]).to_equal(10)

    def should_check_the_second_parameter(self, topic):
        expect(topic.args[1]).to_equal(20)

    def should_check_the_kwarg_parameter(self, topic):
        expect(topic.kwarg).to_equal(30)

    def should_check_the_kwarg_parameter_accesing_from_topic_as_dict(self, topic):
        expect(topic['kwarg']).to_equal(30)

    def should_check_the_kw2_parameter(self, topic):
        expect(topic.kw['kw2']).to_equal(40)

    class SyncTopic(Vows.Context):
        def topic(self):
            return 1

        def should_be_1(self, topic):
            expect(topic).to_equal(1)

        class NestedAsyncTest(Vows.Context):
            @Vows.async_topic
            def topic(self, callback, old_topic):
                def cb(*args, **kw):
                    args = (old_topic,) + args
                    return callback(*args, **kw)
                asyncFunc(self.pool, cb)

            def should_be_the_value_of_the_old_topic(self, topic):
                expect(topic.args[0]).to_equal(1)

            class NestedSyncTopic(Vows.Context):
                def topic(self):
                    return 1

                def should_be_1(self, topic):
                    expect(topic).to_equal(1)
