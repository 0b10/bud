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

"""Tests for `bud.lib.config` package."""


import pytest
from bud.lib.config import Config
from bud.lib.globals import REPOS_ENV_VAR
from unittest.mock import patch
import os
import json

FAKE_PLUGINS = [
    {'name': 'fakename1', 'path': '/fake/path1'},
    {'name': 'fakename2', 'path': '/fake/path2'}
]

FAKE_FILE_CONTENTS = json.dumps(
    {'plugins': FAKE_PLUGINS}
)


class FakeFile:
    # FIXME: make this the source of truth - make it convert result to dict
    def __init__(self):
        self.contents = FAKE_FILE_CONTENTS


@pytest.fixture
def config_factory(monkeypatch):
    with patch('bud.lib.config.isdir', return_value=True):  # patch assertion
        def _(file=FakeFile()):
            return Config(file=file)
        yield _
    # must be removed manually
    monkeypatch.delenv(REPOS_ENV_VAR, raising=False)


# >>> EXISTS >>>
def test_exists(config_factory):
    assert config_factory() is not None, \
        "Config does not exist"


# >>> PROPS >>>
def test_repos_prop(config_factory, monkeypatch):
    monkeypatch.setenv(REPOS_ENV_VAR, '/fake/path')
    assert config_factory().repos == '/fake/path', \
        "Config.repos mismatch"


def test_plugins_prop(config_factory, monkeypatch):
    _plugins = config_factory().plugins
    assert _plugins is not None, \
        "Config.plugins should be a list"
    assert _plugins == FAKE_PLUGINS, \
        "Config.plugins should equal an expected value"


# >>> CONSTRUCTOR >>>
def test_file_obj_constructor_var(config_factory):
    assert config_factory().file is not None, \
        'the file prop should be set'


# >>> ERROR >>>
def test_repos_prop_raises_when_not_set(config_factory, monkeypatch):
    # raises when KeyError - so delete
    monkeypatch.delenv(REPOS_ENV_VAR, raising=False)
    with pytest.raises(EnvironmentError):
        config_factory().repos


# >>> SINGLETON >>>
def test_is_singleton(config_factory):
    file = FakeFile()
    one = config_factory()
    two = config_factory(file=file)

    assert one.file is two.file, \
        'the file props should be the same object'
