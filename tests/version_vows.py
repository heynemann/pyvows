# -*- coding: utf-8 -*-

from pyvows import Vows, expect
import pyvows.version as pyvows_version


@Vows.batch
class PyvowsVersionModule(Vows.Context):
    def topic(self):
        return pyvows_version

    def has_a_docstring(self, topic):
        expect(hasattr(topic, '__doc__')).to_be_true()

    class VersionNumber(Vows.Context):
        def topic(self, topic):
            return topic.__version__

        def should_be_a_tuple(self, topic):
            expect(topic).to_be_instance_of(tuple)

        def should_have_length_of_3(self, topic):
            expect(topic).to_length(3)

        def shoud_not_be_empty(self, topic):
            expect(topic).Not.to_be_empty()

        def should_not_be_None(self, topic):
            expect(topic).Not.to_be_null()

    class VersionString(Vows.Context):
        def topic(self, topic):
            return topic.to_str()

        def should_not_be_empty(self, topic):
            expect(topic).Not.to_be_empty()

        def should_not_be_None(self, topic):
            expect(topic).Not.to_be_null()

        def should_be_a_string(self, topic):
            expect(topic).to_be_instance_of(str)
