# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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

from typing import Optional, Any, Dict

from ..types import Converter
from ..types import Wrapper

from .cryptography import EncryptKey, DecryptKey
from .symmetric import SymmetricKey, SymmetricKeyFactory
from .asymmetric import SignKey, VerifyKey
from .public import PublicKey, PublicKeyFactory
from .private import PrivateKey, PrivateKeyFactory


class CryptographyKeyGeneralFactory:

    # sample data for checking keys
    promise = 'Moky loves May Lee forever!'.encode('utf-8')

    def __init__(self):
        super().__init__()
        # str(algorithm) -> SymmetricKey.Factory
        self.__symmetric_key_factories: Dict[str, SymmetricKeyFactory] = {}
        # str(algorithm) -> PublicKey.Factory
        self.__public_key_factories: Dict[str, PublicKeyFactory] = {}
        # str(algorithm) -> PrivateKey.Factory
        self.__private_key_factories: Dict[str, PrivateKeyFactory] = {}

    def keys_match(self, encrypt_key: EncryptKey, decrypt_key: DecryptKey) -> bool:
        """ check by encryption """
        extra = {}
        ciphertext = encrypt_key.encrypt(data=self.promise, extra=extra)
        plaintext = decrypt_key.decrypt(data=ciphertext, params=extra)
        return plaintext == self.promise

    def asymmetric_keys_match(self, sign_key: SignKey, verify_key: VerifyKey) -> bool:
        """ verify with signature """
        signature = sign_key.sign(data=self.promise)
        return verify_key.verify(data=self.promise, signature=signature)

    # noinspection PyMethodMayBeStatic
    def get_key_algorithm(self, key: Dict[str, Any], default: Optional[str]) -> Optional[str]:
        """ get key algorithm name """
        value = key.get('algorithm')
        return Converter.get_str(value=value, default=default)

    #
    #   SymmetricKey
    #

    def set_symmetric_key_factory(self, algorithm: str, factory: SymmetricKeyFactory):
        self.__symmetric_key_factories[algorithm] = factory

    def get_symmetric_key_factory(self, algorithm: str) -> Optional[SymmetricKeyFactory]:
        return self.__symmetric_key_factories.get(algorithm)

    def generate_symmetric_key(self, algorithm: str) -> Optional[SymmetricKey]:
        factory = self.get_symmetric_key_factory(algorithm=algorithm)
        # assert factory is not None, 'key algorithm not support: %s' % algorithm
        return factory.generate_symmetric_key()

    def parse_symmetric_key(self, key: Any) -> Optional[SymmetricKey]:
        if key is None:
            return None
        if isinstance(key, SymmetricKey):
            return key
        info = Wrapper.get_dict(key)
        if info is None:
            # assert False, 'key error: %s' % key
            return None
        algorithm = self.get_key_algorithm(info, default='*')
        factory = self.get_symmetric_key_factory(algorithm=algorithm)
        if factory is None and algorithm != '*':
            factory = self.get_symmetric_key_factory(algorithm='*')  # unknown
        # if factory is None:
        #     # assert False, 'key algorithm not support: %s' % algorithm
        #     return None
        return factory.parse_symmetric_key(info)

    #
    #   PublicKey
    #

    def set_public_key_factory(self, algorithm: str, factory: PublicKeyFactory):
        self.__public_key_factories[algorithm] = factory

    def get_public_key_factory(self, algorithm: str) -> Optional[PublicKeyFactory]:
        return self.__public_key_factories.get(algorithm)

    def parse_public_key(self, key: Any) -> Optional[PublicKey]:
        if key is None:
            return None
        elif isinstance(key, PublicKey):
            return key
        info = Wrapper.get_dict(key)
        if info is None:
            # assert False, 'key error: %s' % key
            return None
        algorithm = self.get_key_algorithm(info, default='*')
        factory = self.get_public_key_factory(algorithm=algorithm)
        if factory is None and algorithm != '*':
            factory = self.get_public_key_factory(algorithm='*')  # unknown
        # if factory is None:
        #     # assert False, 'key algorithm not support: %s' % algorithm
        #     return None
        return factory.parse_public_key(info)

    #
    #   PrivateKey
    #

    def set_private_key_factory(self, algorithm: str, factory: PrivateKeyFactory):
        self.__private_key_factories[algorithm] = factory

    def get_private_key_factory(self, algorithm: str) -> Optional[PrivateKeyFactory]:
        return self.__private_key_factories.get(algorithm)

    def generate_private_key(self, algorithm: str) -> Optional[PrivateKey]:
        factory = self.get_private_key_factory(algorithm=algorithm)
        # assert factory is not None, 'key algorithm not support: %s' % algorithm
        return factory.generate_private_key()

    def parse_private_key(self, key: Any) -> Optional[PrivateKey]:
        if key is None:
            return None
        elif isinstance(key, PrivateKey):
            return key
        info = Wrapper.get_dict(key)
        if info is None:
            # assert False, 'key error: %s' % key
            return None
        algorithm = self.get_key_algorithm(info, default='*')
        factory = self.get_private_key_factory(algorithm=algorithm)
        if factory is None and algorithm != '*':
            factory = self.get_private_key_factory(algorithm='*')  # unknown
        # if factory is None:
        #     # assert False, 'key algorithm not support: %s' % algorithm
        #     return None
        return factory.parse_private_key(info)


# Singleton
class CryptographyKeyFactoryManager:

    general_factory = CryptographyKeyGeneralFactory()
