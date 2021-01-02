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
from typing import Optional, MutableMapping, Iterator, ItemsView, KeysView, ValuesView, Any


class SOMap(MutableMapping):
    """
        Mapping: str -> Any
    """

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
        elif isinstance(dictionary, Dictionary):
            self.__dictionary = dictionary.dictionary
        else:
            assert isinstance(dictionary, dict), 'dictionary error: %s' % dictionary
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
        self.__dictionary[str(key)] = value

    def __getitem__(self, key):
        return self.__dictionary[str(key)]

    def __delitem__(self, key) -> None:
        del self.__dictionary[str(key)]

    def __contains__(self, item):
        return str(item) in self.__dictionary

    def __eq__(self, other):
        if isinstance(other, SOMap):
            other = other.dictionary
        return self.__dictionary == other

    def __ne__(self, other):
        if isinstance(other, SOMap):
            other = other.dictionary
        return self.__dictionary != other

    def get(self, key) -> Optional[Any]:
        return self.__dictionary.get(str(key))

    def pop(self, key, default=None) -> Optional[Any]:
        return self.__dictionary.pop(str(key), default)

    def items(self) -> ItemsView[str, Any]:
        return self.__dictionary.items()

    def keys(self) -> KeysView[str]:
        return self.__dictionary.keys()

    def values(self) -> ValuesView[Any]:
        return self.__dictionary.values()

    def clear(self):
        self.__dictionary.clear()


class String:
    """
        A container with inner string
    """

    def __init__(self, string: Optional[str]=None):
        super().__init__()
        if string is None:
            self.__string = ''
        else:
            self.__string = string

    @property
    def string(self) -> str:
        return self.__string

    def __str__(self):
        return self.__string

    def __len__(self):
        return len(self.__string)

    def __hash__(self):
        return hash(self.__string)

    def __iter__(self):
        return iter(self.__string)

    def __add__(self, other):
        string = self.__string + str(other)
        return String(string=string)

    def __eq__(self, other):
        return self.__string == str(other)

    def __ne__(self, other):
        return self.__string != str(other)

    def __contains__(self, item):
        return str(item) in self.__string

    def __getitem__(self, item):
        return self.__string[item]

    def count(self, sub, start=None, end=None) -> int:
        return self.__string.count(str(sub), start, end)

    def startswith(self, prefix, start=None, end=None) -> bool:
        return self.__string.startswith(prefix=str(prefix), start=start, end=end)

    def endswith(self, suffix, start=None, end=None) -> bool:
        return self.__string.endswith(suffix=str(suffix), start=start, end=end)

    def find(self, sub, start=None, end=None) -> int:
        return self.__string.find(str(sub), start, end)

    def rfind(self, sub, start=None, end=None) -> int:
        return self.__string.rfind(str(sub), start, end)

    def index(self, sub, start=None, end=None) -> int:
        return self.__string.index(str(sub), start, end)

    def rindex(self, sub, start=None, end=None) -> int:
        return self.__string.rindex(str(sub), start, end)

    def strip(self, chars: Optional[str]=None):
        string = self.__string.strip(chars=chars)
        return String(string=string)

    def lstrip(self, chars: Optional[str]=None):
        string = self.__string.lstrip(chars=chars)
        return String(string=string)

    def rstrip(self, chars: Optional[str]=None):
        string = self.__string.rstrip(chars=chars)
        return String(string=string)

    def lower(self):
        string = self.__string.lower()
        return String(string=string)

    def upper(self):
        string = self.__string.upper()
        return String(string=string)
