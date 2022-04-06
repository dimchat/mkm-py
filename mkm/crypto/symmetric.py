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
from typing import Optional, Any

from ..wrappers import MapWrapper

from .cryptography import EncryptKey, DecryptKey, key_algorithm
from .factories import Factories


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

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if isinstance(other, SymmetricKey):
            return self.match(key=other)

    #
    #  Factory methods
    #

    @classmethod
    def generate(cls, algorithm: str):  # -> Optional[SymmetricKey]:
        factory = cls.factory(algorithm=algorithm)
        assert isinstance(factory, SymmetricKeyFactory), 'key algorithm not support: %s' % algorithm
        return factory.generate_symmetric_key()

    @classmethod
    def parse(cls, key: Any):  # -> Optional[SymmetricKey]:
        if key is None:
            return None
        elif isinstance(key, cls):
            return key
        elif isinstance(key, MapWrapper):
            key = key.dictionary
        # assert isinstance(key, dict), 'key error: %s' % key
        algorithm = key_algorithm(key=key)
        factory = cls.factory(algorithm=algorithm)
        if factory is None:
            factory = cls.factory(algorithm='*')  # unknown
            assert factory is not None, 'cannot parse key: %s' % key
        assert isinstance(factory, SymmetricKeyFactory), 'key algorithm not support: %s' % algorithm
        return factory.parse_symmetric_key(key=key)

    @classmethod
    def factory(cls, algorithm: str):  # -> Optional[SymmetricKeyFactory]:
        return Factories.symmetric_key_factories.get(algorithm)

    @classmethod
    def register(cls, algorithm: str, factory):
        Factories.symmetric_key_factories[algorithm] = factory


class SymmetricKeyFactory(ABC):

    @abstractmethod
    def generate_symmetric_key(self) -> Optional[SymmetricKey]:
        """
        Generate key

        :return: SymmetricKey
        """
        raise NotImplemented

    @abstractmethod
    def parse_symmetric_key(self, key: dict) -> Optional[SymmetricKey]:
        """
        Parse map object to key

        :param key: key info
        :return: SymmetricKey
        """
        raise NotImplemented
