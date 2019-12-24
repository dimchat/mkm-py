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
from typing import Union

from .cryptography import CryptographyKey, VerifyKey, SignKey, EncryptKey


class AsymmetricKey(CryptographyKey):

    RSA = 'RSA'
    ECC = 'ECC'

    @property
    @abstractmethod
    def size(self) -> int:
        data = self.data
        if data is not None:
            return len(data)


class PublicKey(AsymmetricKey, VerifyKey):
    """This class is used to en/decrypt symmetric key or sign/verify signature with message data

        Asymmetric Cryptography Public Key
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        key data format: {
            algorithm : "RSA", // "ECC", ...
            data      : "{BASE64_ENCODE}",
            ...
        }
    """

    # noinspection PyTypeChecker
    def __new__(cls, key: dict):
        """
        Create public key

        :param key: key info with algorithm='RSA'
        :return: public key
        """
        if key is None:
            return None
        assert cls is PublicKey, 'call PublicKey() directly'
        if isinstance(key, PublicKey):
            # return PublicKey object directly
            return key
        # get class by algorithm name
        clazz = cls.key_class(algorithm=key['algorithm'])
        if clazz is not None:
            return clazz.__new__(clazz, key)
        else:
            raise ModuleNotFoundError('Invalid key algorithm: %s' % key)

    @property
    @abstractmethod
    def size(self) -> int:
        return super().size

    def match(self, private_key) -> bool:
        if not isinstance(private_key, dict):
            return False
        private_key = PrivateKey(private_key)
        # 1. if the SK has the same public key, return true
        if private_key.public_key == self:
            return True
        # 2. try to verify the SK's signature
        promise = 'Moky loves May Lee forever!'.encode('utf-8')
        signature = private_key.sign(promise)
        return self.verify(promise, signature)

    #
    #   Runtime
    #
    __key_classes = {}  # class map

    @classmethod
    def register(cls, algorithm: str, key_class=None) -> bool:
        """
        Register public key class with algorithm

        :param algorithm: key algorithm
        :param key_class: if key class is None, then remove with algorithm
        :return: False on error
        """
        if key_class is None:
            cls.__key_classes.pop(algorithm, None)
        elif issubclass(key_class, PublicKey):
            cls.__key_classes[algorithm] = key_class
        else:
            raise TypeError('%s must be subclass of PublicKey' % key_class)
        return True

    @classmethod
    def key_class(cls, algorithm: str):
        """
        Get public key class with algorithm

        :param algorithm: key algorithm
        :return: public key class
        """
        return cls.__key_classes.get(algorithm)


class PrivateKey(AsymmetricKey, SignKey):
    """This class is used to decrypt symmetric key or sign message data

        Asymmetric Cryptography Private Key
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        key data format: {
            algorithm : "RSA", // "ECC", ...
            data      : "{BASE64_ENCODE}",
            ...
        }
    """

    # noinspection PyTypeChecker
    def __new__(cls, key: dict):
        """
        Create private key

        :param key: key info with algorithm='RSA'
        :return: private key
        """
        if key is None:
            return None
        assert cls is PrivateKey, 'call PrivateKey() directly'
        if isinstance(key, PrivateKey):
            # return PrivateKey object directly
            return key
        # get class by algorithm name
        clazz = cls.key_class(algorithm=key['algorithm'])
        if clazz is not None:
            return clazz.__new__(clazz, key)
        else:
            raise ModuleNotFoundError('Invalid key algorithm: %s' % key)

    def __eq__(self, other) -> bool:
        if not isinstance(other, dict):
            return False
        if super().__eq__(other):
            return True
        pk = self.public_key
        if pk is not None:
            sk = PrivateKey(other)
            return pk.match(private_key=sk)

    @property
    @abstractmethod
    def public_key(self) -> Union[PublicKey, EncryptKey]:
        """
        Get public key from private key

        :return: public key paired to this private key
        """
        raise NotImplemented

    #
    #   Runtime
    #
    __key_classes = {}  # class map

    @classmethod
    def register(cls, algorithm: str, key_class=None) -> bool:
        """
        Register private key class with algorithm

        :param algorithm: key algorithm
        :param key_class: if key class is None, then remove with algorithm
        :return: False on error
        """
        if key_class is None:
            cls.__key_classes.pop(algorithm, None)
        elif issubclass(key_class, PrivateKey):
            cls.__key_classes[algorithm] = key_class
        else:
            raise TypeError('%s must be subclass of PrivateKey' % key_class)
        return True

    @classmethod
    def key_class(cls, algorithm: str):
        """
        Get private key class with algorithm

        :param algorithm: key algorithm
        :return: private key class
        """
        return cls.__key_classes.get(algorithm)
