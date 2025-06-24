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
from typing import Optional, Dict

from ..types import Mapper


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
        raise NotImplemented

    @property
    @abstractmethod
    def data(self) -> bytes:
        """
        Get key data

        :return: key data
        """
        raise NotImplemented


class EncryptKey(CryptographyKey, ABC):

    @abstractmethod
    def encrypt(self, data: bytes, extra: Optional[Dict]) -> bytes:
        """
        1. Symmetric Key:
            ciphertext = encrypt(plaintext, PW)
        2. Asymmetric Public Key:
            ciphertext = encrypt(plaintext, PK)

        :param data:  plaintext
        :param extra: store extra variables ('IV' for 'AES')
        :return: ciphertext
        """
        raise NotImplemented


class DecryptKey(CryptographyKey, ABC):

    @abstractmethod
    def decrypt(self, data: bytes, params: Optional[Dict]) -> Optional[bytes]:
        """
        1. Symmetric Key:
            plaintext = decrypt(ciphertext, PW)
        2. Asymmetric Private Key:
            plaintext = decrypt(ciphertext, SK)

        :param data:   ciphertext
        :param params: extra params ('IV' for 'AES')
        :return: plaintext
        """
        raise NotImplemented

    @abstractmethod
    def match_encrypt_key(self, key: EncryptKey) -> bool:
        """
        CT = encrypt(data, PK)
        OK = decrypt(CT, SK) == data

        :param key: encrypt (public) key
        :return: False on error
        """
        raise NotImplemented
