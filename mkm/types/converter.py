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


class Converter(ABC):

    @classmethod
    def get_str(cls, value: Any) -> Optional[str]:
        if value is None:
            return None
        elif isinstance(value, str):
            # exactly
            return value
        else:
            return str(value)

    @classmethod
    def get_bool(cls, value: Any) -> Optional[bool]:
        """ assume value can be a config string:
            'true', 'false', 'yes', 'no', 'on', 'off', '1', '0', ...
        """
        if value is None:
            return None
        elif isinstance(value, bool):
            # exactly
            return value
        elif isinstance(value, int):
            return value != 0
        elif isinstance(value, float):
            return value != 0.0
        elif isinstance(value, str):
            lo = value.lower()
            # return lo in true_array
            return lo not in false_array
        else:
            return True

    @classmethod
    def get_int(cls, value: Any) -> Optional[int]:
        if value is None:
            return None
        elif isinstance(value, int):
            # exactly
            return value
        elif isinstance(value, bool) or isinstance(value, float) or isinstance(value, str):
            return int(value)
        else:
            return 0

    @classmethod
    def get_float(cls, value: Any) -> Optional[float]:
        if value is None:
            return None
        elif isinstance(value, float):
            # exactly
            return value
        elif isinstance(value, bool) or isinstance(value, int) or isinstance(value, str):
            return float(value)
        else:
            return 0.0

    @classmethod
    def get_time(cls, value: Any) -> Optional[float]:
        """ assume value be a timestamp in seconds
            (from 1970-01-01 00:00:00)
        """
        return cls.get_float(value=value)


true_array = [
    'true', 'yes', 'on', '1',
]
false_array = [
    'false', 'no', 'off', '0', 'null', 'undefined',
]
