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

from abc import ABC, abstractmethod
from typing import Optional, Any, MutableMapping, Dict, List


class Stringer(ABC):
    """
        Constant String Wrapper
        ~~~~~~~~~~~~~~~~~~~~~~~
    """

    def __hash__(self) -> int:
        return NotImplemented

    def __len__(self) -> int:
        return NotImplemented

    def __eq__(self, other) -> bool:
        return NotImplemented

    def __ne__(self, other) -> bool:
        return NotImplemented

    def __str__(self) -> str:
        return NotImplemented

    @property
    def string(self) -> str:
        """ get inner string """
        return NotImplemented


class Mapper(MutableMapping[str, Any], ABC):
    """
        Mutable Map Wrapper
        ~~~~~~~~~~~~~~~~~~~
    """

    @property
    def dictionary(self) -> Dict[str, Any]:
        """ get inner map """
        raise NotImplemented

    @abstractmethod
    def copy_dictionary(self, deep_copy: bool = False) -> Dict[str, Any]:
        """ copy inner map """
        raise NotImplemented


class Wrapper:

    @classmethod
    def get_string(cls, s) -> Optional[str]:
        """
            Get inner string
            ~~~~~~~~~~~~~~~~
        """
        if isinstance(s, Stringer):
            return s.string
        elif isinstance(s, str):
            return s

    @classmethod
    def get_dictionary(cls, d) -> Optional[Dict[str, Any]]:
        """
            Get inner map
            ~~~~~~~~~~~~~
            Remove first wrapper
        """
        if isinstance(d, Mapper):
            return d.dictionary
        elif isinstance(d, Dict):
            return d

    @classmethod
    def unwrap(cls, o) -> Any:
        """
            Unwrap object container
            ~~~~~~~~~~~~~~~~~~~~~~~
        """
        if isinstance(o, Stringer):
            return o.string
        elif isinstance(o, Mapper):
            return cls.unwrap_map(o.dictionary)
        elif isinstance(o, Dict):
            return cls.unwrap_map(o)
        elif isinstance(o, List):
            return cls.unwrap_list(o)
        return o

    @classmethod
    def unwrap_map(cls, d) -> Dict[str, Any]:
        """ Unwrap values for keys in map """
        if isinstance(d, Mapper):
            d = d.dictionary
        dictionary = {}
        for key in d:
            value = d[key]
            naked = cls.unwrap(value)
            dictionary[key] = naked
        return dictionary

    @classmethod
    def unwrap_list(cls, a) -> List[Any]:
        """ Unwrap values in the array """
        array = []
        for value in a:
            naked = cls.unwrap(value)
            array.append(naked)
        return array
