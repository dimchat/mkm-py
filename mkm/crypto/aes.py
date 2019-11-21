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

from typing import Optional

import numpy
from Crypto.Cipher import AES

from .symmetric import SymmetricKey
from .utils import base64_encode, base64_decode


def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    assert data is not None, 'data cannot be None'
    amount = block_size - len(data) % block_size
    if amount == 0:
        amount = block_size
    pad = chr(amount).encode('utf-8')
    return data + pad * amount


def pkcs7_unpad(data: bytes) -> bytes:
    assert data is not None and len(data) > 0, 'data empty'
    amount = data[-1]
    assert len(data) >= amount
    return data[:-amount]


class AESKey(dict, SymmetricKey):
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
        self.__data = data
        self.iv = iv

    @property
    def data(self) -> bytes:
        return self.__data

    @property
    def size(self) -> int:
        size = self.get('size')
        if size is None:
            return 32  # AES-256
        else:
            return int(size)

    def encrypt(self, data: bytes) -> bytes:
        data = pkcs7_pad(data=data, block_size=AES.block_size)
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        return key.encrypt(data)

    def decrypt(self, data: bytes) -> Optional[bytes]:
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        plaintext = key.decrypt(data)
        return pkcs7_unpad(data=plaintext)


# register symmetric key class with algorithm
SymmetricKey.register(algorithm=SymmetricKey.AES, key_class=AESKey)        # default
SymmetricKey.register(algorithm='AES/CBC/PKCS7Padding', key_class=AESKey)
