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
    Crypto
    ~~~~~~

    Crypto Keys: SymmetricKey, PrivateKey, PublicKey
"""

from .digest import *

from .cryptography import CryptographyKey, EncryptKey, DecryptKey
from .asymmetric import AsymmetricKey, SignKey, VerifyKey
from .symmetric import SymmetricKey, SymmetricKeyFactory
from .public import PublicKey, PublicKeyFactory
from .private import PrivateKey, PrivateKeyFactory

# from .symmetric import SymmetricKeyHelper
# from .public import PublicKeyHelper
# from .private import PrivateKeyHelper
# from .helpers import CryptoExtensions

name = "Crypto"

__author__ = 'Albert Moky'

__all__ = [

    #
    #   Data Digest
    #

    'DataDigester',
    'MD5', 'SHA1', 'SHA256', 'KECCAK256', 'RIPEMD160',

    'md5', 'sha1', 'sha256', 'keccak256', 'ripemd160',

    #
    #   Crypto
    #

    'CryptographyKey',
    'EncryptKey', 'DecryptKey', 'SignKey', 'VerifyKey',
    'SymmetricKey', 'AsymmetricKey',
    'PrivateKey', 'PublicKey',

    #
    #   Factories
    #

    'SymmetricKeyFactory', 'PrivateKeyFactory', 'PublicKeyFactory',

    #
    #   Plugins
    #

    # 'SymmetricKeyHelper', 'PublicKeyHelper', 'PrivateKeyHelper',
    # 'CryptoExtensions',

]
