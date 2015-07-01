#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com


from pyvows import Vows, expect


class NotAContextThingy(object):
    alicorns = (u'Celestia', u'Luna', u'Nyx', u'Pluto', u'Lauren Faust')

    def get_alicorns(self):
        return self.alicorns


class BaseContext(Vows.Context):

    # First case: Thingy should be ignored.
    Thingy = None

    def topic(self, ponies):
        self.ignore('Thingy', 'BaseSubcontext')
        return (self.Thingy, ponies)

    # Second case: BaseSubcontext should be ignored.
    class BaseSubcontext(Vows.Context):

        def topic(self, (Thingy, ponies)):
            self.ignore('prepare')
            for pony in ponies:
                yield (Thingy, self.prepare(pony))

        def prepare(self, something):
            raise NotImplementedError

        def pony_has_name(self, topic):
            expect(topic).to_be_true()


@Vows.batch
class PonyVows(Vows.Context):

    def topic(self):
        return ('Nyx', 'Pluto')

    class ActualContext(BaseContext):

        Thingy = NotAContextThingy

        class ActualSubcontext(BaseContext.BaseSubcontext):

            def prepare(self, something):
                return unicode(something)

            def pony_is_alicorn(self, (Thingy, pony)):
                expect(Thingy.alicorns).to_include(pony)
