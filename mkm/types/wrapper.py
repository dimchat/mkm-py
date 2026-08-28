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
from collections.abc import Mapping, MutableMapping
from typing import Optional, Any

from .x import final
from .x import MutableStrMap
from .x import AnyList

from .mapper import Mapper
from .stringer import Stringer


######################
#                    #
#   Data Wrapper     #
#                    #
######################


class DataWrapper(ABC):

    @abstractmethod
    def get_str(self, s) -> Optional[str]:
        """ Shallow unwrap string value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_str()'
        )

    @abstractmethod
    def get_map(self, d) -> Optional[MutableStrMap]:
        """ Shallow unwrap dict value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_map()'
        )

    @abstractmethod
    def unwrap(self, o) -> Any:
        """ Deep unwrap value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.unwrap()'
        )

    @abstractmethod
    def unwrap_map(self, d) -> Optional[MutableStrMap]:
        """ Deep unwrap dict value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.unwrap_map()'
        )

    @abstractmethod
    def unwrap_list(self, a) -> Optional[AnyList]:
        """ Deep unwrap List value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.unwrap_list()'
        )


class BaseWrapper(DataWrapper):

    # Override
    def get_str(self, s) -> Optional[str]:
        if s is None:
            return None
        elif isinstance(s, Stringer):
            return s.to_str()
        elif isinstance(s, str):
            return s
        else:
            # assert False, f'string error: {s}'
            return str(s)

    # Override
    def get_map(self, d) -> Optional[MutableStrMap]:
        if d is None:
            return None
        elif isinstance(d, Mapper):
            return d.to_map()
        elif isinstance(d, MutableMapping):
            return d
        else:
            assert isinstance(d, Mapping), f'map error: {d}'
            return dict(d)

    # Override
    def unwrap(self, o) -> Any:
        if o is None:
            return None
        elif isinstance(o, Mapper):
            return self.unwrap_map(o.to_map())
        elif isinstance(o, Mapping):
            return self.unwrap_map(o)
        elif isinstance(o, list):
            return self.unwrap_list(o)
        elif isinstance(o, Stringer):
            return o.to_str()
        else:
            return o

    # Override
    def unwrap_map(self, d) -> Optional[MutableStrMap]:
        if d is None:
            return None
        elif isinstance(d, Mapper):
            d = d.to_map()
        # dictionary = {}
        # for key, value in d.items():
        #     naked = self.unwrap(value)
        #     dictionary[key] = naked
        # return dictionary
        return {key: self.unwrap(value) for key, value in d.items()}

    # Override
    def unwrap_list(self, a) -> Optional[AnyList]:
        if a is None:
            return None
        # array = []
        # for item in a:
        #     naked = self.unwrap(item)
        #     array.append(naked)
        # return array
        return [self.unwrap(item) for item in a]


@final
class Wrapper:

    # Singleton
    wrapper: DataWrapper = BaseWrapper()

    @classmethod
    def get_str(cls, s) -> Optional[str]:
        """
            Get inner string
            ~~~~~~~~~~~~~~~~
        """
        return cls.wrapper.get_str(s)

    @classmethod
    def get_map(cls, d) -> Optional[MutableStrMap]:
        """
            Get inner map
            ~~~~~~~~~~~~~
            Remove first wrapper
        """
        return cls.wrapper.get_map(d)

    @classmethod
    def unwrap(cls, o) -> Any:
        """
            Unwrap object container
            ~~~~~~~~~~~~~~~~~~~~~~~
        """
        return cls.wrapper.unwrap(o)

    @classmethod
    def unwrap_map(cls, d) -> Optional[MutableStrMap]:
        """ Unwrap values for keys in map """
        return cls.wrapper.unwrap_map(d)

    @classmethod
    def unwrap_list(cls, a) -> Optional[AnyList]:
        """ Unwrap values in the array """
        return cls.wrapper.unwrap_list(a)
