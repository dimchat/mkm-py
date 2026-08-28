# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2024 Albert Moky
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
from collections.abc import Mapping
from typing import Any

from .x import final
from .x import StrMap, MutableStrMap
from .x import AnyList

from .mapper import Mapper


######################
#                    #
#   Data Copier      #
#                    #
######################


class DataCopier(ABC):

    @abstractmethod
    def copy(self, o: Any) -> Any:
        """ Shallow copy any object """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.copy()'
        )

    @abstractmethod
    def copy_map(self, d: StrMap) -> MutableStrMap:
        """ Shallow copy the map """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.copy_map()'
        )

    @abstractmethod
    def copy_list(self, a: AnyList) -> AnyList:
        """ Shallow copy the list """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.copy_list()'
        )

    @abstractmethod
    def deep_copy(self, o: Any) -> Any:
        """ Deep copy any object """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.deep_copy()'
        )

    @abstractmethod
    def deep_copy_map(self, d: StrMap) -> MutableStrMap:
        """ Deep copy the map """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.deep_copy_map()'
        )

    @abstractmethod
    def deep_copy_list(self, a: AnyList) -> AnyList:
        """ Deep copy the list """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.deep_copy_list()'
        )


class BaseCopier(DataCopier):

    # Override
    def copy(self, o: Any) -> Any:
        if o is None:
            return None
        elif isinstance(o, Mapper):
            return self.copy_map(o.to_map())
        elif isinstance(o, Mapping):
            return self.copy_map(o)
        elif isinstance(o, list):
            return self.copy_list(o)
        else:
            return o

    # Override
    def copy_map(self, d: StrMap) -> MutableStrMap:
        # return d.copy()
        return dict(d)

    # Override
    def copy_list(self, a: AnyList) -> AnyList:
        return a.copy()

    # Override
    def deep_copy(self, o: Any) -> Any:
        if o is None:
            return None
        elif isinstance(o, Mapper):
            return self.deep_copy_map(o.to_map())
        elif isinstance(o, Mapping):
            return self.deep_copy_map(o)
        elif isinstance(o, list):
            return self.deep_copy_list(o)
        else:
            return o
            # return copy.deepcopy(o)

    # Override
    def deep_copy_map(self, d: StrMap) -> MutableStrMap:
        # dictionary = {}
        # for key, value in d.items():
        #     clone = self.deep_copy(value)
        #     dictionary[key] = clone
        # return dictionary
        return {key: self.deep_copy(value) for key, value in d.items()}

    # Override
    def deep_copy_list(self, a: AnyList) -> AnyList:
        # array = []
        # for item in a:
        #     clone = self.deep_copy(item)
        #     array.append(clone)
        # return array
        return [self.deep_copy_list(item) for item in a]


@final
class Copier:

    # Singleton
    copier: DataCopier = BaseCopier()

    #
    #   Shallow Copy
    #

    @classmethod
    def copy(cls, o: Any) -> Any:
        return cls.copier.copy(o)

    @classmethod
    def copy_map(cls, d: StrMap) -> MutableStrMap:
        return cls.copier.copy_map(d)

    @classmethod
    def copy_list(cls, a: AnyList) -> AnyList:
        return cls.copier.copy_list(a)

    #
    #   Deep Copy
    #

    @classmethod
    def deep_copy(cls, o: Any) -> Any:
        return cls.copier.deep_copy(o)

    @classmethod
    def deep_copy_map(cls, d: StrMap) -> MutableStrMap:
        return cls.copier.deep_copy_map(d)

    @classmethod
    def deep_copy_list(cls, a: AnyList) -> AnyList:
        return cls.copier.deep_copy_list(a)
