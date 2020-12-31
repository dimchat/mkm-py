# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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

from .crypto import SOMap, Dictionary

from .crypto import DataCoder, Base64, Base58, Hex
from .crypto import base64_encode, base64_decode, base58_encode, base58_decode, hex_encode, hex_decode
from .crypto import DataParser, JSON, UTF8
from .crypto import json_encode, json_decode, utf8_encode, utf8_decode
from .crypto import DataDigester, MD5, SHA1, SHA256, KECCAK256, RIPEMD160
from .crypto import md5, sha1, sha256, keccak256, ripemd160

from .crypto import CryptographyKey, EncryptKey, DecryptKey
from .crypto import AsymmetricKey, SignKey, VerifyKey
from .crypto import PublicKey, PublicKeyFactory
from .crypto import PrivateKey, PrivateKeyFactory
from .crypto import SymmetricKey, SymmetricKeyFactory

from .types import NetworkType, MetaType
from .address import Address, AddressFactory, ANYWHERE, EVERYWHERE
from .identifier import ID, ANYONE, EVERYONE
from .meta import Meta, BaseMeta, MetaFactory
from .tai import Document
from .profile import Visa, Bulletin, BaseDocument, BaseVisa, BaseBulletin, DocumentFactory

name = "MingKeMing"

__author__ = 'Albert Moky'

__all__ = [

    # Types
    'SOMap', 'Dictionary',

    # Data
    'DataCoder', 'Base64', 'Base58', 'Hex',
    'base64_encode', 'base64_decode', 'base58_encode', 'base58_decode', 'hex_encode', 'hex_decode',
    'DataParser', 'JSON', 'UTF8',
    'json_encode', 'json_decode', 'utf8_encode', 'utf8_decode',
    'DataDigester', 'MD5', 'SHA1', 'SHA256', 'KECCAK256', 'RIPEMD160',
    'md5', 'sha1', 'sha256', 'keccak256', 'ripemd160',

    # Crypto
    'CryptographyKey', 'EncryptKey', 'DecryptKey',
    'AsymmetricKey', 'SignKey', 'VerifyKey',
    'PublicKey', 'PublicKeyFactory',
    'PrivateKey', 'PrivateKeyFactory',
    'SymmetricKey', 'SymmetricKeyFactory',

    # Entity
    'NetworkType', 'MetaType',
    'Address', 'AddressFactory',
    'ID', 'ANYONE', 'EVERYONE', 'ANYWHERE', 'EVERYWHERE',
    'Meta', 'BaseMeta', 'MetaFactory',
    'Document', 'BaseDocument', 'DocumentFactory',
    'Visa', 'BaseVisa', 'Bulletin', 'BaseBulletin',
]
