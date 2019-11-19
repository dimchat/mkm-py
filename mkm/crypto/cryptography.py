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

from abc import ABCMeta, abstractmethod
from typing import Optional


class CryptographyKey(dict, metaclass=ABCMeta):
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
    def data(self) -> bytes:
        """
        Get key data

        :return: key data
        """
        raise NotImplemented


class EncryptKey(metaclass=ABCMeta):

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        """
        ciphertext = encrypt(plaintext, PW)
        ciphertext = encrypt(plaintext, PK)

        :param data: plaintext
        :return:     ciphertext
        """
        raise NotImplemented


class DecryptKey(metaclass=ABCMeta):

    @abstractmethod
    def decrypt(self, data: bytes) -> Optional[bytes]:
        """
        plaintext = decrypt(ciphertext, PW);
        plaintext = decrypt(ciphertext, SK);

        :param data: ciphertext
        :return:     plaintext
        """
        raise NotImplemented


class SignKey(metaclass=ABCMeta):

    @abstractmethod
    def sign(self, data: bytes) -> bytes:
        """
        signature = sign(data, SK);

        :param data: message data
        :return:     signature
        """
        raise NotImplemented


class VerifyKey(metaclass=ABCMeta):

    @abstractmethod
    def verify(self, data: bytes, signature: bytes) -> bool:
        """
        OK = verify(data, signature, PK)

        :param data:      message data
        :param signature: signature of message data
        :return:          True on signature matched
        """
        raise NotImplemented
