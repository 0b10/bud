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
from os import environ
from os.path import isdir
from bud.lib.globals import REPOS_ENV_VAR
from bud.lib.common import SingletonMeta
from abc import ABC, abstractmethod, ABCMeta
from json import loads


class ConfigAbstract(ABC):
    @property
    @abstractmethod
    def plugins(self):
        raise NotImplementedError('You must override the plugins property')

    @property
    @abstractmethod
    def repos(self):
        raise NotImplementedError('You must override the repos property')


class ConfigMeta(ABCMeta, SingletonMeta):
    pass

# Config = ConfigMeta('Config', (ConfigAbstract), {plugins:.., repos:..})


class Config(ConfigAbstract, metaclass=ConfigMeta):
    def __init__(self, file):
        self.file = file
        self._contents = loads(self.file.contents)

    @property
    def plugins(self):
        return self._contents.get('plugins', [])

    @property
    def repos(self):
        try:
            repos_path = environ[REPOS_ENV_VAR]
        except KeyError:
            raise EnvironmentError(f'You must set the {REPOS_ENV_VAR} env var')

        assert isdir(repos_path), \
            f'The env var: {REPOS_ENV_VAR}={repos_path} - should point to a directory.'
        return repos_path
