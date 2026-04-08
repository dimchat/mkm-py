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

from .types import *
from .format import *
from .digest import *
from .crypto import *
from .protocol import *
from .ext import *

# from .types.string import String
from .protocol.broadcast import BroadcastAddress, Identifier


name = "MingKeMing"

__author__ = 'Albert Moky'

__all__ = [

    #
    #   Types
    #

    'Singleton',

    'URI', 'DateTime',

    'Converter', 'DataConverter', 'BaseConverter',

    'Copier',
    'Wrapper', 'Stringer', 'Mapper',
    'ConstantString',  # 'String',
    'Dictionary',

    #
    #   Format
    #

    'DataCoder', 'Hex', 'Base58', 'Base64',
    'ObjectCoder', 'JSON',
    'MapCoder', 'JSONMap',
    'StringCoder', 'UTF8',

    'hex_encode', 'hex_decode',
    'base58_encode', 'base58_decode',
    'base64_encode', 'base64_decode',
    'json_encode', 'json_decode',
    'utf8_encode', 'utf8_decode',

    'TransportableResource',
    'TransportableData',

    'TransportableDataFactory',

    # 'TransportableDataHelper',
    # 'FormatExtensions', 'shared_format_extensions',

    #
    #   Digest
    #

    'MessageDigester',
    'SHA256', 'KECCAK256', 'RIPEMD160',
    'sha256', 'keccak256', 'ripemd160',

    #
    #   Crypto
    #

    'CryptographyKey',
    'EncryptKey', 'DecryptKey', 'SignKey', 'VerifyKey',
    'SymmetricKey', 'AsymmetricKey',
    'PrivateKey', 'PublicKey',

    'SymmetricKeyFactory', 'PrivateKeyFactory', 'PublicKeyFactory',

    # 'SymmetricKeyHelper', 'PublicKeyHelper', 'PrivateKeyHelper',
    # 'CryptoExtensions', 'shared_crypto_extensions',

    #
    #   Protocol
    #

    'EntityType',
    'Address', 'ID',
    'Meta', 'TAI', 'Document',

    'AddressFactory', 'IDFactory',
    'MetaFactory', 'DocumentFactory',

    'ANYWHERE', 'EVERYWHERE',
    'ANYONE', 'EVERYONE', 'FOUNDER',
    # 'BroadcastAddress', 'Identifier',

    # 'AddressHelper', 'IDHelper',
    # 'MetaHelper', 'DocumentHelper',
    # 'AccountExtensions', 'shared_account_extensions',

    #
    #   Extensions
    #

    'TransportableDataHelper',
    'FormatExtensions', 'shared_format_extensions',

    'SymmetricKeyHelper', 'PublicKeyHelper', 'PrivateKeyHelper',
    'CryptoExtensions', 'shared_crypto_extensions',

    'AddressHelper', 'IDHelper',
    'MetaHelper', 'DocumentHelper',
    'AccountExtensions', 'shared_account_extensions',

    'GeneralCryptoHelper',
    'GeneralAccountHelper',

    #
    #   Core
    #

    # 'String',
    'BroadcastAddress',
    'Identifier',

]
