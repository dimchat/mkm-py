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
    Data Format
    ~~~~~~~~~~~

    Base64, Base58, Hex, UTF-8, JsON
"""

import base64
import json
from abc import ABC, abstractmethod
from typing import Optional, Union, Any, Dict, List


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


class ObjectCoder(ABC):
    """
        Object Coder
        ~~~~~~~~~~~~
        JsON, XML, ...

        1. encode object to string;
        2. decode string to object.
    """

    @abstractmethod
    def encode(self, obj: Any) -> str:
        """
        Encode Map/List object to str

        :param obj: Map or List
        :return: serialized string
        """
        raise NotImplemented

    @abstractmethod
    def decode(self, string: str) -> Optional[Any]:
        """
        Decode str to Map/List object

        :param string: serialized string
        :return: Map or List
        """
        raise NotImplemented


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


"""
    Interfaces
"""


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


def json_encode(obj: Union[Dict, List]) -> str:
    return JSON.encode(obj=obj)


def json_decode(string: str) -> Union[Dict, List, None]:
    return JSON.decode(string=string)


def utf8_encode(string: str) -> bytes:
    return UTF8.encode(string=string)


def utf8_decode(data: bytes) -> Optional[str]:
    return UTF8.decode(data=data)


"""
    Implementations
    ~~~~~~~~~~~~~~~
    
    Data coders
"""


class B64(DataCoder):

    # Override
    def encode(self, data: bytes) -> str:
        """ BASE-64 Encode """
        return base64.b64encode(data).decode('utf-8')

    # Override
    def decode(self, string: str) -> Optional[bytes]:
        """ BASE-64 Decode """
        return base64.b64decode(string)


class H(DataCoder):

    # Override
    def encode(self, data: bytes) -> str:
        """ HEX Encode """
        # return binascii.b2a_hex(data).decode('utf-8')
        return data.hex()

    # Override
    def decode(self, string: str) -> Optional[bytes]:
        """ HEX Decode """
        # return binascii.a2b_hex(string)
        return bytes.fromhex(string)


class Base64:
    coder: DataCoder = B64()

    @staticmethod
    def encode(data: bytes) -> str:
        # assert Base64.coder is not None, 'Base64 coder not set yet'
        return Base64.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        # assert Base64.coder is not None, 'Base64 coder not set yet'
        return Base64.coder.decode(string=string)


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


class Hex:
    coder: DataCoder = H()

    @staticmethod
    def encode(data: bytes) -> str:
        # assert Hex.coder is not None, 'Hex coder not set yet'
        return Hex.coder.encode(data=data)

    @staticmethod
    def decode(string: str) -> Optional[bytes]:
        # assert Hex.coder is not None, 'Hex coder not set yet'
        return Hex.coder.decode(string=string)


"""
    Implementations
    ~~~~~~~~~~~~~~~

    Data parsers
"""


class J(ObjectCoder):

    # Override
    def encode(self, obj: Any) -> str:
        """ JsON encode """
        return json.dumps(obj)

    # Override
    def decode(self, string: str) -> Optional[Any]:
        """ JsON decode """
        return json.loads(string)


class U(StringCoder):

    # Override
    def encode(self, string: str) -> bytes:
        """ UTF-8 encode """
        return string.encode('utf-8')

    # Override
    def decode(self, data: bytes) -> Optional[str]:
        """ UTF-8 decode """
        return data.decode('utf-8')


class JSON:
    coder: ObjectCoder = J()

    @staticmethod
    def encode(obj: Any) -> str:
        # assert JSON.coder is not None, 'JSON parser not set yet'
        return JSON.coder.encode(obj=obj)

    @staticmethod
    def decode(string: str) -> Optional[Any]:
        # assert JSON.coder is not None, 'JSON parser not set yet'
        return JSON.coder.decode(string=string)


class UTF8:
    coder: StringCoder = U()

    @staticmethod
    def encode(string: str) -> bytes:
        # assert UTF8.coder is not None, 'UTF8 parser not set yet'
        return UTF8.coder.encode(string=string)

    @staticmethod
    def decode(data: bytes) -> Optional[str]:
        # assert UTF8.coder is not None, 'UTF8 parser not set yet'
        return UTF8.coder.decode(data=data)
