# Changelog

This file is an summary of major changes.  Check out [the commit history on GitHub](https://github.com/heynemann/pyvows/commits/master) 
if you need an exhaustive list of changes.


## 2.0.0 (2013-05-22)

* Numerous minor improvements:
 - code cleanup
 - added comments
 - reorganization
 - renamed variables, methods, etc. to better describe their purpose


### Features

* Close #86: New option (`--template`): generate new PyVows files
* Close #73: Vows filtering [nathan dotz]
  Exclude tests based on a string pattern


### Bugfixes

* Fix broken test `file_vows.py` 
* Fixed bug in `_get_topic_times()` 
* Fix #91: `ImportError` exception on Windows [Doug McCall]
  Module names were not being properly constructed on Windows; 
  code used the `/` character instead of `os.path.sep`
* Fixed build-breaking use of set comprehensions… 
  P.S.: Python 2.6 is dumb
* Fix #81, #48: Now catching internal errors when printing tracebacks  
* Fix #6, #78: from Zearin/bug/67_error_on_reorganizing_vows
* Fix #67: A simple `__init__.py` fixed things ;) 
* Fixed build error: `aptitude` → `apt-get` (for Travis) 
  Getting an "`aptitude not found`" error.  Odd…  Advised by support
  from Travis IRC channel to try `apt-get` instead
* `reporting.test`: commented out problematic `except:` block
* Fix #89: Handle generative topics like simple topics if they produce an exception [Telofy]
  If an exception occures in a topic, the value remains iterable since
  expections, somehow, are iterable. The result is that the entries
  (i.e. the error message string) are handed down to the vows where they
  cause strange errors that are hard to debug.  By resetting
  `is_generator` to False, these errors are handed to the vows unchanged,
  so that they can actually see the error type and topic.error.  Since
  most of my topics are not supposed to produce exceptions, it would be
  nice to have something like `Vows.NotErrorContext` that instead of just
  adding a vow, does not execute any vows in case of an error in the
  topic, and also prints a complete traceback of the error. The API
  might be a function decorator for `topic()` that sets a function
  attribute heeded by the runner


### Refactoring

* New modules:
  - `decorators`: now contains all decorators in PyVows
    Decorators existing elsewhere should import them from here
  - `errors`: now contains all custom errors in PyVows
  - `utils`: now contains all utility functions previously scattered throughout PyVows
* Moved `Vows.NotErrorContext` and `Vows.NotEmptyContext` to 
    `tests/assertions/assertion_vows.py` (The only place they were ever used…)
* `pyvows.console` → `pyvows.cli` 
      NEW!!! Module name now 57% shorter! ☺

#### Preggy
**Introducing…preggy!**

Preggy is an assertions library extracted from PyVows!  
Preggy now exists as a standalone project.
PyVows now lists preggy as a requirement.

* Removed:
  - `__init__`: Removed `import` for `VowsAssertionError` 
  - Removed `pyvows.assertions` 
  - Removed `_AssertionNotFoundError` class
    Functionality now covered by `preggy`
  - Removed `utils.VowsAssertion` class
    Functionality now covered by `preggy`
  - Replaced references to `expect`, `decorators._assertion`, and
    `decorators._create_assertions` to `preggy` counterparts
* Updated requirements in project metadata:
    - Makefile 
    - REQUIREMENTS 
    - setup.py 
    - test_requirements.txt 
    - tox.ini
* `tests.*`: Updated test string checking to match updated preggy


#### pyvows.runner

Although preggy was the focus of this release, we’ve also began 
a refactoring `pyvows.runner`.  Work is ongoing...

* Close #83: Semi-refactoring of `pyvows.runner` 
* Made `pool` a class-level attribute
* Extracted `VowsParallelRunner` methods to module functions (for now…) 
* Removed superfluous variable in `VowsParallelRunner.run()` 
* Organized code in `VowsParallelRunner.run_context_async()` 
* Runner: Predetermine vows & contexts
  - …only iterate over the vows or contexts (rather than over all context members, 
    testing whether each is a vow/subcontext) 
  - …iterate over sets, which (since they’re unordered) iterate much faster than lists
* Runner: determine excluded items *first* 
* Runner: Better variable names
* Runner: Precompile regexes. use `set`s (since we don’t care about the order of the patterns)
  
  
### Misc

Tons of tweaks, cleaning, and changes to make the source code more human-friendly

* `reporting.common`: better checking to format tracebacks
* `Vows` now tracks test files with `Vows.suites`

* Patch up missing flag [nathan dotz]
* Update tests to reflect upstream changes [nathan dotz]
* Add `prune` function (currently doesn’t do anything) [nathan dotz]
* Make the exclusions regex matches [nathan dotz]
* Update exclusion notes in help [nathan dotz]
* Make test for matching contexts a smidge nicer [nathan dotz]
* Rename to be appropriate to the feature under test [nathan dotz]
* Passing exclusion patterns to test runner [nathan dotz]

* Close #79: PEP8 compliance
* Bring `docstring_vows.py` up to date with refactorings
* Add tests to improve coverage
* `xunit.py`: Use `with...` to write report file
* Add message to `VowsInternalError` encouraging bug reports
* Add `#FIXME` for a needed comment
* Import `VowsInternalError` for problems at runtime
* Add `VowsInternalError` to `raise` for any illegal behavior internal to PyVows
* Removed redundant `FunctionWrapper` declaration
* Decoupled `result` and `reporter` in `pyvows.cli:run()` 
* Clean up call to `async_topic()` 
* Travis requirements
* Fix PEP8 issues
* Fix import in `__init__.py` 
* Underscore-prefixed `_get_topic_times()` in `VowsResult` 
* `Vows.ensure()` → `Vows.run()` 
* `Vows.gather()` → `Vows.collect()` 
* Moved pseudo-private methods to top (`VowsParallelRunner`) 
* Underscored internal methods in `VowsParallelRunner` 
* Tidied up `VowsTestReporter` printing
  This also required a few edits to the base class `VowsReporter`
  This, in turn, required a minor edit to a test
  (`tests/bugs/64_vows.py`).  (In the test, the lambdas arguments count
  must equal the corresponding methods in `VowsReporter`.)
* Don’t `pprint` results
* Expanded docstring of `VowsResult` 
* Move class-level attributes to top
* Close #72: `--long_cli_option` → `--long-cli-option` (underscores are annoying)
* Tidied profile results list code
* `README.mkd` → `README.md` 
* Replaced uses of `map()` with list comprehensions
* Minor improvements to `VowsReporter.print_traceback()` (in `reporting.common`) 
  - Renamed variables for readability
  - This method was manually indenting its output; changed to use the `indent_msg()` method