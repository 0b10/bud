#!/usr/bin/env python
# MIT License

# Copyright (c) 2020, 0b10

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Tests for `bud.lib.plugin` package."""


import pytest
from bud.lib.plugin import Plugin


@pytest.fixture
def plugin():
    def _():
        return Plugin()
    yield _


# >>> EXISTS >>>
def test_exists(plugin):
    assert isinstance(plugin(), Plugin), \
        'Plugin does not exist'


@pytest.mark.parametrize('method_name', ['pre', 'build', 'post'])
def test_methods_exist(plugin, method_name):
    pl = plugin()
    assert callable(getattr(pl, method_name)), \
        f'Plugin.{method_name}() does not exist or isn\'t callable'

# >>> RETURN VALUE >>>
@pytest.mark.parametrize('method_name', ['pre', 'build', 'post'])
def test_default_return_values(plugin, method_name):
    pl = plugin()
    assert getattr(pl, method_name)() is False, \
        f'Plugin.{method_name}() should return False by default'
