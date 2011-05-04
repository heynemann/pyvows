#!/usr/bin/env python

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

