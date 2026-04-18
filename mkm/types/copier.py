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

import copy
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .wrapper import Mapper


######################
#                    #
#   Data Copier      #
#                    #
######################


class DataCopier(ABC):

    @abstractmethod
    def copy(self, o: Any) -> Any:
        raise NotImplemented

    @abstractmethod
    def copy_map(self, d: Dict) -> Dict:
        raise NotImplemented

    @abstractmethod
    def copy_list(self, a: List) -> List:
        raise NotImplemented

    @abstractmethod
    def deep_copy(self, o: Any) -> Any:
        raise NotImplemented

    @abstractmethod
    def deep_copy_map(self, d: Dict) -> Dict:
        raise NotImplemented

    @abstractmethod
    def deep_copy_list(self, a: List) -> List:
        raise NotImplemented


class BaseCopier(DataCopier):

    # Override
    def copy(self, o: Any) -> Any:
        if o is None:
            return None
        elif isinstance(o, Mapper):
            return self.copy_map(o.to_dict())
        elif isinstance(o, Dict):
            return self.copy_map(o)
        elif isinstance(o, List):
            return self.copy_list(o)
        else:
            return o

    # Override
    def copy_map(self, d: Dict) -> Dict:
        return d.copy()

    # Override
    def copy_list(self, a: List) -> List:
        return a.copy()

    # Override
    def deep_copy(self, o: Any) -> Any:
        if o is None:
            return None
        elif isinstance(o, Mapper):
            return self.deep_copy_map(o.to_dict())
        elif isinstance(o, Dict):
            return self.deep_copy_map(o)
        elif isinstance(o, List):
            return self.deep_copy_list(o)
        else:
            # return o
            return copy.deepcopy(o)

    # Override
    def deep_copy_map(self, d: Dict) -> Dict:
        dictionary = {}
        for k in d:
            v = d[k]
            dictionary[k] = self.deep_copy(v)
        return dictionary

    # Override
    def deep_copy_list(self, a: List) -> List:
        array = []
        for item in a:
            array.append(self.deep_copy(item))
        return array


class Copier(ABC):

    # Singleton
    copier: DataCopier = BaseCopier()

    #
    #   Shallow Copy
    #

    @classmethod
    def copy(cls, o: Any) -> Any:
        return cls.copier.copy(o)

    @classmethod
    def copy_map(cls, d: Dict) -> Dict:
        return cls.copier.copy_map(d)

    @classmethod
    def copy_list(cls, a: List) -> List:
        return cls.copier.copy_list(a)

    #
    #   Deep Copy
    #

    @classmethod
    def deep_copy(cls, o: Any) -> Any:
        return cls.copier.deep_copy(o)

    @classmethod
    def deep_copy_map(cls, d: Dict) -> Dict:
        return cls.copier.deep_copy_map(d)

    @classmethod
    def deep_copy_list(cls, a: List) -> List:
        return cls.copier.deep_copy_list(a)
