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

"""Tests for `bud.lib.common` package."""

import pytest
from bud.lib.common import SingletonMeta


class FakeClass(metaclass=SingletonMeta):
    def __init__(self, canary):
        self.canary = canary


@pytest.fixture
def class_factory():
    def _(canary=False):
        return FakeClass(canary=canary)
    yield _


def test_singleton_fixture_exists(class_factory):
    assert isinstance(class_factory(), FakeClass), \
        "FakeClass cannot be instantiated"


def test_singleton(class_factory):
    one = class_factory()
    two = class_factory()

    one.canary = True  # two.canary would still be False if not a singleton

    assert one.canary == two.canary, \
        "Singleton class: FakeClass - canary props should match," +\
        "because they should be the same object"
