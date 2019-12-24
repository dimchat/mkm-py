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

from .cryptography import EncryptKey, DecryptKey


class SymmetricKey(EncryptKey, DecryptKey):
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

    # noinspection PyTypeChecker
    def __new__(cls, key: dict):
        """
        Create symmetric key

        :param key: key info (with algorithm='AES')
        :return: symmetric key
        """
        if key is None:
            return None
        assert cls is SymmetricKey, 'call SymmetricKey() directly'
        if isinstance(key, SymmetricKey):
            # return SymmetricKey object directly
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
        other = SymmetricKey(other)
        promise = 'Moky loves May Lee forever!'.encode('utf-8')
        return self.decrypt(other.encrypt(promise)) == promise

    @property
    @abstractmethod
    def size(self) -> int:
        data = self.data
        if data is not None:
            return len(data)

    #
    #   Runtime
    #
    __key_classes = {}  # class map

    @classmethod
    def register(cls, algorithm: str, key_class=None) -> bool:
        """
        Register symmetric key class with algorithm

        :param algorithm: key algorithm
        :param key_class: if key class is None, then remove with algorithm
        :return: False on error
        """
        if key_class is None:
            cls.__key_classes.pop(algorithm, None)
        elif issubclass(key_class, SymmetricKey):
            cls.__key_classes[algorithm] = key_class
        else:
            raise TypeError('%s must be subclass of SymmetricKey' % key_class)
        return True

    @classmethod
    def key_class(cls, algorithm: str):
        """
        Get symmetric key class with algorithm

        :param algorithm: key algorithm
        :return: symmetric key class
        """
        return cls.__key_classes.get(algorithm)
