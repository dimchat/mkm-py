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
from typing import Optional

from .types import SOMap
from .cryptography import key_algorithm
from .asymmetric import VerifyKey, SignKey, asymmetric_keys_match


class PublicKey(VerifyKey, ABC):
    """This class is used to en/decrypt symmetric key or sign/verify signature with message data

        Asymmetric Cryptography Public Key
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        key data format: {
            algorithm : "RSA", // "ECC", ...
            data      : "{BASE64_ENCODE}",
            ...
        }
    """

    def match(self, private_key: SignKey):
        return asymmetric_keys_match(private_key=private_key, public_key=self)

    #
    #  Factory method
    #
    @classmethod
    def parse(cls, key: dict):  # -> Optional[PublicKey]:
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
        return factory.parse_public_key(key=key)

    @classmethod
    def factory(cls, algorithm: str):  # -> Optional[PublicKeyFactory]:
        return s_factories.get(algorithm)

    @classmethod
    def register(cls, algorithm: str, factory):
        s_factories[algorithm] = factory


"""
    Key Factory
    ~~~~~~~~~~~
"""
s_factories = {}


class PublicKeyFactory:

    @abstractmethod
    def parse_public_key(self, key: dict) -> Optional[PublicKey]:
        """
        Parse map object to key

        :param key: key info
        :return: PublicKey
        """
        raise NotImplemented
