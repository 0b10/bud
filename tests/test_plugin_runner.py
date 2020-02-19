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

"""Tests for `bud.lib.pr_factory` package."""


import pytest
from bud.lib.plugin_loader import PluginLoader
from bud.lib.plugin_runner import PluginRunner
from unittest.mock import MagicMock, patch, call
from .fixtures import plugin_one, plugin_two


@pytest.fixture
def fake_plugins():
    def _(modules):
        # add custom modules, these are will should be mocked.
        # ! don't use this unless you are testing modules, otherwise you will be writing lots of mocks.
        plugins = {
            'fakename1': {'module_path': 'ignorethis.plugin_one', 'class_name': 'FakePluginOne'},
            'fakename2': {'module_path': 'ignorethis.plugin_two', 'class_name': 'FakePluginTwo'}
        }
        # add modules to dict
        for k, module in modules.items():
            plugins[k]['module'] = module
        return plugins
    yield _


@pytest.fixture
def pr_factory():
    def _(loader=MagicMock(spec_set=PluginLoader)):
        return {'runner': PluginRunner(loader=loader), 'loader': loader}
    return _


# >>> EXISTS >>>
def test_exists(pr_factory):
    runner = pr_factory()['runner']
    assert isinstance(runner, PluginRunner), \
        "PluginRunner does not exist"


def test_run_all(pr_factory):
    runner = pr_factory()['runner']
    assert callable(runner.run_all), \
        "PluginRunner.run_all does not exist"


def test_run_some(pr_factory):
    runner = pr_factory()['runner']
    assert callable(runner.run_all), \
        "PluginRunner.run_some does not exist"


@patch.object(plugin_two.FakePluginTwo, 'post')
@patch.object(plugin_one.FakePluginOne, 'post')
@patch.object(plugin_two.FakePluginTwo, 'build')
@patch.object(plugin_one.FakePluginOne, 'build')
@patch.object(plugin_two.FakePluginTwo, 'pre')
@patch.object(plugin_one.FakePluginOne, 'pre')
class TestWithPatchedPlugins:
    # >>> RUN_ALL >>>
    def test_call_run_all(
        self,
        mocked_p1_pre,
        mocked_p2_pre,
        mocked_p1_build,
        mocked_p2_build,
        mocked_p1_post,
        mocked_p2_post,
        pr_factory,
        fake_plugins
    ):
        fixture = pr_factory()
        loader = fixture['loader']
        runner = fixture['runner']

        loader.loaded = fake_plugins(
            {'fakename1': plugin_one, 'fakename2': plugin_two})

        runner.run_all()
        assert mocked_p1_pre.called
        assert mocked_p2_pre.called
        assert mocked_p1_build.called
        assert mocked_p2_build.called
        assert mocked_p1_post.called
        assert mocked_p2_post.called


    # >>> RUN_SOME >>>
    def test_call_run_some(
        self,
        mocked_p1_pre,
        mocked_p2_pre,
        mocked_p1_build,
        mocked_p2_build,
        mocked_p1_post,
        mocked_p2_post,
        pr_factory,
        fake_plugins
    ):
        fixture = pr_factory()
        loader = fixture['loader']
        runner = fixture['runner']

        loader.loaded = fake_plugins(
            {'fakename1': plugin_one, 'fakename2': plugin_two})

        runner.run_some(['fakename1', 'fakename2'])
        assert mocked_p1_pre.called
        assert mocked_p2_pre.called
        assert mocked_p1_build.called
        assert mocked_p2_build.called
        assert mocked_p1_post.called
        assert mocked_p2_post.called


    def test_call_run_some_name(
        self,
        mocked_p1_pre,
        mocked_p2_pre,
        mocked_p1_build,
        mocked_p2_build,
        mocked_p1_post,
        mocked_p2_post,
        pr_factory,
        fake_plugins
    ):
        fixture = pr_factory()
        loader = fixture['loader']
        runner = fixture['runner']

        loader.loaded = fake_plugins(
            {'fakename1': plugin_one, 'fakename2': plugin_two})

        runner.run_some(['fakename1', 'fakename2'])
        assert mocked_p1_pre.called
        assert mocked_p2_pre.called
        assert mocked_p1_build.called
        assert mocked_p2_build.called
        assert mocked_p1_post.called
        assert mocked_p2_post.called
