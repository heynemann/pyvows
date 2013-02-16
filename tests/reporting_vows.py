#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect
from pyvows.reporting import VowsDefaultReporter


@Vows.batch
class CoverageXMLParser(Vows.Context):

    def topic(self):
        return VowsDefaultReporter(None, 0)

    def should_be_an_instance_of_class(self, inst):
        expect(inst).to_be_instance_of(VowsDefaultReporter)

    class WhenParseCoverageXMLResult:
        """
            {'overall': 99.0, 'classes': [ {'name': 'pyvows.cli', 'line_rate': 0.0568, 'uncovered_lines':[ 12, 13 ] }, ] }
        """

        def topic(self, default_reporter):
            return default_reporter.parse_coverage_xml('''<?xml version="1.0" ?>
<!DOCTYPE coverage
  SYSTEM 'http://cobertura.sourceforge.net/xml/coverage-03.dtd'>
<coverage branch-rate="0" line-rate="0.99" timestamp="1331692518922" version="3.5.1">
    <packages>
        <package branch-rate="0" complexity="0" line-rate="0.99" name="pyvows">
            <classes>
                <class branch-rate="0" complexity="0" filename="pyvows/cli.py" line-rate="0.568" name="cli">
                    <methods/>
                    <lines>
                        <line hits="0" number="12"/>
                        <line hits="1" number="13"/>
                        <line hits="0" number="14"/>
                    </lines>
                </class>
            </classes>
        </package>
        <package branch-rate="0" complexity="0" line-rate="0.99" name="tests">
            <classes>
                <class branch-rate="0" complexity="0" filename="tests/bla.py" line-rate="0.88" name="bla">
                    <methods/>
                    <lines>
                        <line hits="1" number="1"/>
                        <line hits="0" number="2"/>
                        <line hits="0" number="3"/>
                    </lines>
                </class>
            </classes>
        </package>
    </packages>
</coverage>''')

        def should_return_a_dict(self, result):
            expect(result).to_be_instance_of(dict)

        def should_contain_only_one_package(self, result):
            expect(len(result['classes'])).to_equal(2)

        def should_be_overall_99(self, result):
            expect(result['overall']).to_equal(0.99)

        class TheFirstClass(Vows.Context):

            def topic(self, result):
                return result['classes'][0]

            def should_be_pyvows_cli(self, klass):
                expect(klass['name']).to_equal('pyvows.cli')

            def should_contain_linehate(self, klass):
                expect(klass['line_rate']).to_equal(0.568)

            def should_contain_lines_uncovered(self, klass):
                expect(klass['uncovered_lines']).to_equal(['12', '14'])

        class TheSecondClass(Vows.Context):

            def topic(self, result):
                return result['classes'][1]

            def should_be_pyvowsconsole(self, klass):
                expect(klass['name']).to_equal('tests.bla')

            def should_contain_linehate(self, klass):
                expect(klass['line_rate']).to_equal(0.88)

            def should_contain_lines_uncovered(self, klass):
                expect(klass['uncovered_lines']).to_equal(['2', '3'])
