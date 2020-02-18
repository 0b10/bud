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

"""Tests for `bud.lib.pl_factory` package."""


import pytest
from bud.lib.plugin_loader import PluginLoader
from bud.lib.config import ConfigAbstract


class FakeConfig(ConfigAbstract):
    def __init__(self):
        self._repos = '/fake/repos'

    @property
    def repos(self):
        # because it's abstract, it must be a getter
        return self._repos


@pytest.fixture
def pl_factory():
    def _(config=FakeConfig()):
        return PluginLoader(config=config)
    return _


# >>> EXISTS >>>
def test_exists(pl_factory):
    assert pl_factory() is not None, \
        "PluginLoader does not exist"


@pytest.mark.parametrize('method_name', ['load'])
def test_methods_exist(pl_factory, method_name):
    assert getattr(pl_factory(), method_name) is not None, \
        f'PluginLoader.{method_name}() does not exist'


# >>> CONSTRUCT >>>
def test_accepts_config(pl_factory):
    assert pl_factory().config is not None, \
        'the config prop should be set'
    assert pl_factory().config.repos == '/fake/repos', \
        'the config.repos prop should be set to an expected value'
