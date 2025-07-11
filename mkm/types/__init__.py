# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from .converter import Converter, DataConverter, BaseConverter

from .copier import Copier
from .wrapper import Wrapper, Stringer, Mapper
from .string import ConstantString, String
from .dictionary import Dictionary

from .x import URI, DateTime


class Singleton(object):

    __instances = {}

    def __init__(self, cls):
        self.__cls = cls

    def __call__(self, *args, **kwargs):
        cls = self.__cls
        instance = self.__instances.get(cls, None)
        if instance is None:
            instance = cls(*args, **kwargs)
            self.__instances[cls] = instance
        return instance

    def __getattr__(self, key):
        return getattr(self.__cls, key, None)


__all__ = [

    'Singleton',

    'URI', 'DateTime',

    'Converter', 'DataConverter', 'BaseConverter',

    'Copier',
    'Wrapper', 'Stringer', 'Mapper',
    'ConstantString',  # 'String',
    'Dictionary',

]
