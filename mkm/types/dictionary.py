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

from typing import Optional, Union
from typing import Any, Tuple
from typing import Iterable, Iterator
from typing import AbstractSet, ValuesView

from .x import DateTime
from .x import Mapping, MutableMapping
from .x import StrMap, MutableStrMap

from .string import Stringer
from .converter import Converter
from .copier import Copier
from .wrapper import Mapper


class Dictionary(Mapper):
    """
        Mutable Map Wrapper
        ~~~~~~~~~~~~~~~~~~~
        A container sharing the same inner dictionary
    """

    def __init__(self, dictionary: Optional[StrMap] = None):
        super().__init__()
        if dictionary is None:
            dictionary = {}
        elif isinstance(dictionary, Mapper):
            dictionary = dictionary.to_map()
        elif not isinstance(dictionary, MutableMapping):
            assert isinstance(dictionary, Mapping), f'map value error: {dictionary}'
            dictionary = Copier.copy_map(dictionary)
        self.__dictionary: MutableStrMap = dictionary

    def __eq__(self, o: StrMap) -> bool:
        """ Return self==value. """
        if isinstance(o, Mapper):
            if self is o:
                # same object
                return True
            o = o.to_map()
        # check inner map
        return self.__dictionary.__eq__(o)

    def __ne__(self, o: StrMap) -> bool:
        """ Return self!=value. """
        if isinstance(o, Mapper):
            if self is o:
                # same object
                return False
            o = o.to_map()
        # check inner map
        return self.__dictionary.__ne__(o)

    def __repr__(self) -> str:
        """ Return repr(self). """
        return self.__dictionary.__repr__()

    def __str__(self) -> str:
        """ Return str(self). """
        return self.__dictionary.__str__()

    def __sizeof__(self) -> int:
        """ D.__sizeof__() -> size of D in memory, in bytes """
        return self.__dictionary.__sizeof__()

    def __len__(self) -> int:
        """ Return len(self). """
        return self.__dictionary.__len__()

    #
    #   Hashable
    #

    # Override
    def __hash__(self) -> int:
        """ Implement hash(self). """
        return self.__dictionary.__hash__()

    #
    #   Iterable
    #

    # Override
    def __iter__(self) -> Iterator[str]:
        """ Implement iter(self). """
        return self.__dictionary.__iter__()

    #
    #   Mapping
    #

    # Override
    def __getitem__(self, k: str) -> Any:
        """ x.__getitem__(y) <==> x[y] """
        return self.__dictionary.__getitem__(k)

    # Override
    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """ Return the value for key if key is in the dictionary, else default. """
        return self.__dictionary.get(key, default)

    # Override
    def items(self) -> AbstractSet[Tuple[str, Any]]:
        """ D.items() -> a set-like object providing a view on D's items """
        return self.__dictionary.items()

    # Override
    def keys(self) -> AbstractSet[str]:
        """ D.keys() -> a set-like object providing a view on D's keys """
        return self.__dictionary.keys()

    # Override
    def values(self) -> ValuesView[Any]:
        """ D.values() -> an object providing a view on D's values """
        return self.__dictionary.values()

    # Override
    def __contains__(self, o: object) -> bool:
        """ True if the dictionary has the specified key, else False. """
        return self.__dictionary.__contains__(o)

    #
    #   MutableMapping
    #

    # Override
    def __setitem__(self, k: str, v: Optional[Any]):
        """ Set self[key] to value. """
        self.__dictionary.__setitem__(k, v)

    # Override
    def __delitem__(self, v: Any):
        """ Delete self[key]. """
        self.__dictionary.__delitem__(v)

    # Override
    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        self.__dictionary.clear()

    # Override
    def pop(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        return self.__dictionary.pop(key, default)

    # Override
    def popitem(self) -> Tuple[str, Any]:
        """
        D.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if D is empty.
        """
        return self.__dictionary.popitem()

    # Override
    def setdefault(self, key: str, default: Any = None) -> Any:
        """
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        """
        self.__dictionary.setdefault(key, default)

    # Override
    def update(self, __m: Union[StrMap, Iterable[Tuple[str, Any]]], **kwargs: Any):
        """
        D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]
        """
        self.__dictionary.update(__m, **kwargs)

    #
    #   Mapper
    #

    # Override
    def get_str(self, key: str, default: Optional[str] = None) -> Optional[str]:
        value = self.__dictionary.get(key)
        return Converter.get_str(value=value, default=default)

    # Override
    def get_bool(self, key: str, default: Optional[bool] = None) -> Optional[bool]:
        value = self.__dictionary.get(key)
        return Converter.get_bool(value=value, default=default)

    # Override
    def get_int(self, key: str, default: Optional[int] = None) -> Optional[int]:
        value = self.__dictionary.get(key)
        return Converter.get_int(value=value, default=default)

    # Override
    def get_float(self, key: str, default: Optional[float] = None) -> Optional[float]:
        value = self.__dictionary.get(key)
        return Converter.get_float(value=value, default=default)

    # Override
    def get_datetime(self, key: str, default: Optional[DateTime] = None) -> Optional[DateTime]:
        value = self.__dictionary.get(key)
        return Converter.get_datetime(value=value, default=default)

    # Override
    def set_datetime(self, key: str, value: Optional[DateTime]):
        if value is None:
            self.__dictionary.pop(key, None)
        else:
            self.__dictionary[key] = value.timestamp

    # Override
    def set_string(self, key: str, value: Optional[Stringer]):
        if value is None:
            self.__dictionary.pop(key, None)
        elif isinstance(value, Stringer):
            self.__dictionary[key] = value.to_str()
        else:
            assert isinstance(value, str), f'str value error: {value}'
            self.__dictionary[key] = value

    # Override
    def set_map(self, key: str, value: Optional[Mapper]):
        if value is None:
            self.__dictionary.pop(key, None)
        elif isinstance(value, Mapper):
            self.__dictionary[key] = value.to_map()
        else:
            assert isinstance(value, MutableMapping), f'map value error: {value}'
            self.__dictionary[key] = value

    # Override
    def to_map(self) -> MutableStrMap:
        return self.__dictionary

    # Override
    def copy_map(self, deep_copy: bool = False) -> MutableStrMap:
        if deep_copy:
            return Copier.deep_copy_map(self.__dictionary)
        else:
            return Copier.copy_map(self.__dictionary)
