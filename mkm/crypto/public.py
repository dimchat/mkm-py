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

from ..types import Wrapper
from .factories import Factories
from .cryptography import key_algorithm
from .asymmetric import VerifyKey


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

    #
    #  Factory method
    #

    @classmethod
    def parse(cls, key: Any):  # -> Optional[PublicKey]:
        if key is None:
            return None
        elif isinstance(key, PublicKey):
            return key
        info = Wrapper.get_dictionary(key)
        # assert info is not None, 'key error: %s' % key
        algorithm = key_algorithm(key=info)
        factory = cls.factory(algorithm=algorithm)
        if factory is None:
            factory = cls.factory(algorithm='*')  # unknown
        # assert isinstance(factory, PublicKeyFactory), 'key algorithm not support: %s' % algorithm
        return factory.parse_public_key(key=info)

    @classmethod
    def factory(cls, algorithm: str):  # -> Optional[PublicKeyFactory]:
        return Factories.public_key_factories.get(algorithm)

    @classmethod
    def register(cls, algorithm: str, factory):
        Factories.public_key_factories[algorithm] = factory


class PublicKeyFactory(ABC):

    @abstractmethod
    def parse_public_key(self, key: Dict[str, Any]) -> Optional[PublicKey]:
        """
        Parse map object to key

        :param key: key info
        :return: PublicKey
        """
        raise NotImplemented
