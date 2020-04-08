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

"""
    Base Coder
    ~~~~~~~~~~

    Base64, Base58, Hex
"""

from abc import ABC, abstractmethod
from typing import Optional

import base64
import binascii


class BaseCoder(ABC):

    @abstractmethod
    def encode(self, data: bytes) -> str:
        """
        Encode binary data to text string

        :param data: binary data
        :return:     text string (Base58/64, Hex, ...)
        """
        raise NotImplemented

    @abstractmethod
    def decode(self, string: str) -> Optional[bytes]:
        """
        Decode text string to binary data

        :param string: text string (Base58/64, Hex, ...)
        :return:       binary data
        """
        raise NotImplemented


"""
    Implementations
"""


class B64(BaseCoder):

    def encode(self, data: bytes) -> str:
        """ BASE-64 Encode """
        return base64.b64encode(data).decode('utf-8')

    def decode(self, string: str) -> Optional[bytes]:
        """ BASE-64 Decode """
        return base64.b64decode(string)


class H(BaseCoder):

    def encode(self, data: bytes) -> str:
        """ HEX Encode """
        return binascii.b2a_hex(data).decode('utf-8')

    def decode(self, string: str) -> Optional[bytes]:
        """ HEX Decode """
        return binascii.a2b_hex(string)


"""
    Interfaces
"""


class Base64:

    coder: BaseCoder = B64()

    @staticmethod
    def encode(data: bytes) -> str:
        assert Base64.coder is not None, 'Base64 coder not set yet'
        return Base64.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        assert Base64.coder is not None, 'Base64 coder not set yet'
        return Base64.coder.decode(string=string)


class Base58:

    coder: BaseCoder = None

    @staticmethod
    def encode(data: bytes) -> str:
        assert Base58.coder is not None, 'Base58 coder not set yet'
        return Base58.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        assert Base58.coder is not None, 'Base58 coder not set yet'
        return Base58.coder.decode(string=string)


class Hex:

    coder: BaseCoder = H()

    @staticmethod
    def encode(data: bytes) -> str:
        assert Hex.coder is not None, 'Hex coder not set yet'
        return Hex.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        assert Hex.coder is not None, 'Hex coder not set yet'
        return Hex.coder.decode(string=string)
