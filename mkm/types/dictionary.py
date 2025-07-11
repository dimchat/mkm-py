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

from typing import Any, Optional, Iterator, Tuple, Dict
from typing import Mapping, ItemsView, KeysView, ValuesView

from .x import DateTime
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

    def __init__(self, dictionary: Dict = None):
        super().__init__()
        if dictionary is None:
            dictionary = {}
        elif isinstance(dictionary, Mapper):
            dictionary = dictionary.dictionary
        self.__dictionary = dictionary

    @property  # Override
    def dictionary(self) -> Dict:
        return self.__dictionary

    # Override
    def copy_dictionary(self, deep_copy: bool = False) -> Dict:
        if deep_copy:
            return Copier.deep_copy(self.__dictionary)
        else:
            return self.__dictionary.copy()

    # Override
    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        self.__dictionary.clear()

    # Override
    def copy(self):
        """ D.copy() -> a shallow copy of D """
        dictionary = self.__dictionary.copy()
        return Dictionary(dictionary=dictionary)

    @staticmethod
    def fromkeys(*args, **kwargs):
        """ Create a new dictionary with keys from iterable and values set to value. """
        dictionary = dict.fromkeys(*args, **kwargs)
        return Dictionary(dictionary=dictionary)

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
        else:
            self.__dictionary[key] = value.string

    # Override
    def set_map(self, key: str, value: Optional[Mapper]):
        if value is None:
            self.__dictionary.pop(key, None)
        else:
            self.__dictionary[key] = value.dictionary

    # Override
    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """ Return the value for key if key is in the dictionary, else default. """
        return self.__dictionary.get(key, default)

    # Override
    def items(self) -> ItemsView[str, Any]:
        """ D.items() -> a set-like object providing a view on D's items """
        return self.__dictionary.items()

    # Override
    def keys(self) -> KeysView[str]:
        """ D.keys() -> a set-like object providing a view on D's keys """
        return self.__dictionary.keys()

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
    def setdefault(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        """
        self.__dictionary.setdefault(key, default)

    # Override
    def update(self, __m: Mapping[str, Any], **kwargs: Any):
        self.__dictionary.update(__m, **kwargs)

    # Override
    def values(self) -> ValuesView[Any]:
        """ D.values() -> an object providing a view on D's values """
        return self.__dictionary.values()

    def __contains__(self, o) -> bool:
        """ True if the dictionary has the specified key, else False. """
        return self.__dictionary.__contains__(o)

    def __delitem__(self, v: str):
        """ Delete self[key]. """
        self.__dictionary.__delitem__(v)

    def __eq__(self, o: Dict) -> bool:
        """ Return self==value. """
        if isinstance(o, Mapper):
            if self is o:
                # same object
                return True
            o = o.dictionary
        # check inner map
        return self.__dictionary.__eq__(o)

    # def __getattribute__(self, name: str) -> Any:
    #     """ Return getattr(self, name). """
    #     if isinstance(name, Stringer):
    #         name = name.string
    #     return self.__dictionary.__getattribute__(name=name)

    def __getitem__(self, k: str) -> Any:
        """ x.__getitem__(y) <==> x[y] """
        return self.__dictionary.__getitem__(k)

    def __ge__(self, other) -> bool:
        """ Return self>=value. """
        pass

    def __gt__(self, other) -> bool:
        """ Return self>value. """
        pass

    def __iter__(self) -> Iterator[str]:
        """ Implement iter(self). """
        return self.__dictionary.__iter__()

    def __len__(self) -> int:
        """ Return len(self). """
        return self.__dictionary.__len__()

    def __le__(self, other) -> bool:
        """ Return self<=value. """
        pass

    def __lt__(self, other) -> bool:
        """ Return self<value. """
        pass

    def __ne__(self, o: Dict) -> bool:
        """ Return self!=value. """
        if isinstance(o, Mapper):
            if self is o:
                # same object
                return False
            o = o.dictionary
        # check inner map
        return self.__dictionary.__ne__(o)

    def __repr__(self) -> str:
        """ Return repr(self). """
        return self.__dictionary.__repr__()

    def __setitem__(self, k: str, v: Optional[Any]):
        """ Set self[key] to value. """
        self.__dictionary.__setitem__(k, v)

    def __sizeof__(self) -> int:
        """ D.__sizeof__() -> size of D in memory, in bytes """
        return self.__dictionary.__sizeof__()

    __hash__ = None
