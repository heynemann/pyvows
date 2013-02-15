[![Build Status](https://secure.travis-ci.org/heynemann/pyvows.png?branch=master)](http://travis-ci.org/heynemann/pyvows)

pyVows is the python version of the [Vows.JS](http://vowsjs.org) testing framework.

For more info go to [pyVows website](http://heynemann.github.com/pyvows/).

If you are using tornado you are VERY advised to check the Tornado_pyVows project by Rafael Carício at https://github.com/rafaelcaricio/tornado_pyvows

# WARNING

If you want to contribute to pyvows, please verify your pull request with [flake8](http://pypi.python.org/pypi/flake8/) before sending it. It is very simple to use.

We are using only one different setting from the default. Instead of 80 columns we are using 130 columns of width. Changing flake8 to respect that is as easy as:

    $ cat ~/.config/pep8

    [pep8]
    max-line-length = 130
