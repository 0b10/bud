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

import pytest
from bud.lib.file import File


@pytest.fixture
def file_factory(tmp_path):
    config_path = tmp_path / "bud.conf"

    def _(path=config_path):
        return {'file': File(path=path), 'path': str(path), 'tmp_path': tmp_path}
    return _


# >>> EXISTS >>>
def test_exists(file_factory):
    file = file_factory()['file']
    assert isinstance(file, File), \
        "File was not instantiated"


def test_read_exists(file_factory):
    file = file_factory()['file']
    assert callable(file.read), \
        "File.read doesn't exist, or isn't callable"


# >>> READ >>>
def test_call_read(file_factory):
    fixture = file_factory()
    file = fixture['file']
    path = fixture['path']

    with open(path, 'w') as f:
        f.write('fake contents\ntest')

    assert file.read() == 'fake contents\ntest', \
        "File.read return an expected value"
