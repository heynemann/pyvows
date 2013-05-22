# Contributing to PyVows

If you want to contribute to pyvows, please verify your pull request with [flake8](http://pypi.python.org/pypi/flake8/) before sending it. It’s quite simple to use.

We’re only using one different setting from the default: instead of a maximum line length of 80, we’re using 130. 

Changing flake8 to respect this is as easy as:

    $ cat ~/.config/pep8

    [pep8]
    max-line-length = 130
