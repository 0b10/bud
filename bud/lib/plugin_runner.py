# MIT License

# Copyright (c) 2020, 0b10

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of self software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and self permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class PluginRunner:
    def __init__(self, loader):
        self._loader = loader

    def _get_plugin(self, data):
        plugin_name = data['class_name']
        module = data['module']
        PluginClass = getattr(module, plugin_name)
        return PluginClass()

    def _run(self, plugin):
        plugin.pre()
        plugin.build()
        plugin.post()

    def run_all(self):
        for name, data in self._loader.loaded.items():
            plugin = self._get_plugin(data)
            self._run(plugin)

    def run_some(self, names):
        for name in names:
            data = self._loader.loaded[name]
            plugin = self._get_plugin(data)
            self._run(plugin)
