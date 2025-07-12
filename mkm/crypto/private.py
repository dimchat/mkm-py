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

from .asymmetric import SignKey
from .public import PublicKey
from .helpers import CryptoExtensions


class PrivateKey(SignKey, ABC):
    """This class is used to decrypt symmetric key or sign message data

        Asymmetric Cryptography Private Key
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        key data format: {
            algorithm : "RSA", // "ECC", ...
            data      : "{BASE64_ENCODE}",
            ...
        }
    """

    @property
    @abstractmethod
    def public_key(self) -> PublicKey:
        """
        Get public key from private key

        :return: public key paired to this private key
        """
        raise NotImplemented

    #
    #  Factory methods
    #

    @classmethod
    def generate(cls, algorithm: str):  # -> Optional[PrivateKey]:
        helper = private_helper()
        return helper.generate_private_key(algorithm=algorithm)

    @classmethod
    def parse(cls, key: Any):  # -> Optional[PrivateKey]:
        helper = private_helper()
        return helper.parse_private_key(key)

    @classmethod
    def get_factory(cls, algorithm: str):  # -> Optional[PrivateKeyFactory]:
        helper = private_helper()
        return helper.get_private_key_factory(algorithm=algorithm)

    @classmethod
    def set_factory(cls, algorithm: str, factory):
        helper = private_helper()
        helper.set_private_key_factory(algorithm=algorithm, factory=factory)


def private_helper():
    helper = CryptoExtensions.private_helper
    assert isinstance(helper, PrivateKeyHelper), 'private helper error: %s' % helper
    return helper


class PrivateKeyFactory(ABC):
    """ Key Factory """

    @abstractmethod
    def generate_private_key(self) -> PrivateKey:
        """
        Generate key

        :return: PrivateKey
        """
        raise NotImplemented

    @abstractmethod
    def parse_private_key(self, key: Dict) -> Optional[PrivateKey]:
        """
        Parse map object to key

        :param key: key info
        :return: PrivateKey
        """
        raise NotImplemented


########################
#                      #
#   Plugins: Helpers   #
#                      #
########################


class PrivateKeyHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_private_key_factory(self, algorithm: str, factory: PrivateKeyFactory):
        raise NotImplemented

    @abstractmethod
    def get_private_key_factory(self, algorithm: str) -> Optional[PrivateKeyFactory]:
        raise NotImplemented

    @abstractmethod
    def generate_private_key(self, algorithm: str) -> Optional[PrivateKey]:
        raise NotImplemented

    @abstractmethod
    def parse_private_key(self, key: Any) -> Optional[PrivateKey]:
        raise NotImplemented
