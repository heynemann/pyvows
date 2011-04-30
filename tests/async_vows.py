#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import time

import eventlet

from pyvows import Vows, expect

pool = eventlet.GreenPool()

def asyncFunc(callback):
    def async():
        time.sleep(2)
        return 10

    func = pool.spawn(async)

    def get_value(gt, callback):
        value = gt.wait()

        callback(value)

    func.link(get_value, callback)

@Vows.batch
class AsyncTopic(Vows.Context):
    def topic(self):
        return Vows.AsyncTopic(asyncFunc)

    def should_return_10(self, topic):
        expect(topic).to_equal(10)
