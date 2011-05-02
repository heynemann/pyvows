#!/usr/bin/env python

from pyvows import Vows, expect

def get_test_data():
    for i in range(10):
        yield i

@Vows.batch
class GeneratorTests(Vows.Context):
    def topic(self):
        return get_test_data()

    def should_be_numeric(self, topic):
        expect(topic).to_be_numeric()

