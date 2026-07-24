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

from abc import ABC, abstractmethod
from collections.abc import Mapping, MutableMapping
from typing import Optional

from ..types import Singleton
from ..types import Mapper
from ..format import TransportableData


class CryptographyKey(Mapper, ABC):
    """Cryptography key with designated algorithm

        Cryptography Key
        ~~~~~~~~~~~~~~~~

        key data format: {
            algorithm : "RSA", // ECC, AES, ...
            data      : "{BASE64_ENCODE}",
            ...
        }
    """

    @property
    @abstractmethod
    def algorithm(self) -> str:
        """
        Get key algorithm name

        :return: algorithm name
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.algorithm getter'
        )

    @property
    @abstractmethod
    def data(self) -> TransportableData:
        """
        Get key data

        :return: key data
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.data getter'
        )


class EncryptKey(CryptographyKey, ABC):

    @abstractmethod
    def encrypt(self, plaintext: bytes, extra: Optional[MutableMapping] = None) -> bytes:
        """
        1. Symmetric Key:
            ciphertext = encrypt(plaintext, PW)
        2. Asymmetric Public Key:
            ciphertext = encrypt(plaintext, PK)

        :param plaintext: original data
        :param extra:     store extra variables ('IV' for 'AES')
        :return: ciphertext
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.encrypt()'
        )


class DecryptKey(CryptographyKey, ABC):

    @abstractmethod
    def decrypt(self, ciphertext: bytes, params: Optional[Mapping] = None) -> Optional[bytes]:
        """
        1. Symmetric Key:
            plaintext = decrypt(ciphertext, PW)
        2. Asymmetric Private Key:
            plaintext = decrypt(ciphertext, SK)

        :param ciphertext: encrypted data
        :param params:     extra params ('IV' for 'AES')
        :return: plaintext
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.decrypt()'
        )

    @abstractmethod
    def match_encrypt_key(self, key: EncryptKey) -> bool:
        """
        CT = encrypt(data, PK)
        OK = decrypt(CT, SK) == data

        :param key: encrypt (public) key
        :return: False on error
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.match_encrypt_key()'
        )


# -----------------------------------------------------------------------------
#  Crypto Extensions
# -----------------------------------------------------------------------------


@Singleton
class CryptoExtensions:
    pass


# global
shared_crypto_extensions = CryptoExtensions()
