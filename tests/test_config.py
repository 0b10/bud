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


@pytest.fixture
def config(monkeypatch):
    with patch('bud.lib.config.isdir', return_value=True):  # patch assertion
        yield Config()
    # must be removed manually
    monkeypatch.delenv(REPOS_ENV_VAR, raising=False)


# >>> EXISTS >>>
def test_exists(config):
    assert config is not None, \
        "Config does not exist"


# >>> PROPS >>>
def test_repos_prop(config, monkeypatch):
    monkeypatch.setenv(REPOS_ENV_VAR, '/fake/path')
    assert config.repos == '/fake/path', \
        "Config.repos mismatch"


# >>> ERROR >>>
def test_repos_prop_raises_when_not_set(config, monkeypatch):
    # raises when KeyError - so delete
    monkeypatch.delenv(REPOS_ENV_VAR, raising=False)
    with pytest.raises(EnvironmentError):
        config.repos
