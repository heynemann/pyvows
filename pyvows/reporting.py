#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyvows testing engine
# https://github.com/heynemann/pyvows

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys
import re

from lxml import etree
from colorama import init, Fore, Style

class VowsDefaultReporter(object):
    honored = Fore.GREEN + Style.BRIGHT + '✓' + Fore.RESET + Style.RESET_ALL
    broken = Fore.RED + Style.BRIGHT + '✗' + Fore.RESET + Style.RESET_ALL

    def __init__(self, result):
        init(autoreset=True)
        self.result = result
        self.tab = " " * 2
        self.indent = 1

    def camel_split(self, string):
        return re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z])|(?=[0-9]\b))', ' ', string).strip()

    def under_split(self, string):
        return ' '.join(string.split('_'))

    @classmethod
    def handle_success(cls, vow):
        sys.stdout.write(cls.honored)

    @classmethod
    def handle_error(cls, vow):
        sys.stdout.write(cls.broken)

    def pretty_print(self):
        print
        print
        if not self.result:
            print " %s No vows found! » 0 honored • 0 broken (0.0s)" % self.broken
            return

        for name, context in self.result.contexts.iteritems():
            self.print_context(name, context)
        print
        print "%s%s OK » %d honored • %d broken (%.6fs)" % (
                self.tab * self.indent,
                self.honored if self.result.successful else self.broken,
                self.result.successful_tests,
                self.result.errored_tests,
                self.result.ellapsed_time
        )

    def print_context(self, name, context):
        print "%s%s" % (self.tab * self.indent, self.camel_split(name).capitalize())
        self.indent += 1

        print_test = lambda icon, test_name: "%s%s %s" % (self.tab * self.indent, icon, self.camel_split(self.under_split(test_name)).capitalize())

        for test in context['tests']:
            if test['succeeded']:
                print print_test(VowsDefaultReporter.honored, test['name'])
            else:
                print print_test(VowsDefaultReporter.broken, test['name'])
                print "%s%s" % (self.tab * (self.indent + 2), Fore.RED + str(test['error']) + Fore.RESET)
                if 'file' in test:
                    print "%s%s" % (self.tab * (self.indent + 3), Fore.RED + "(found in %s at line %s)" % (test['file'], test['lineno']) + Fore.RESET)
        for name, context in context['contexts'].iteritems():
            self.print_context(name, context)

        self.indent -= 1

    def print_coverage(self, xml, cover_threshold):
        write_blue = lambda msg: Fore.BLUE + Style.BRIGHT + str(msg) + Style.RESET_ALL + Fore.RESET
        write_white = lambda msg: Fore.WHITE + Style.BRIGHT + str(msg) + Style.RESET_ALL + Fore.RESET

        root = etree.fromstring(xml)

        klasses = root.xpath('//class')
        names = ['.'.join([klass.getparent().getparent().attrib['name'], klass.attrib['name']]) for klass in klasses]
        max_length = max([len(klass_name) for klass_name in names])
        max_coverage = max([int(round(float(klass.attrib['line-rate']) * 100, 0)) for klass in klasses])

        print ' ' + '=' * len('Code Coverage')
        print Fore.GREEN + Style.BRIGHT + " Code Coverage" + Style.RESET_ALL + Fore.RESET
        print ' ' + '=' * len('Code Coverage')
        print

        klasses = sorted(klasses, key=lambda klass: float(klass.attrib['line-rate']))

        for klass in klasses:
            package_name = klass.getparent().getparent().attrib['name']
            klass_name = '.'.join([package_name, klass.attrib['name']])
            coverage = float(klass.attrib['line-rate']) * 100
            if coverage < cover_threshold:
                cover_character = self.broken
            else:
                cover_character = self.honored

            uncovered_lines = [line.attrib['number'] for line in klass.find('lines') if line.attrib['hits'] == '0']

            coverage = int(round(coverage, 0))
            offset = coverage == 0 and 2 or (coverage < 10 and 1 or 0)
            print " %s %s%s\t%s%s%%%s %s" % (cover_character,
                                        write_blue(klass_name),
                                        ' ' * (max_length - len(klass_name)),
                                        '•' * coverage,
                                        write_white((coverage > 0 and ' ' or '') + '%.2f' % coverage),
                                        ' ' * (max_coverage - coverage + offset),
                                        self.get_uncovered_lines(uncovered_lines))

        print
        total_coverage = float(root.xpath('//coverage')[0].attrib['line-rate']) * 100
        print " %s %s%s\t%s %s%%" % (self.broken,
                                    write_blue('OVERALL'),
                                    ' ' * (max_length - len('OVERALL')),
                                    '•' * int(round(total_coverage, 0)),
                                    write_white('%.2f' % total_coverage))

        print

    def get_uncovered_lines(self, uncovered_lines, number_of=3):
        if len(uncovered_lines) > number_of:
            template_str = []
            for i in range(number_of):
                template_str.append(uncovered_lines[i])
                if not i == number_of - 1:
                    template_str += " ,"

            template_str.append(" and %d more" % (len(uncovered_lines) - number_of))

            return "".join(template_str)

        return ", ".join(uncovered_lines)




#<?xml version="1.0" ?>
#<!DOCTYPE coverage
  #SYSTEM 'http://cobertura.sourceforge.net/xml/coverage-03.dtd'>
#<coverage branch-rate="0" line-rate="0.3564" timestamp="1304205443244" version="3.4">
	#<!-- Generated by coverage.py: http://nedbatchelder.com/code/coverage -->
	#<packages>
		#<package branch-rate="0" complexity="0" line-rate="0.3012" name="pyvows">
			#<classes>
				#<class branch-rate="0" complexity="0" filename="pyvows/__init__.py" line-rate="0" name="__init__">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="12"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="14"/>
						#<line hits="0" number="15"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/console.py" line-rate="0" name="console">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="12"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="15"/>
						#<line hits="0" number="16"/>
						#<line hits="0" number="17"/>
						#<line hits="0" number="18"/>
						#<line hits="0" number="19"/>
						#<line hits="0" number="20"/>
						#<line hits="0" number="22"/>
						#<line hits="0" number="23"/>
						#<line hits="0" number="24"/>
						#<line hits="0" number="25"/>
						#<line hits="0" number="26"/>
						#<line hits="0" number="28"/>
						#<line hits="0" number="29"/>
						#<line hits="0" number="31"/>
						#<line hits="0" number="32"/>
						#<line hits="0" number="33"/>
						#<line hits="0" number="34"/>
						#<line hits="0" number="35"/>
						#<line hits="0" number="37"/>
						#<line hits="0" number="38"/>
						#<line hits="0" number="40"/>
						#<line hits="0" number="41"/>
						#<line hits="0" number="43"/>
						#<line hits="0" number="44"/>
						#<line hits="0" number="45"/>
						#<line hits="0" number="47"/>
						#<line hits="0" number="49"/>
						#<line hits="0" number="51"/>
						#<line hits="0" number="52"/>
						#<line hits="0" number="53"/>
						#<line hits="0" number="54"/>
						#<line hits="0" number="56"/>
						#<line hits="0" number="58"/>
						#<line hits="0" number="59"/>
						#<line hits="0" number="60"/>
						#<line hits="0" number="61"/>
						#<line hits="0" number="62"/>
						#<line hits="0" number="64"/>
						#<line hits="0" number="66"/>
						#<line hits="0" number="68"/>
						#<line hits="0" number="69"/>
						#<line hits="0" number="71"/>
						#<line hits="0" number="72"/>
						#<line hits="0" number="73"/>
						#<line hits="0" number="74"/>
						#<line hits="0" number="76"/>
						#<line hits="0" number="78"/>
						#<line hits="0" number="79"/>
						#<line hits="0" number="81"/>
						#<line hits="0" number="83"/>
						#<line hits="0" number="85"/>
						#<line hits="0" number="86"/>
						#<line hits="0" number="87"/>
						#<line hits="0" number="89"/>
						#<line hits="0" number="90"/>
						#<line hits="0" number="91"/>
						#<line hits="0" number="92"/>
						#<line hits="0" number="93"/>
						#<line hits="0" number="94"/>
						#<line hits="0" number="96"/>
						#<line hits="0" number="97"/>
						#<line hits="0" number="99"/>
						#<line hits="0" number="100"/>
						#<line hits="0" number="102"/>
						#<line hits="0" number="103"/>
						#<line hits="0" number="104"/>
						#<line hits="0" number="105"/>
						#<line hits="0" number="107"/>
						#<line hits="0" number="109"/>
						#<line hits="0" number="110"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/core.py" line-rate="0.3086" name="core">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="12"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="14"/>
						#<line hits="0" number="15"/>
						#<line hits="0" number="17"/>
						#<line hits="0" number="19"/>
						#<line hits="0" number="20"/>
						#<line hits="0" number="22"/>
						#<line hits="0" number="23"/>
						#<line hits="0" number="24"/>
						#<line hits="0" number="25"/>
						#<line hits="0" number="26"/>
						#<line hits="0" number="27"/>
						#<line hits="0" number="29"/>
						#<line hits="0" number="31"/>
						#<line hits="0" number="33"/>
						#<line hits="1" number="34"/>
						#<line hits="1" number="35"/>
						#<line hits="0" number="37"/>
						#<line hits="1" number="38"/>
						#<line hits="0" number="39"/>
						#<line hits="1" number="41"/>
						#<line hits="1" number="42"/>
						#<line hits="1" number="43"/>
						#<line hits="1" number="45"/>
						#<line hits="1" number="46"/>
						#<line hits="0" number="47"/>
						#<line hits="1" number="49"/>
						#<line hits="1" number="50"/>
						#<line hits="1" number="52"/>
						#<line hits="0" number="54"/>
						#<line hits="0" number="55"/>
						#<line hits="1" number="56"/>
						#<line hits="1" number="57"/>
						#<line hits="1" number="58"/>
						#<line hits="0" number="60"/>
						#<line hits="0" number="61"/>
						#<line hits="0" number="62"/>
						#<line hits="0" number="63"/>
						#<line hits="0" number="65"/>
						#<line hits="0" number="66"/>
						#<line hits="0" number="67"/>
						#<line hits="0" number="68"/>
						#<line hits="0" number="71"/>
						#<line hits="0" number="72"/>
						#<line hits="0" number="74"/>
						#<line hits="0" number="75"/>
						#<line hits="1" number="76"/>
						#<line hits="1" number="77"/>
						#<line hits="0" number="79"/>
						#<line hits="1" number="80"/>
						#<line hits="1" number="81"/>
						#<line hits="1" number="83"/>
						#<line hits="1" number="84"/>
						#<line hits="1" number="86"/>
						#<line hits="0" number="88"/>
						#<line hits="0" number="90"/>
						#<line hits="0" number="92"/>
						#<line hits="0" number="94"/>
						#<line hits="0" number="95"/>
						#<line hits="0" number="97"/>
						#<line hits="0" number="99"/>
						#<line hits="0" number="101"/>
						#<line hits="0" number="103"/>
						#<line hits="1" number="104"/>
						#<line hits="0" number="105"/>
						#<line hits="1" number="106"/>
						#<line hits="0" number="107"/>
						#<line hits="0" number="108"/>
						#<line hits="0" number="110"/>
						#<line hits="1" number="112"/>
						#<line hits="1" number="114"/>
						#<line hits="0" number="116"/>
						#<line hits="0" number="118"/>
						#<line hits="0" number="120"/>
						#<line hits="0" number="122"/>
						#<line hits="0" number="123"/>
						#<line hits="0" number="124"/>
						#<line hits="0" number="125"/>
						#<line hits="0" number="126"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/reporting.py" line-rate="0.02222" name="reporting">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="12"/>
						#<line hits="0" number="14"/>
						#<line hits="0" number="16"/>
						#<line hits="0" number="17"/>
						#<line hits="0" number="18"/>
						#<line hits="0" number="20"/>
						#<line hits="0" number="21"/>
						#<line hits="0" number="22"/>
						#<line hits="0" number="23"/>
						#<line hits="0" number="24"/>
						#<line hits="0" number="26"/>
						#<line hits="0" number="27"/>
						#<line hits="0" number="29"/>
						#<line hits="0" number="30"/>
						#<line hits="0" number="32"/>
						#<line hits="1" number="34"/>
						#<line hits="0" number="36"/>
						#<line hits="0" number="38"/>
						#<line hits="0" number="40"/>
						#<line hits="0" number="41"/>
						#<line hits="0" number="42"/>
						#<line hits="0" number="43"/>
						#<line hits="0" number="44"/>
						#<line hits="0" number="45"/>
						#<line hits="0" number="47"/>
						#<line hits="0" number="48"/>
						#<line hits="0" number="49"/>
						#<line hits="0" number="50"/>
						#<line hits="0" number="58"/>
						#<line hits="0" number="59"/>
						#<line hits="0" number="60"/>
						#<line hits="0" number="62"/>
						#<line hits="0" number="64"/>
						#<line hits="0" number="65"/>
						#<line hits="0" number="66"/>
						#<line hits="0" number="68"/>
						#<line hits="0" number="69"/>
						#<line hits="0" number="70"/>
						#<line hits="0" number="71"/>
						#<line hits="0" number="72"/>
						#<line hits="0" number="73"/>
						#<line hits="0" number="75"/>
						#<line hits="0" number="77"/>
						#<line hits="0" number="78"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/result.py" line-rate="0.07407" name="result">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="12"/>
						#<line hits="1" number="13"/>
						#<line hits="1" number="14"/>
						#<line hits="0" number="16"/>
						#<line hits="0" number="18"/>
						#<line hits="0" number="20"/>
						#<line hits="0" number="22"/>
						#<line hits="0" number="24"/>
						#<line hits="0" number="26"/>
						#<line hits="0" number="28"/>
						#<line hits="0" number="30"/>
						#<line hits="0" number="32"/>
						#<line hits="0" number="33"/>
						#<line hits="0" number="35"/>
						#<line hits="0" number="36"/>
						#<line hits="0" number="38"/>
						#<line hits="0" number="39"/>
						#<line hits="0" number="40"/>
						#<line hits="0" number="42"/>
						#<line hits="0" number="44"/>
						#<line hits="0" number="45"/>
						#<line hits="0" number="46"/>
						#<line hits="0" number="47"/>
						#<line hits="0" number="49"/>
						#<line hits="0" number="50"/>
						#<line hits="0" number="52"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/runner.py" line-rate="0.72" name="runner">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="12"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="15"/>
						#<line hits="0" number="17"/>
						#<line hits="0" number="19"/>
						#<line hits="0" number="20"/>
						#<line hits="1" number="21"/>
						#<line hits="1" number="22"/>
						#<line hits="1" number="23"/>
						#<line hits="1" number="24"/>
						#<line hits="1" number="25"/>
						#<line hits="1" number="26"/>
						#<line hits="1" number="27"/>
						#<line hits="0" number="29"/>
						#<line hits="1" number="30"/>
						#<line hits="1" number="31"/>
						#<line hits="1" number="33"/>
						#<line hits="1" number="34"/>
						#<line hits="1" number="36"/>
						#<line hits="0" number="38"/>
						#<line hits="0" number="39"/>
						#<line hits="0" number="41"/>
						#<line hits="0" number="43"/>
						#<line hits="0" number="44"/>
						#<line hits="0" number="45"/>
						#<line hits="0" number="47"/>
						#<line hits="1" number="48"/>
						#<line hits="1" number="49"/>
						#<line hits="1" number="54"/>
						#<line hits="1" number="56"/>
						#<line hits="1" number="57"/>
						#<line hits="1" number="58"/>
						#<line hits="1" number="59"/>
						#<line hits="1" number="60"/>
						#<line hits="1" number="61"/>
						#<line hits="1" number="62"/>
						#<line hits="1" number="63"/>
						#<line hits="1" number="65"/>
						#<line hits="1" number="67"/>
						#<line hits="1" number="68"/>
						#<line hits="1" number="70"/>
						#<line hits="1" number="71"/>
						#<line hits="1" number="72"/>
						#<line hits="1" number="73"/>
						#<line hits="1" number="75"/>
						#<line hits="1" number="76"/>
						#<line hits="1" number="78"/>
						#<line hits="1" number="79"/>
						#<line hits="1" number="81"/>
						#<line hits="1" number="82"/>
						#<line hits="1" number="83"/>
						#<line hits="1" number="84"/>
						#<line hits="1" number="86"/>
						#<line hits="1" number="88"/>
						#<line hits="1" number="89"/>
						#<line hits="1" number="91"/>
						#<line hits="1" number="94"/>
						#<line hits="0" number="96"/>
						#<line hits="1" number="97"/>
						#<line hits="1" number="98"/>
						#<line hits="1" number="99"/>
						#<line hits="1" number="107"/>
						#<line hits="1" number="108"/>
						#<line hits="1" number="109"/>
						#<line hits="1" number="110"/>
						#<line hits="1" number="111"/>
						#<line hits="1" number="112"/>
						#<line hits="0" number="113"/>
						#<line hits="0" number="114"/>
						#<line hits="0" number="115"/>
						#<line hits="0" number="116"/>
						#<line hits="1" number="118"/>
						#<line hits="1" number="120"/>
						#<line hits="0" number="122"/>
						#<line hits="1" number="123"/>
						#<line hits="1" number="124"/>
						#<line hits="0" number="125"/>
						#<line hits="0" number="126"/>
						#<line hits="1" number="128"/>
						#<line hits="1" number="129"/>
						#<line hits="1" number="131"/>
						#<line hits="0" number="133"/>
						#<line hits="1" number="134"/>
						#<line hits="1" number="135"/>
						#<line hits="1" number="137"/>
						#<line hits="1" number="138"/>
						#<line hits="0" number="139"/>
						#<line hits="0" number="140"/>
						#<line hits="1" number="142"/>
						#<line hits="0" number="143"/>
						#<line hits="1" number="145"/>
						#<line hits="1" number="147"/>
						#<line hits="1" number="149"/>
						#<line hits="1" number="150"/>
						#<line hits="1" number="151"/>
						#<line hits="0" number="152"/>
						#<line hits="1" number="153"/>
						#<line hits="1" number="154"/>
						#<line hits="1" number="156"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/version.py" line-rate="0" name="version">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
					#</lines>
				#</class>
			#</classes>
		#</package>
		#<package branch-rate="0" complexity="0" line-rate="0.4962" name="pyvows.assertions">
			#<classes>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/__init__.py" line-rate="0" name="__init__">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="12"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="14"/>
						#<line hits="0" number="15"/>
						#<line hits="0" number="16"/>
						#<line hits="0" number="17"/>
						#<line hits="0" number="18"/>
						#<line hits="0" number="19"/>
						#<line hits="0" number="20"/>
						#<line hits="0" number="21"/>
						#<line hits="0" number="22"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/boolean.py" line-rate="0.4" name="boolean">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="1" number="15"/>
						#<line hits="0" number="17"/>
						#<line hits="1" number="19"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/classes.py" line-rate="0.4" name="classes">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="1" number="15"/>
						#<line hits="0" number="17"/>
						#<line hits="1" number="19"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/emptiness.py" line-rate="0.5714" name="emptiness">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="1" number="15"/>
						#<line hits="1" number="17"/>
						#<line hits="0" number="19"/>
						#<line hits="1" number="21"/>
						#<line hits="1" number="23"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/equality.py" line-rate="0.4" name="equality">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="1" number="15"/>
						#<line hits="0" number="17"/>
						#<line hits="1" number="19"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/errors.py" line-rate="0.5" name="errors">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="15"/>
						#<line hits="1" number="17"/>
						#<line hits="0" number="19"/>
						#<line hits="1" number="21"/>
						#<line hits="0" number="23"/>
						#<line hits="1" number="25"/>
						#<line hits="0" number="27"/>
						#<line hits="1" number="29"/>
						#<line hits="1" number="30"/>
						#<line hits="1" number="32"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/function.py" line-rate="0.3333" name="function">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="15"/>
						#<line hits="1" number="17"/>
						#<line hits="0" number="19"/>
						#<line hits="1" number="21"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/inclusion.py" line-rate="0.5714" name="inclusion">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="1" number="15"/>
						#<line hits="1" number="17"/>
						#<line hits="0" number="19"/>
						#<line hits="1" number="21"/>
						#<line hits="1" number="23"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/length.py" line-rate="0.3333" name="length">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="1" number="15"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/like.py" line-rate="0.6923" name="like">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="15"/>
						#<line hits="1" number="17"/>
						#<line hits="1" number="18"/>
						#<line hits="0" number="20"/>
						#<line hits="1" number="22"/>
						#<line hits="1" number="23"/>
						#<line hits="0" number="25"/>
						#<line hits="1" number="26"/>
						#<line hits="0" number="28"/>
						#<line hits="1" number="29"/>
						#<line hits="1" number="30"/>
						#<line hits="1" number="31"/>
						#<line hits="1" number="32"/>
						#<line hits="1" number="33"/>
						#<line hits="1" number="34"/>
						#<line hits="1" number="35"/>
						#<line hits="1" number="36"/>
						#<line hits="0" number="38"/>
						#<line hits="0" number="40"/>
						#<line hits="1" number="41"/>
						#<line hits="1" number="42"/>
						#<line hits="1" number="43"/>
						#<line hits="0" number="45"/>
						#<line hits="1" number="46"/>
						#<line hits="1" number="48"/>
						#<line hits="1" number="49"/>
						#<line hits="0" number="51"/>
						#<line hits="1" number="52"/>
						#<line hits="0" number="54"/>
						#<line hits="1" number="55"/>
						#<line hits="1" number="56"/>
						#<line hits="0" number="57"/>
						#<line hits="1" number="58"/>
						#<line hits="0" number="60"/>
						#<line hits="1" number="61"/>
						#<line hits="0" number="63"/>
						#<line hits="1" number="64"/>
						#<line hits="1" number="65"/>
						#<line hits="1" number="66"/>
						#<line hits="1" number="67"/>
						#<line hits="1" number="68"/>
						#<line hits="0" number="69"/>
						#<line hits="1" number="70"/>
						#<line hits="1" number="71"/>
						#<line hits="1" number="72"/>
						#<line hits="1" number="73"/>
						#<line hits="0" number="74"/>
						#<line hits="1" number="75"/>
						#<line hits="1" number="76"/>
						#<line hits="1" number="78"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/nullable.py" line-rate="0.4" name="nullable">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="1" number="15"/>
						#<line hits="0" number="17"/>
						#<line hits="1" number="19"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/numeric.py" line-rate="0.3333" name="numeric">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="15"/>
						#<line hits="1" number="17"/>
						#<line hits="0" number="19"/>
						#<line hits="1" number="21"/>
					#</lines>
				#</class>
				#<class branch-rate="0" complexity="0" filename="pyvows/assertions/regexp.py" line-rate="0.3333" name="regexp">
					#<methods/>
					#<lines>
						#<line hits="0" number="11"/>
						#<line hits="0" number="13"/>
						#<line hits="0" number="15"/>
						#<line hits="1" number="17"/>
						#<line hits="0" number="19"/>
						#<line hits="1" number="21"/>
					#</lines>
				#</class>
			#</classes>
		#</package>
	#</packages>
#</coverage>

