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


class DataCoder(ABC):
    """
        Data Coder
        ~~~~~~~~~~
        Hex, Base58, Base64, ...

        1. encode binary data to string;
        2. decode string to binary data.
    """

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


class Hex:
    coder: DataCoder = None

    @staticmethod
    def encode(data: bytes) -> str:
        # assert Hex.coder is not None, 'Hex coder not set yet'
        return Hex.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        # assert Hex.coder is not None, 'Hex coder not set yet'
        return Hex.coder.decode(string=string)


class Base58:
    coder: DataCoder = None

    @staticmethod
    def encode(data: bytes) -> str:
        # assert Base58.coder is not None, 'Base58 coder not set yet'
        return Base58.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        # assert Base58.coder is not None, 'Base58 coder not set yet'
        return Base58.coder.decode(string=string)


class Base64:
    coder: DataCoder = None

    @staticmethod
    def encode(data: bytes) -> str:
        # assert Base64.coder is not None, 'Base64 coder not set yet'
        return Base64.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        # assert Base64.coder is not None, 'Base64 coder not set yet'
        return Base64.coder.decode(string=string)


#
#   Interfaces
#


def base64_encode(data: bytes) -> str:
    return Base64.encode(data)


def base64_decode(string: str) -> Optional[bytes]:
    return Base64.decode(string)


def base58_encode(data: bytes) -> str:
    return Base58.encode(data)


def base58_decode(string: str) -> Optional[bytes]:
    return Base58.decode(string)


def hex_encode(data: bytes) -> str:
    return Hex.encode(data)


def hex_decode(string: str) -> Optional[bytes]:
    return Hex.decode(string)
