from pyvows import Vows, expect
from pyvows.runner.executionplan import ExecutionPlanner


@Vows.batch
class DiscoveringExecutionTree(Vows.Context):

    class NormalBatch(Vows.Context):
        def topic(self):
            planner = ExecutionPlanner(
                {'dummySuite': set([UnrunnableBatch])},
                set([]),
                set([])
            )
            return planner.plan()

        def the_tree_matches(self, topic):
            baseline = {
                'dummySuite': {
                    'contexts': {
                        'UnrunnableBatch': {
                            'name': 'UnrunnableBatch',
                            'id': 'UnrunnableBatch',
                            'vows': [],
                            'contexts': {
                                'SubA': {
                                    'name': 'SubA',
                                    'id': 'UnrunnableBatch.SubA',
                                    'vows': [],
                                    'contexts': {}
                                },
                                'SubB': {
                                    'name': 'SubB',
                                    'id': 'UnrunnableBatch.SubB',
                                    'vows': ['testB_0'],
                                    'contexts': {
                                        'SubC': {
                                            'name': 'SubC',
                                            'id': 'UnrunnableBatch.SubB.SubC',
                                            'vows': ['testB1_0', 'testB1_1'],
                                            'contexts': {}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            expect(topic).to_equal(baseline)

    class WithExclusionPatternForContext(Vows.Context):
        def topic(self):
            planner = ExecutionPlanner(
                {'dummySuite': set([UnrunnableBatch])},
                set([r'S[bu]{2}B']),
                set([])
            )
            return planner.plan()

        def the_excluded_context_is_not_included(self, topic):
            baseline = {
                'dummySuite': {
                    'contexts': {
                        'UnrunnableBatch': {
                            'name': 'UnrunnableBatch',
                            'id': 'UnrunnableBatch',
                            'vows': [],
                            'contexts': {
                                'SubA': {
                                    'name': 'SubA',
                                    'id': 'UnrunnableBatch.SubA',
                                    'vows': [],
                                    'contexts': {}
                                }
                            }
                        }
                    }
                }
            }
            expect(topic).to_equal(baseline)

    class WithExclusionPatternForBatch(Vows.Context):
        def topic(self):
            planner = ExecutionPlanner(
                {'dummySuite': set([UnrunnableBatch])},
                set([r'UnrunnableBatch']),
                set([])
            )
            return planner.plan()

        def the_excluded_context_is_not_included(self, topic):
            baseline = {
                'dummySuite': {
                    'contexts': {}
                }
            }
            expect(topic).to_equal(baseline)

    class WithExclusionPatternForVow(Vows.Context):
        def topic(self):
            planner = ExecutionPlanner(
                {'dummySuite': set([UnrunnableBatch])},
                set([r'testB1.*']),
                set([])
            )
            return planner.plan()

        def the_excluded_context_is_not_included(self, topic):
            baseline = {
                'dummySuite': {
                    'contexts': {
                        'UnrunnableBatch': {
                            'name': 'UnrunnableBatch',
                            'id': 'UnrunnableBatch',
                            'vows': [],
                            'contexts': {
                                'SubA': {
                                    'name': 'SubA',
                                    'id': 'UnrunnableBatch.SubA',
                                    'vows': [],
                                    'contexts': {}
                                },
                                'SubB': {
                                    'name': 'SubB',
                                    'id': 'UnrunnableBatch.SubB',
                                    'vows': ['testB_0'],
                                    'contexts': {
                                        'SubC': {
                                            'name': 'SubC',
                                            'id': 'UnrunnableBatch.SubB.SubC',
                                            'vows': [],
                                            'contexts': {}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            expect(topic).to_equal(baseline)

    class WithBothInclusionAndExclusion(Vows.Context):
        @Vows.capture_error
        def topic(self):
            planner = ExecutionPlanner(
                {'dummySuite': set([UnrunnableBatch])},
                set([r'testB1.*']),
                set([r'asdf'])
            )
            return planner.plan()

        def exception_is_raised(self, topic):
            expect(topic).to_be_an_error()

    class WithInclusionPatternForOneContext(Vows.Context):
        def topic(self):
            planner = ExecutionPlanner(
                {'dummySuite': set([UnrunnableBatch, SomeLoneBatch])},
                set([]),
                set([r'SubB$'])
            )
            return planner.plan()

        def target_context_topic_and_ancestors_topics_are_included(self, topic):
            baseline = {
                'dummySuite': {
                    'contexts': {
                        'UnrunnableBatch': {
                            'name': 'UnrunnableBatch',
                            'id': 'UnrunnableBatch',
                            'vows': [],
                            'contexts': {
                                'SubB': {
                                    'name': 'SubB',
                                    'id': 'UnrunnableBatch.SubB',
                                    'vows': [],
                                    'contexts': {}
                                }
                            }
                        }
                    }
                }
            }
            expect(topic).to_equal(baseline)

    class WithInclusionPatternForOneVow(Vows.Context):
        def topic(self):
            planner = ExecutionPlanner(
                {'dummySuite': set([UnrunnableBatch, SomeLoneBatch])},
                set([]),
                set([r'testB1_0'])
            )
            return planner.plan()

        def the_only_the_targeted_vow_is_run_on_the_context(self, topic):
            baseline = {
                'dummySuite': {
                    'contexts': {
                        'UnrunnableBatch': {
                            'name': 'UnrunnableBatch',
                            'id': 'UnrunnableBatch',
                            'vows': [],
                            'contexts': {
                                'SubB': {
                                    'name': 'SubB',
                                    'id': 'UnrunnableBatch.SubB',
                                    'vows': [],
                                    'contexts': {
                                        'SubC': {
                                            'name': 'SubC',
                                            'id': 'UnrunnableBatch.SubB.SubC',
                                            'vows': ['testB1_0'],
                                            'contexts': {}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            expect(topic).to_equal(baseline)

    class WithInclusionPatternHittingOnlyOneBatch(Vows.Context):
        def topic(self):
            planner = ExecutionPlanner(
                {'dummySuite': set([UnrunnableBatch, SomeOtherBatch])},
                set([]),
                set([r'UnrunnableBatch'])
            )
            return planner.plan()

        def the_other_batch_is_not_included(self, topic):
            baseline = {
                'dummySuite': {
                    'contexts': {
                        'UnrunnableBatch': {
                            'name': 'UnrunnableBatch',
                            'id': 'UnrunnableBatch',
                            'vows': [],
                            'contexts': {
                                'SubA': {
                                    'name': 'SubA',
                                    'id': 'UnrunnableBatch.SubA',
                                    'vows': [],
                                    'contexts': {}
                                },
                                'SubB': {
                                    'name': 'SubB',
                                    'id': 'UnrunnableBatch.SubB',
                                    'vows': ['testB_0'],
                                    'contexts': {
                                        'SubC': {
                                            'name': 'SubC',
                                            'id': 'UnrunnableBatch.SubB.SubC',
                                            'vows': ['testB1_0', 'testB1_1'],
                                            'contexts': {}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            expect(topic).to_equal(baseline)


class UnrunnableBatch(Vows.Context):
    def topic(self):
        raise Exception('Never Run Me')

    class SubA(Vows.Context):
        pass

    class SubB(Vows.Context):
        def testB_0(self, topic):
            pass

        class SubC(Vows.Context):
            def testB1_0(self, topic):
                pass

            def testB1_1(self, topic):
                pass


class SomeOtherBatch(UnrunnableBatch):
    pass


class SomeLoneBatch(Vows.Context):
    pass
