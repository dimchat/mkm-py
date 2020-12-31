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

from abc import abstractmethod
from typing import Optional

from .types import SOMap
from .cryptography import key_algorithm
from .asymmetric import SignKey, asymmetric_keys_match
from .public import PublicKey


class PrivateKey(SignKey):
    """This class is used to decrypt symmetric key or sign message data

        Asymmetric Cryptography Private Key
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        key data format: {
            algorithm : "RSA", // "ECC", ...
            data      : "{BASE64_ENCODE}",
            ...
        }
    """

    def __eq__(self, other) -> bool:
        if super().__eq__(other):
            return True
        if isinstance(other, SignKey):
            return asymmetric_keys_match(private_key=other, public_key=self.public_key)

    @property
    @abstractmethod
    def public_key(self) -> Optional[PublicKey]:
        """
        Get public key from private key

        :return: public key paired to this private key
        """
        raise NotImplemented

    #
    #   Factory methods
    #
    @classmethod
    def generate(cls, algorithm: str):  # -> Optional[PrivateKey]:
        factory = cls.factory(algorithm=algorithm)
        assert factory is not None, 'key algorithm not found: %s' % algorithm
        return factory.generate_private_key()

    @classmethod
    def parse(cls, key: dict):  # -> Optional[PrivateKey]:
        if key is None:
            return None
        elif isinstance(key, cls):
            return key
        elif isinstance(key, SOMap):
            key = key.dictionary
        algorithm = key_algorithm(key=key)
        assert algorithm is not None, 'failed to get algorithm from key: %s' % key
        factory = cls.factory(algorithm=algorithm)
        if factory is None:
            factory = cls.factory(algorithm='*')  # unknown
            assert factory is not None, 'cannot parse key: %s' % key
        return factory.parse_private_key(key=key)

    @classmethod
    def factory(cls, algorithm: str):  # -> Optional[PrivateKeyFactory]:
        return s_factories.get(algorithm)

    @classmethod
    def register(cls, algorithm: str, factory):
        s_factories[algorithm] = factory


"""
    Key Factory
    ~~~~~~~~~~~
"""
s_factories = {}


class PrivateKeyFactory:

    @abstractmethod
    def generate_private_key(self) -> Optional[PrivateKey]:
        """
        Generate key

        :return: PrivateKey
        """
        raise NotImplemented

    @abstractmethod
    def parse_private_key(self, key: dict) -> Optional[PrivateKey]:
        """
        Parse map object to key

        :param key: key info
        :return: PrivateKey
        """
        raise NotImplemented
