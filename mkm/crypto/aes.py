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

import numpy
from Crypto.Cipher import AES

from .symmetric import SymmetricKey, symmetric_key_classes
from .utils import base64_encode, base64_decode


class AESKey(SymmetricKey):
    """ AES Key """

    def __new__(cls, key: dict):
        """
        Create AES key

        :param key: key info
        :return: AESKey object
        """
        if key is None:
            return None
        elif cls is AESKey:
            if isinstance(key, AESKey):
                # return AESKey object directly
                return key
        # new AESKey(dict)
        return super().__new__(cls, key)

    def __init__(self, key: dict):
        if self is key:
            # no need to init again
            return
        super().__init__(key)
        # key data
        data = self.get('data')
        if data is None:
            # generate data and iv
            data = bytes(numpy.random.bytes(self.size))
            self['data'] = base64_encode(data)
            iv = bytes(numpy.random.bytes(AES.block_size))
            self['iv'] = base64_encode(iv)
            # self['mode'] = 'CBC'
            # self['padding'] = 'PKCS7'
        else:
            data = base64_decode(data)
        # initialization vector
        iv = self.get('iv')
        if iv is None:
            # iv = b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'
            iv = AES.block_size * chr(0).encode('utf-8')
            self['iv'] = base64_encode(iv)
        else:
            iv = base64_decode(iv)
        self.data = data
        self.iv = iv

    @property
    def size(self) -> int:
        size = self.get('size')
        if size is None:
            return 32
        else:
            return int(size)

    @staticmethod
    def __pad(data: bytes) -> bytes:
        block_size = AES.block_size
        amount = block_size - len(data) % block_size
        if amount == 0:
            amount = block_size
        pad = chr(amount).encode('utf-8')
        return data + pad * amount

    @staticmethod
    def __unpad(data: bytes) -> bytes:
        amount = data[-1]
        return data[:-amount]

    def encrypt(self, data: bytes) -> bytes:
        data = self.__pad(data)
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        return key.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        plaintext = key.decrypt(data)
        return self.__unpad(plaintext)


"""
    Key Classes Maps
"""

# AES Key
symmetric_key_classes[SymmetricKey.AES] = AESKey        # default
symmetric_key_classes['AES/CBC/PKCS7Padding'] = AESKey
