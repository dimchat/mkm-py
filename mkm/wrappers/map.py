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
from typing import Any, MutableMapping

from .string import String


class Wrapper:
    """
        Wrapper for dict, list, str
    """

    @classmethod
    def unwrap(cls, o: Any, circularly: bool = False) -> Any:
        # unwrap string
        if isinstance(o, String):
            return o.string
        if isinstance(o, str):
            return o
        # unwrap container
        if circularly:
            # unwrap map circularly
            if isinstance(o, Map):
                return Map.unwrap(o.dictionary, circularly=True)
            if isinstance(o, dict):
                return Map.unwrap(o, circularly=True)
            # unwrap list circularly
            if isinstance(o, Array):
                return Array.unwrap(o.array, circularly=True)
            if isinstance(o, list):
                return Array.unwrap(o, circularly=True)
        else:
            # unwrap map
            if isinstance(o, Map):
                return o.dictionary
            # unwrap list
            if isinstance(o, Array):
                return o.array
        # others
        return o


class Array(ABC):
    """
        List: Any
    """

    @classmethod
    def unwrap(cls, a: list, circularly: bool = False) -> list:
        # unwrap list container
        if isinstance(a, Array):
            a = a.array
        if not circularly:
            return a
        # unwrap items circularly
        t = []
        for o in a:
            item = Wrapper.unwrap(o, circularly=True)
            t.append(item)
        return t

    @property
    def array(self) -> list:
        raise NotImplemented

    @abstractmethod
    def copy_array(self, deep_copy: bool = False) -> list:
        raise NotImplemented


class Map(MutableMapping, ABC):
    """
        Mapping: str -> Any
    """

    @classmethod
    def unwrap(cls, d: dict, circularly: bool = False) -> dict:
        # unwrap map container
        if isinstance(d, Map):
            d = d.dictionary
        if not circularly:
            return d
        # unwrap keys, values circularly
        t = {}
        for k in d:
            v = d[k]
            key = String.unwrap(k)
            value = Wrapper.unwrap(v, circularly=True)
            t[key] = value
        return t

    @property
    def dictionary(self) -> dict:
        raise NotImplemented

    @abstractmethod
    def copy_dictionary(self, deep_copy: bool = False) -> dict:
        raise NotImplemented
