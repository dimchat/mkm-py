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
from typing import Optional


class StringCoder(ABC):
    """
        String Coder
        ~~~~~~~~~~~~
        UTF-8, UTF-16, GBK, GB2312, ...

        1. encode string to binary data;
        2. decode binary data to string.
    """

    @abstractmethod
    def encode(self, string: str) -> bytes:
        """
        Encode local string to binary data

        :param string: local string
        :return: binary data
        """
        raise NotImplemented

    @abstractmethod
    def decode(self, data: bytes) -> Optional[str]:
        """
        Decode binary data to local string

        :param data: binary data
        :return: local string
        """
        raise NotImplemented


class UTF8:
    coder: StringCoder = None

    @staticmethod
    def encode(string: str) -> bytes:
        # assert UTF8.coder is not None, 'UTF8 parser not set yet'
        return UTF8.coder.encode(string=string)

    @staticmethod
    def decode(data: bytes) -> Optional[str]:
        # assert UTF8.coder is not None, 'UTF8 parser not set yet'
        return UTF8.coder.decode(data=data)


#
#   Interfaces
#


def utf8_encode(string: str) -> bytes:
    return UTF8.encode(string=string)


def utf8_decode(data: bytes) -> Optional[str]:
    return UTF8.decode(data=data)
