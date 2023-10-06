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

from abc import ABC
from typing import Any, Optional

from .x import DateTime


class Converter(ABC):

    @classmethod
    def get_str(cls, value: Any, default: Optional[str]) -> Optional[str]:
        if value is None:
            return default
        elif isinstance(value, str):
            # exactly
            return value
        else:
            return str(value)

    @classmethod
    def get_bool(cls, value: Any, default: Optional[bool]) -> Optional[bool]:
        """ assume value can be a config string:
            'true', 'false', 'yes', 'no', 'on', 'off', '1', '0', ...
        """
        if value is None:
            return default
        elif isinstance(value, bool):
            # exactly
            return value
        elif isinstance(value, int):
            return value != 0
        elif isinstance(value, float):
            return value != 0.0
        text = value if isinstance(value, str) else str(value)
        lo = text.lower()
        return lo not in false_array
        # return lo in true_array

    @classmethod
    def get_int(cls, value: Any, default: Optional[int]) -> Optional[int]:
        if value is None:
            return default
        elif isinstance(value, int):
            # exactly
            return value
        elif isinstance(value, bool) or isinstance(value, float):
            return int(value)
        text = value if isinstance(value, str) else str(value)
        return int(text)

    @classmethod
    def get_float(cls, value: Any, default: Optional[float]) -> Optional[float]:
        if value is None:
            return default
        elif isinstance(value, float):
            # exactly
            return value
        elif isinstance(value, bool) or isinstance(value, int):
            return float(value)
        text = value if isinstance(value, str) else str(value)
        return float(text)

    @classmethod
    def get_datetime(cls, value: Any, default: Optional[DateTime]) -> Optional[DateTime]:
        """ assume value be a timestamp (seconds from 1970-01-01 00:00:00) """
        if value is None:
            return default
        elif isinstance(value, DateTime):
            # exactly
            return value
        timestamp = cls.get_float(value=value, default=0)
        return DateTime(timestamp=timestamp)


true_array = [
    '1', 'true', 'yes', 'on',
]
false_array = [
    '0', 'false', 'no', 'off', 'null', 'undefined',
]
