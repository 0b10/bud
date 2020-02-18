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
from unittest.mock import patch, call

FAKE_PLUGINS = [
    { 'module_path': 'plugins.plugin_one', 'class_name': 'FakePluginOne' },
    { 'module_path': 'plugins.plugin_two', 'class_name': 'FakePluginTwo' }
]

class FakeConfig(ConfigAbstract):
    def __init__(self, plugins):
        self._repos = '/fake/repos'
        self._plugins = plugins

    @property
    def plugins(self):
        return self._plugins

    @property
    def repos(self):
        # because it's abstract, it must be a getter
        return self._repos


@pytest.fixture
def pl_factory(fake_config_factory):
    def _(config=fake_config_factory()):
        return PluginLoader(config=config)
    return _


@pytest.fixture
def fake_config_factory():
    def _(plugins=FAKE_PLUGINS):
        return FakeConfig(plugins=plugins)
    yield _


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


# >>> LOAD >>>
def test_module_loader_is_called(pl_factory):
    with patch('bud.lib.plugin_loader.import_module') as mock_import:
        pl_factory().load()
        assert mock_import.called, \
            'The module loader was not called'

        call_one = FAKE_PLUGINS[0]['module_path']
        call_two = FAKE_PLUGINS[1]['module_path']

        expected_calls = [call(call_one), call(call_two)]
        mock_import.assert_has_calls(expected_calls)

def test_loader_associates_module_correctly(pl_factory):
    with patch('bud.lib.plugin_loader.import_module', return_value='placeholder_module_name') as mock_import:
        plugin_loader = pl_factory()
        plugin_loader.load()
        assert isinstance(plugin_loader.loaded, list) and len(plugin_loader.loaded) == len(FAKE_PLUGINS), \
            'The loaded prop should be a non-empty list'

        for plugin in zip(plugin_loader.loaded, FAKE_PLUGINS):
            assert plugin[0]['module_path'] == plugin[1]['module_path']
            assert plugin[0]['class_name'] == plugin[1]['class_name']
            assert plugin[0]['module'] == 'placeholder_module_name'
