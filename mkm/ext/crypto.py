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

from ..crypto import SignKey, VerifyKey
from ..crypto import EncryptKey, DecryptKey
from ..crypto.cryptography import CryptoExtensions


# -----------------------------------------------------------------------------
#  Crypto Extensions
# -----------------------------------------------------------------------------


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
        ciphertext = encrypt_key.encrypt(cls.PROMISE, extra=extra)
        plaintext = decrypt_key.decrypt(ciphertext, params=extra)
        return plaintext == cls.PROMISE

    #
    #   Algorithm
    #

    @abstractmethod
    def get_key_algorithm(self, key: Dict, default: Optional[str] = None) -> Optional[str]:
        raise NotImplemented


class _CryptoExt:
    _crypto_helper: Optional[GeneralCryptoHelper] = None

    @property
    def crypto_helper(self) -> Optional[GeneralCryptoHelper]:
        return _CryptoExt._crypto_helper

    @crypto_helper.setter
    def crypto_helper(self, helper: GeneralCryptoHelper):
        _CryptoExt._crypto_helper = helper


CryptoExtensions.helper = _CryptoExt.crypto_helper
