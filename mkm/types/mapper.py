# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2026 Albert Moky
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
from collections.abc import MutableMapping
from typing import Optional

from .x import DateTime
from .x import MutableStrMap

from .stringer import Stringer


class Mapper(MutableMapping, ABC):
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
    def to_map(self) -> MutableStrMap:
        """ Get inner map """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.to_map()'
        )

    @abstractmethod
    def copy_map(self, deep_copy: bool = False) -> MutableStrMap:
        """ Copy inner map """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.copy_map()'
        )
