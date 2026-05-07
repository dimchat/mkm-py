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

from .x import DateTime


class Stringer(ABC):
    """
        Constant String Wrapper
        ~~~~~~~~~~~~~~~~~~~~~~~
    """

    def __hash__(self) -> int:
        """ Return hash(self). """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__hash__()'
        )

    def __len__(self) -> int:
        """ Return len(self). """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__len__()'
        )

    def __eq__(self, other) -> bool:
        """ Return self==value. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__eq__()'
        )

    def __ne__(self, other) -> bool:
        """ Return self!=value. """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__ne__()'
        )

    def __str__(self) -> str:
        """ Return str(self). """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__str__()'
        )

    @abstractmethod
    def to_str(self) -> str:
        """ get inner string """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.to_str()'
        )


class Mapper(MutableMapping[str, Any], ABC):
    """
        Mutable Map Wrapper
        ~~~~~~~~~~~~~~~~~~~
    """

    @abstractmethod
    def get_str(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """ Get string value for key, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_str()'
        )

    @abstractmethod
    def get_bool(self, key: str, default: Optional[bool] = None) -> Optional[bool]:
        """ Get boolean value for key, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_bool()'
        )

    @abstractmethod
    def get_int(self, key: str, default: Optional[int] = None) -> Optional[int]:
        """ Get integer value for key, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_int()'
        )

    @abstractmethod
    def get_float(self, key: str, default: Optional[float] = None) -> Optional[float]:
        """ Get float number for key, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_float()'
        )

    @abstractmethod
    def get_datetime(self, key: str, default: Optional[DateTime] = None) -> Optional[DateTime]:
        """ Get DataTime object for key, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_datetime()'
        )

    @abstractmethod
    def set_datetime(self, key: str, value: Optional[DateTime]):
        """ Set DateTime object for key """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_datetime()'
        )

    @abstractmethod
    def set_string(self, key: str, value: Optional[Stringer]):
        """ Set Stringer object for key """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_string()'
        )

    @abstractmethod
    def set_map(self, key: str, value):  # value: Optional[Mapper]
        """ Set Mapper object for key """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_map()'
        )

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """ Get inner map """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.to_dict()'
        )

    @abstractmethod
    def copy_dict(self, deep_copy: bool = False) -> Dict[str, Any]:
        """ Copy inner map """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.copy_dict()'
        )


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
    def get_dict(self, d) -> Optional[Dict]:
        """ Shallow unwrap Dict value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_dict()'
        )

    @abstractmethod
    def unwrap(self, o) -> Any:
        """ Deep unwrap value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.unwrap()'
        )

    @abstractmethod
    def unwrap_dict(self, d) -> Dict:
        """ Deep unwrap Dict value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.unwrap_dict()'
        )

    @abstractmethod
    def unwrap_list(self, a) -> List[Any]:
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
            # assert False, 'string error: %s' % s
            return str(s)

    # Override
    def get_dict(self, d) -> Optional[Dict]:
        if d is None:
            return None
        elif isinstance(d, Mapper):
            return d.to_dict()
        elif isinstance(d, Dict):
            return d
        else:
            assert False, 'map error: %s' % d

    # Override
    def unwrap(self, o) -> Any:
        if o is None:
            return None
        elif isinstance(o, Mapper):
            return self.unwrap_dict(o.to_dict())
        elif isinstance(o, Dict):
            return self.unwrap_dict(o)
        elif isinstance(o, List):
            return self.unwrap_list(o)
        elif isinstance(o, Stringer):
            return o.to_str()
        else:
            return o

    # Override
    def unwrap_dict(self, d) -> Dict:
        if isinstance(d, Mapper):
            d = d.to_dict()
        dictionary = {}
        for key in d:
            value = d[key]
            naked = self.unwrap(value)
            dictionary[key] = naked
        return dictionary

    # Override
    def unwrap_list(self, a) -> List[Any]:
        array = []
        for item in a:
            naked = self.unwrap(item)
            array.append(naked)
        return array


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
    def get_dict(cls, d) -> Optional[Dict]:
        """
            Get inner map
            ~~~~~~~~~~~~~
            Remove first wrapper
        """
        return cls.wrapper.get_dict(d)

    @classmethod
    def unwrap(cls, o) -> Any:
        """
            Unwrap object container
            ~~~~~~~~~~~~~~~~~~~~~~~
        """
        return cls.wrapper.unwrap(o)

    @classmethod
    def unwrap_dict(cls, d) -> Dict:
        """ Unwrap values for keys in map """
        return cls.wrapper.unwrap_dict(d)

    @classmethod
    def unwrap_list(cls, a) -> List[Any]:
        """ Unwrap values in the array """
        return cls.wrapper.unwrap_list(a)
