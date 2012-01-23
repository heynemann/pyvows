#!/usr/bin/env python

import time
from pyvows import Vows, expect

@Vows.batch
class TheFirstBatch(Vows.Context):
    def topic(self):
        globals()['database'] = {}

    def sets_up_some_huge_test_environment(self, topic):
        return expect(globals()['database']).to_equal({})

@Vows.batch
class TheSecondBatch(Vows.Context):
    def topic(self):
        globals()['database']['pie'] = 42
        time.sleep(0.1)

    def does_some_huge_and_complicated_database_jobs(self, topic):
        expect(database).to_be_like({'pie': 42})

@Vows.batch
class TheThirdBatch(Vows.Context):
    def topic(self):
        del(globals()['database'])

    def tears_down_the_test_environment(self, topic):
        expect(globals().get('database')).to_equal(None)
