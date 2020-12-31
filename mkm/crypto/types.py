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

import copy
from abc import abstractmethod
from typing import MutableMapping, Iterator, Optional


class SOMap(MutableMapping):

    @property
    @abstractmethod
    def dictionary(self) -> dict:
        raise NotImplemented

    @abstractmethod
    def copy_dictionary(self, deep_copy: bool = False) -> dict:
        raise NotImplemented


class Dictionary(SOMap):
    """
        A container sharing the same inner dictionary
    """

    def __init__(self, dictionary: Optional[dict]=None):
        super().__init__()
        if dictionary is None:
            self.__dictionary = {}
        else:
            self.__dictionary = dictionary

    @property
    def dictionary(self) -> dict:
        return self.__dictionary

    def copy_dictionary(self, deep_copy: bool=False) -> dict:
        if deep_copy:
            copy.deepcopy(self.__dictionary)
        else:
            return self.__dictionary.copy()

    def __iter__(self) -> Iterator:
        return iter(self.__dictionary)

    def __len__(self) -> int:
        return len(self.__dictionary)

    def __setitem__(self, key, value):
        self.__dictionary[key] = value

    def __getitem__(self, key):
        return self.__dictionary[key]

    def __delitem__(self, key) -> None:
        del self.__dictionary[key]

    def get(self, key):
        return self.__dictionary.get(key)

    def pop(self, key, default=None):
        return self.__dictionary.pop(key, default)
