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
from typing import Any, Optional

from .x import DateTime


######################
#                    #
#   Data Converter   #
#                    #
######################


class DataConverter(ABC):

    @abstractmethod
    def get_str(self, value: Any, default: Optional[str]) -> Optional[str]:
        """ Convert the value to a string, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_str()'
        )

    @abstractmethod
    def get_bool(self, value: Any, default: Optional[bool]) -> Optional[bool]:
        """ Convert the value to a boolean value, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_bool()'
        )

    @abstractmethod
    def get_int(self, value: Any, default: Optional[int]) -> Optional[int]:
        """ Convert the value to a integer, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_int()'
        )

    @abstractmethod
    def get_float(self, value: Any, default: Optional[float]) -> Optional[float]:
        """ Convert the value to a float number, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_float()'
        )

    @abstractmethod
    def get_datetime(self, value: Any, default: Optional[DateTime]) -> Optional[DateTime]:
        """ Convert the value to a DateTime object, if value is None, return the default value """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_datetime()'
        )


class BaseConverter(DataConverter):

    # Override
    def get_str(self, value: Any, default: Optional[str]) -> Optional[str]:
        if value is None:
            return default
        elif isinstance(value, str):
            # exactly
            return value
        else:
            # assert False, f'not a string value: {value}'
            return str(value)

    # Override
    def get_bool(self, value: Any, default: Optional[bool]) -> Optional[bool]:
        if value is None:
            return default
        elif isinstance(value, bool):
            # exactly
            return value
        elif isinstance(value, int):
            assert value == 1 or value == 0, f'bool value error: {value}'
            return value != 0
        elif isinstance(value, float):
            assert value == 1.0 or value == 0.0, f'bool value error: {value}'
            return value != 0.0
        else:
            text = to_str(value=value)
        text = text.strip()
        size = len(text)
        if size == 0:
            return False
        elif size > Converter.MAX_BOOLEAN_LEN:
            raise ValueError(f'bool value error: "{value}"')
        text = text.lower()
        state = Converter.BOOLEAN_STATES.get(text)
        if state is None:
            raise ValueError(f'bool value error: "{value}"')
        return state

    # Override
    def get_int(self, value: Any, default: Optional[int]) -> Optional[int]:
        if value is None:
            return default
        elif isinstance(value, int):
            # exactly
            return value
        elif isinstance(value, float):
            return int(value)
        elif isinstance(value, bool):
            return 1 if value else 0
        else:
            text = to_str(value=value)
            return int(text)

    # Override
    def get_float(self, value: Any, default: Optional[float]) -> Optional[float]:
        if value is None:
            return default
        elif isinstance(value, float):
            # exactly
            return value
        elif isinstance(value, int):
            return float(value)
        elif isinstance(value, bool):
            return 1.0 if value else 0.0
        else:
            text = to_str(value=value)
            return float(text)

    # Override
    def get_datetime(self, value: Any, default: Optional[DateTime]) -> Optional[DateTime]:
        if value is None:
            return default
        elif isinstance(value, DateTime):
            # exactly
            return value
        seconds = self.get_float(value=value, default=None)
        if seconds is None or seconds < 0:
            raise ValueError(f'Timestamp error: "{value}"')
        else:
            return DateTime(timestamp=seconds)


def to_str(value: Any) -> str:
    if isinstance(value, str):
        return value
    else:
        return str(value)


class Converter(ABC):
    """ Data Convert Interface """

    BOOLEAN_STATES = {
        '1': True, 'yes': True, 'true': True, 'on': True,

        '0': False, 'no': False, 'false': False, 'off': False,
        # '+0': False, '-0': False, '0.0': False, '+0.0': False, '-0.0': False,
        'null': False, 'none': False, 'undefined': False,
    }
    MAX_BOOLEAN_LEN = len('undefined')

    # Singleton
    converter: DataConverter = BaseConverter()

    @classmethod
    def get_str(cls, value: Any, default: Optional[str] = None) -> Optional[str]:
        return cls.converter.get_str(value=value, default=default)

    @classmethod
    def get_bool(cls, value: Any, default: Optional[bool] = None) -> Optional[bool]:
        """ assume value can be a config string:
            'true', 'false', 'yes', 'no', 'on', 'off', '1', '0', ...
        """
        return cls.converter.get_bool(value=value, default=default)

    @classmethod
    def get_int(cls, value: Any, default: Optional[int] = None) -> Optional[int]:
        return cls.converter.get_int(value=value, default=default)

    @classmethod
    def get_float(cls, value: Any, default: Optional[float] = None) -> Optional[float]:
        return cls.converter.get_float(value=value, default=default)

    @classmethod
    def get_datetime(cls, value: Any, default: Optional[DateTime] = None) -> Optional[DateTime]:
        """ assume value be a timestamp (seconds from 1970-01-01 00:00:00) """
        return cls.converter.get_datetime(value=value, default=default)
