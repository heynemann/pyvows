# Contributing to PyVows

If you want to contribute to pyvows, we’d love the help!  

To make the process go smoother, please check your changes with 
[`flake8`] before submitting your Pull Request.  
(Don’t worry--`flake8` is simple to use.)

We’re only using one different setting from the default; 
instead of the default maximum line length of 80, we’re using 130.

Changing `flake8` to respect this is as easy as:

    $ cat ~/.config/pep8

    [pep8]
    max-line-length = 130

[flake8]: http://pypi.python.org/pypi/flake8/


## Useful Tools

* **General:**
  * **[git-hooks]**: Easily control hooks for git actions, at the system-, user-, and project-levels.
  * **[travis]**: A command-line tool for interacting with the Travis-CI service.

* **Python:**
  * **[pylint]**: Code quality checks. Better than `pep8`.  Better than `flake8`.  (Yeah…I said it.)
  * **[pyenv]**:  Manage multiple versions of Python with ease.
  * **[tox]**:    Tests code with multiple versions of Python.


[git-hooks]: https://github.com/icefox/git-hooks
[travis]: https://github.com/travis-ci/travis.rb

[pylint]: http://www.pylint.org
[pyenv]:  https://github.com/yyuu/pyenv
[tox]:    http://tox.readthedocs.org/en/latest/
