# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
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

    UTF-8, JsON, Hex, Base58, Base64, ...
    TED, PNF
"""

from .data import DataCoder, Hex, Base58, Base64
from .data import hex_encode, hex_decode
from .data import base58_encode, base58_decode, base64_encode, base64_decode

from .object import ObjectCoder, JSON
from .object import MapCoder, ListCoder, JSONMap, JSONList
from .object import json_encode, json_decode

from .string import StringCoder, UTF8
from .string import utf8_encode, utf8_decode


from .encode import TransportableData, TransportableDataFactory
from .file import PortableNetworkFile, PortableNetworkFileFactory

# from .encode import TransportableDataHelper
# from .file import PortableNetworkFileHelper
# from .helpers import FormatExtensions


name = "Crypto"

__author__ = 'Albert Moky'

__all__ = [

    #
    #   Format
    #

    'DataCoder', 'Hex', 'Base58', 'Base64',
    'ObjectCoder', 'JSON',
    'MapCoder', 'JSONMap',
    'ListCoder', 'JSONList',
    'StringCoder', 'UTF8',

    'hex_encode', 'hex_decode',
    'base58_encode', 'base58_decode',
    'base64_encode', 'base64_decode',
    'json_encode', 'json_decode',
    'utf8_encode', 'utf8_decode',

    'TransportableData',
    'PortableNetworkFile',

    #
    #   Factories
    #

    'TransportableDataFactory',
    'PortableNetworkFileFactory',

    #
    #   Plugins
    #

    # 'TransportableDataHelper', 'PortableNetworkFileHelper',
    # 'FormatExtensions',

]
