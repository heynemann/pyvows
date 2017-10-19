#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect


#   TEST DATA
STRINGS = {
    'that_are_files': (
        __file__,
        (__file__.decode('utf8')
         if isinstance(__file__, bytes) \
         else __file__),
    ),

    'that_are_not_files':   (
        __doc__,
    )
}


#   HELPERS
isafile = lambda topic: expect(topic).to_be_a_file()
isnotafile = lambda topic: expect(topic).not_to_be_a_file()


#   NOW, MAKE YOUR VOWS.

@Vows.batch
class WhenMakingFileAssertions(Vows.Context):
    #   @TODO:  Clean up this repetitive test code
    #
    #           Preferable one of the following:
    #
    #           -   context inheritance
    #               http://pyvows.org/#-context-inheritance
    #
    #           -   generative testing
    #               http://pyvows.org/#-using-generative-testing

    class OnFilesThatDoNotExist(Vows.Context):
        def topic(self):
            for item in STRINGS['that_are_not_files']:
                yield item

        class AssertingThatTheyDo(Vows.Context):
            @Vows.capture_error
            def topic(self, parent_topic):
                return isafile(parent_topic)

            def should_raise_an_error(self, topic):
                expect(topic).to_be_an_error_like(AssertionError)

        class AssertingThatTheyDoNot(Vows.Context):
            @Vows.capture_error
            def topic(self, parent_topic):
                return isnotafile(parent_topic)

            def should_raise_no_errors(self, topic):
                expect(topic).Not.to_be_an_error()

    class OnFilesThatDoExist(Vows.Context):
        def topic(self):
            for item in STRINGS['that_are_files']:
                yield item

        class AssertingTheyAreFiles(Vows.Context):
            @Vows.capture_error
            def topic(self, parent_topic):
                return isafile(parent_topic)

            def should_not_raise_errors(self, topic):
                expect(topic).not_to_be_an_error()

        class AssertingTheyAreNotFiles(Vows.Context):
            @Vows.capture_error
            def topic(self, parent_topic):
                return isnotafile(parent_topic)

            def should_raise_an_error(self, topic):
                expect(topic).to_be_an_error()

        class WhenWeInstantiateThemAsFileObjects(Vows.Context):
            def topic(self, parent_topic):
                f = open(parent_topic)
                return f

            class AssertingTheyAreFiles(Vows.Context):
                @Vows.capture_error
                def topic(self, parent_topic):
                    return isafile(parent_topic)

                def should_not_raise_errors(self, topic):
                    expect(topic).not_to_be_an_error()

            class AssertingTheyAreNotFiles(Vows.Context):
                @Vows.capture_error
                def topic(self, parent_topic):
                    return isnotafile(parent_topic)

                def should_raise_an_error(self, topic):
                    expect(topic).to_be_an_error()
