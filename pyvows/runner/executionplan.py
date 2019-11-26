# -*- coding: utf-8 -*-
'''The logic PyVows uses to discover contexts and vows'''

import inspect
import re


class ExecutionPlanner(object):
    def __init__(self, suites, exclusion_patterns, inclusion_patterns):
        self.suites = suites
        if exclusion_patterns and inclusion_patterns:
            raise Exception('Using both exclusion_patterns and inclusion_patterns is not allowed')
        self.exclusion_patterns = set([re.compile(x) for x in exclusion_patterns])
        self.inclusion_patterns = set([re.compile(x) for x in inclusion_patterns])

    def plan(self):
        plan = {}
        for suiteName, contextClasses in self.suites.items():
            plan[suiteName] = {
                'contexts': {}
            }
            for contextClass in contextClasses:
                contextPlan, isRequired = self.plan_context(contextClass, '')
                if isRequired and not self.is_excluded(contextPlan['name']):
                    plan[suiteName]['contexts'][contextClass.__name__] = contextPlan
        return plan

    def is_excluded(self, name):
        '''Return whether `name` is in `self.exclusion_patterns`.'''

        for pattern in self.exclusion_patterns:
            if pattern.search(name):
                return True
        return False

    def is_included(self, name):
        '''Return whether `name` is in `self.inclusion_patterns`.'''

        if not self.inclusion_patterns:
            return True

        for pattern in self.inclusion_patterns:
            if pattern.search(name):
                return True
        return False

    def plan_context(self, contextClass, idBase):
        context = {
            'name': contextClass.__name__,
            'id': idBase + ('.' if idBase else '') + contextClass.__name__,
            'contexts': {},
            'vows': []
        }

        special_names = set(['setup', 'teardown', 'topic'])
        if hasattr(contextClass, 'ignored_members'):
            special_names.update(contextClass.ignored_members)

        # remove any special methods
        contextMembers = [
            (name, value) for name, value in inspect.getmembers(contextClass)
            if name not in special_names and not name.startswith('_')
        ]

        context['vows'] = [
            name for name, vow in contextMembers
            if (inspect.ismethod(vow) or inspect.isfunction(vow))
               and self.is_included(context['id'] + '.' + name)
               and not self.is_excluded(name)
        ]

        subcontexts = [
            (name, subcontext) for name, subcontext in contextMembers
            if inspect.isclass(subcontext) and not self.is_excluded(name)
        ]

        for name, subcontext in subcontexts:
            subcontextPlan, subcontextContainsIncludedSubcontexts = self.plan_context(subcontext, context['id'])
            if self.is_included(subcontextPlan['id']) or subcontextContainsIncludedSubcontexts:
                context['contexts'][name] = subcontextPlan

        if self.inclusion_patterns:
            contextRequiredBecauseItContainsVowsOrSubcontexts = bool(context['contexts']) or bool(context['vows'])
        else:
            contextRequiredBecauseItContainsVowsOrSubcontexts = True

        return context, contextRequiredBecauseItContainsVowsOrSubcontexts
