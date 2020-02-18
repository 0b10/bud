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

"""Tests for `bug.lib.console_message` package."""


import pytest
from unittest.mock import patch, call

from bud.lib.console_message import ConsoleMessage


@pytest.fixture
def console_message():
    return ConsoleMessage()

# >>> EXISTS >>>


def test_exists(console_message):
    assert console_message is not None, "ConsoleMessage does not exist"


def test_info_method_exists(console_message):
    assert console_message.info is not None, "ConsoleMessage.info() does not exist"


def test_error_method_exists(console_message):
    assert console_message.error is not None, "ConsoleMessage.error() does not exist"


def test_header_method_exists(console_message):
    assert console_message.header is not None, "ConsoleMessage.header() does not exist"

# >>> PRINTS >>>


def test_header_prints_a_message(console_message):
    with patch('builtins.print') as mocked_print:
        console_message.header("Test header message")
        assert mocked_print.mock_calls == [call(">>> Test header message")], \
            "ConsoleMessage.header does not print a message"


def test_info_prints_a_message(console_message):
    with patch('builtins.print') as mocked_print:
        console_message.info("Test info message")
        # +<1 space>Test info message
        assert mocked_print.mock_calls == [call("\t+  Test info message")], \
            "ConsoleMessage.info does not print a message"


def test_error_prints_a_message(console_message):
    with patch('builtins.print') as mocked_print:
        console_message.error("Test error message")
        # !!<2 spaces>Test error message
        assert mocked_print.mock_calls == [call("\t!! Test error message")], \
            "ConsoleMessage.error does not print a message"
