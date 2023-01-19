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

    AES = 'AES'
    DES = 'DES'

    #
    #  Factory methods
    #

    @classmethod
    def generate(cls, algorithm: str):  # -> Optional[SymmetricKey]:
        gf = general_factory()
        return gf.generate_symmetric_key(algorithm=algorithm)

    @classmethod
    def parse(cls, key: Any):  # -> Optional[SymmetricKey]:
        gf = general_factory()
        return gf.parse_symmetric_key(key=key)

    @classmethod
    def factory(cls, algorithm: str):  # -> Optional[SymmetricKeyFactory]:
        gf = general_factory()
        return gf.get_symmetric_key_factory(algorithm=algorithm)

    @classmethod
    def register(cls, algorithm: str, factory):
        gf = general_factory()
        gf.set_symmetric_key_factory(algorithm=algorithm, factory=factory)


def general_factory():
    from .factory import FactoryManager
    return FactoryManager.general_factory


class SymmetricKeyFactory(ABC):

    @abstractmethod
    def generate_symmetric_key(self) -> Optional[SymmetricKey]:
        """
        Generate key

        :return: SymmetricKey
        """
        raise NotImplemented

    @abstractmethod
    def parse_symmetric_key(self, key: Dict[str, Any]) -> Optional[SymmetricKey]:
        """
        Parse map object to key

        :param key: key info
        :return: SymmetricKey
        """
        raise NotImplemented
