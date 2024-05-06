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
from abc import ABC
from typing import Any, Dict, List

from .wrapper import Mapper


class Copier(ABC):

    @classmethod
    def copy(cls, o: Any) -> Any:
        if o is None:
            return None
        elif isinstance(o, Mapper):
            return cls.copy_map(o.dictionary)
        elif isinstance(o, Dict):
            return cls.copy_map(o)
        elif isinstance(o, List):
            return cls.copy_list(o)
        else:
            return o

    @classmethod
    def copy_map(cls, d: Dict) -> Dict:
        return d.copy()

    @classmethod
    def copy_list(cls, a: List) -> List:
        return a.copy()

    #
    #   Deep Copy
    #

    @classmethod
    def deep_copy(cls, o: Any) -> Any:
        if o is None:
            return None
        elif isinstance(o, Mapper):
            return cls.deep_copy_map(o.dictionary)
        elif isinstance(o, Dict):
            return cls.deep_copy_map(o)
        elif isinstance(o, List):
            return cls.deep_copy_list(o)
        else:
            # return o
            return copy.deepcopy(o)

    @classmethod
    def deep_copy_map(cls, d: Dict) -> Dict:
        dictionary = {}
        for k in d:
            v = d[k]
            dictionary[k] = cls.deep_copy(v)
        return dictionary

    @classmethod
    def deep_copy_list(cls, a: List) -> List:
        array = []
        for item in a:
            array.append(cls.deep_copy(item))
        return array
