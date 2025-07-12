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

from .asymmetric import VerifyKey
from .helpers import CryptoExtensions


# noinspection PyAbstractClass
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
        helper = public_helper()
        return helper.parse_public_key(key)

    @classmethod
    def get_factory(cls, algorithm: str):  # -> Optional[PublicKeyFactory]:
        helper = public_helper()
        return helper.get_public_key_factory(algorithm=algorithm)

    @classmethod
    def set_factory(cls, algorithm: str, factory):
        helper = public_helper()
        helper.set_public_key_factory(algorithm=algorithm, factory=factory)


def public_helper():
    helper = CryptoExtensions.public_helper
    assert isinstance(helper, PublicKeyHelper), 'public helper error: %s' % helper
    return helper


class PublicKeyFactory(ABC):

    @abstractmethod
    def parse_public_key(self, key: Dict) -> Optional[PublicKey]:
        """
        Parse map object to key

        :param key: key info
        :return: PublicKey
        """
        raise NotImplemented


########################
#                      #
#   Plugins: Helpers   #
#                      #
########################


class PublicKeyHelper(ABC):

    @abstractmethod
    def set_public_key_factory(self, algorithm: str, factory: PublicKeyFactory):
        raise NotImplemented

    @abstractmethod
    def get_public_key_factory(self, algorithm: str) -> Optional[PublicKeyFactory]:
        raise NotImplemented

    @abstractmethod
    def parse_public_key(self, key: Any) -> Optional[PublicKey]:
        raise NotImplemented
