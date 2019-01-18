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

"""
    Extends Crypto Keys
    ~~~~~~~~~~~~~~~~~~~

    AESKey        -> SymmetricKey
    RSAPublicKey  -> PublicKey
    RSAPrivateKey -> PrivateKey
"""

import numpy
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_PKCS1_v1_5

from mkm.utils import base64_encode, base64_decode
from mkm.crypto import SymmetricKey, symmetric_key_classes
from mkm.crypto import PublicKey, public_key_classes
from mkm.crypto import PrivateKey, private_key_classes


class AESKey(SymmetricKey):
    """ AES Key """

    data: bytes = None
    iv: bytes = None

    def __new__(cls, key: dict):
        # data
        if 'data' in key:
            # import key from data
            data = base64_decode(key['data'])
        else:
            raise ValueError('AES key data empty')
        # iv
        if 'iv' in key:
            iv = key['iv']
            iv = base64_decode(iv)
        else:
            iv = AES.block_size * chr(0).encode('utf-8')  # b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'
            key['iv'] = base64_encode(iv)
        # create key
        self = super().__new__(cls, key)
        self.data = data
        self.iv = iv
        return self

    @classmethod
    def generate(cls, key: dict) -> SymmetricKey:
        if 'size' in key:
            size = int(key['size'])
        else:
            size = 32
        # key data
        data = bytes(numpy.random.bytes(size))
        key['data'] = base64_encode(data)
        # initialized vector
        iv = bytes(numpy.random.bytes(AES.block_size))
        key['iv'] = base64_encode(iv)
        return AESKey(key)

    def encrypt(self, plaintext: bytes) -> bytes:
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        size = key.block_size
        pad = (size - len(plaintext) % size) * chr(0).encode('utf-8')
        return key.encrypt(plaintext + pad)

    def decrypt(self, data: bytes) -> bytes:
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        plaintext = key.decrypt(data)
        pad = plaintext[-1:]  # chr(0).encode('utf-8')
        return plaintext.rstrip(pad)


def unwrap_key_content(content, tag):
    # search tags
    begin = '-----BEGIN RSA ' + tag + ' KEY-----'
    end = '-----END RSA ' + tag + ' KEY-----'
    pos1 = content.find(begin)
    if pos1 < 0:
        begin = '-----BEGIN ' + tag + ' KEY-----'
        end = '-----END ' + tag + ' KEY-----'
        pos1 = content.find(begin)
    # unwrap tags
    if pos1 < 0:
        # tags not found
        pos2 = -1
    else:
        pos1 += len(begin)
        pos2 = content.find(end, pos1)
    if pos1 != -1 and pos2 != -1:
        content = content[pos1:pos2]
    # remove spaces
    content = content.replace('\r', '')
    content = content.replace('\n', '')
    content = content.replace('\t', '')
    content = content.replace(' ', '')
    return content


class RSAPublicKey(PublicKey):
    """ RSA Public Key """

    data: bytes = None
    key = None

    def __new__(cls, key: dict):
        # data
        if 'data' in key:
            data = base64_decode(unwrap_key_content(key['data'], 'PUBLIC'))
        else:
            raise ValueError('Public key data empty')
        # create key
        self = super().__new__(cls, key)
        self.data = data
        self.key = RSA.importKey(data)
        return self

    def encrypt(self, plaintext: bytes) -> bytes:
        cipher = Cipher_PKCS1_v1_5.new(self.key)
        return cipher.encrypt(plaintext)

    def verify(self, data: bytes, signature: bytes) -> bool:
        hash_obj = SHA256.new(data)
        verifier = Signature_PKCS1_v1_5.new(self.key)
        try:
            return verifier.verify(hash_obj, signature)
        except ValueError:
            # raise ValueError("Invalid signature")
            return False


class RSAPrivateKey(PrivateKey):
    """ RSA Private Key """

    data: bytes = None
    key = None

    def __new__(cls, key: dict):
        # data
        if 'data' in key:
            data = base64_decode(unwrap_key_content(key['data'], 'PRIVATE'))
        else:
            raise ValueError('RSA key data empty')
        # create key
        self = super().__new__(cls, key)
        self.data = data
        self.key = RSA.importKey(data)
        return self

    @classmethod
    def generate(cls, key: dict) -> PrivateKey:
        if 'keySizeInBits' in key:
            bits = int(key['keySizeInBits'])
        else:
            bits = 1024
        private_key = RSA.generate(bits)
        data = private_key.export_key()
        key['data'] = base64_encode(data)
        return RSAPrivateKey(key)

    def decrypt(self, data: bytes) -> bytes:
        cipher = Cipher_PKCS1_v1_5.new(self.key)
        sentinel = ''
        plaintext = cipher.decrypt(data, sentinel)
        if sentinel:
            print('error: ' + sentinel)
        return plaintext

    def sign(self, data: bytes) -> bytes:
        hash_obj = SHA256.new(data)
        signer = Signature_PKCS1_v1_5.new(self.key)
        return signer.sign(hash_obj)

    def publicKey(self) -> PublicKey:
        pk = self.key.publickey()
        data = pk.export_key()
        info = {
            'algorithm': 'RSA',
            'data': base64_encode(data),
        }
        return RSAPublicKey(info)


"""
    Key Classes Maps
"""

symmetric_key_classes['AES'] = AESKey
public_key_classes['RSA'] = RSAPublicKey
private_key_classes['RSA'] = RSAPrivateKey
