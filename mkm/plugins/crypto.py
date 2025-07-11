# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2024 Albert Moky
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

from ..types import Singleton

from ..crypto import SignKey, VerifyKey
from ..crypto import EncryptKey, DecryptKey

from ..crypto.symmetric import SymmetricKeyHelper
from ..crypto.private import PrivateKeyHelper
from ..crypto.public import PublicKeyHelper
from ..crypto.helpers import CryptoExtensions


# class GeneralCryptoHelper(SymmetricKeyHelper, PrivateKeyHelper, PublicKeyHelper, ABC):
class GeneralCryptoHelper(ABC):
    """ CryptographyKey GeneralFactory """

    """ sample data for checking keys """
    PROMISE = 'Moky loves May Lee forever!'.encode('utf-8')

    @classmethod
    def match_asymmetric_keys(cls, sign_key: SignKey, verify_key: VerifyKey) -> bool:
        """ verify with signature """
        signature = sign_key.sign(data=cls.PROMISE)
        return verify_key.verify(data=cls.PROMISE, signature=signature)

    @classmethod
    def match_symmetric_keys(cls, encrypt_key: EncryptKey, decrypt_key: DecryptKey) -> bool:
        """ check by encryption """
        extra = {}
        ciphertext = encrypt_key.encrypt(data=cls.PROMISE, extra=extra)
        plaintext = decrypt_key.decrypt(data=ciphertext, params=extra)
        return plaintext == cls.PROMISE

    #
    #   Algorithm
    #

    @abstractmethod
    def get_key_algorithm(self, key: Dict, default: Optional[str] = None) -> Optional[str]:
        raise NotImplemented


@Singleton
class SharedCryptoExtensions:
    """ CryptographyKey FactoryManager """

    def __init__(self):
        super().__init__()
        self.__helper: Optional[GeneralCryptoHelper] = None

    @property
    def helper(self) -> Optional[GeneralCryptoHelper]:
        return self.__helper

    @helper.setter
    def helper(self, helper: GeneralCryptoHelper):
        self.__helper = helper

    #
    #   Symmetric Key
    #

    @property
    def symmetric_helper(self) -> Optional[SymmetricKeyHelper]:
        return CryptoExtensions.symmetric_helper

    @symmetric_helper.setter
    def symmetric_helper(self, helper: SymmetricKeyHelper):
        CryptoExtensions.symmetric_helper = helper

    #
    #   Private Key
    #

    @property
    def private_helper(self) -> Optional[PrivateKeyHelper]:
        return CryptoExtensions.private_helper

    @private_helper.setter
    def private_helper(self, helper: PrivateKeyHelper):
        CryptoExtensions.private_helper = helper

    #
    #   Public Key
    #

    @property
    def public_helper(self) -> Optional[PublicKeyHelper]:
        return CryptoExtensions.public_helper

    @public_helper.setter
    def public_helper(self, helper: PublicKeyHelper):
        CryptoExtensions.public_helper = helper
