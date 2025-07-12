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
from typing import Optional, Any, Dict

from .cryptography import EncryptKey, DecryptKey
from .helpers import CryptoExtensions


# noinspection PyAbstractClass
class SymmetricKey(EncryptKey, DecryptKey, ABC):
    """This class is used to encrypt or decrypt message data

        Symmetric Cryptography Key
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        key data format: {
            algorithm : "AES", // "DES", ...
            data      : "{BASE64_ENCODE}",
            ...
        }
    """

    # AES = 'AES'  # -- "AES/CBC/PKCS7Padding"
    # DES = 'DES'

    #
    #  Factory methods
    #

    @classmethod
    def generate(cls, algorithm: str):  # -> Optional[SymmetricKey]:
        helper = symmetric_helper()
        return helper.generate_symmetric_key(algorithm=algorithm)

    @classmethod
    def parse(cls, key: Any):  # -> Optional[SymmetricKey]:
        helper = symmetric_helper()
        return helper.parse_symmetric_key(key)

    @classmethod
    def get_factory(cls, algorithm: str):  # -> Optional[SymmetricKeyFactory]:
        helper = symmetric_helper()
        return helper.get_symmetric_key_factory(algorithm=algorithm)

    @classmethod
    def set_factory(cls, algorithm: str, factory):
        helper = symmetric_helper()
        helper.set_symmetric_key_factory(algorithm=algorithm, factory=factory)


def symmetric_helper():
    helper = CryptoExtensions.symmetric_helper
    assert isinstance(helper, SymmetricKeyHelper), 'symmetric helper error: %s' % helper
    return helper


class SymmetricKeyFactory(ABC):
    """ Key Factory """

    @abstractmethod
    def generate_symmetric_key(self) -> SymmetricKey:
        """
        Generate key

        :return: SymmetricKey
        """
        raise NotImplemented

    @abstractmethod
    def parse_symmetric_key(self, key: Dict) -> Optional[SymmetricKey]:
        """
        Parse map object to key

        :param key: key info
        :return: SymmetricKey
        """
        raise NotImplemented


########################
#                      #
#   Plugins: Helpers   #
#                      #
########################


class SymmetricKeyHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_symmetric_key_factory(self, algorithm: str, factory: SymmetricKeyFactory):
        raise NotImplemented

    @abstractmethod
    def get_symmetric_key_factory(self, algorithm: str) -> Optional[SymmetricKeyFactory]:
        raise NotImplemented

    @abstractmethod
    def generate_symmetric_key(self, algorithm: str) -> Optional[SymmetricKey]:
        raise NotImplemented

    @abstractmethod
    def parse_symmetric_key(self, key: Any) -> Optional[SymmetricKey]:
        raise NotImplemented
