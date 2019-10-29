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

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_PKCS1_v1_5

from .asymmetric import PublicKey, PrivateKey


class RSAPublicKey(PublicKey):
    """ RSA Public Key """

    def __new__(cls, key: dict):
        """
        Create RSA public key

        :param key: key info
        :return: RSAPublicKey object
        """
        if key is None:
            return None
        elif cls is RSAPublicKey:
            if isinstance(key, RSAPublicKey):
                # return RSAPublicKey object directly
                return key
        # new RSAPublicKey(dict)
        return super().__new__(cls, key)

    def __init__(self, key: dict):
        if self is key:
            # no need to init again
            return
        super().__init__(key)
        # data in 'PEM' format
        data = key['data']
        self.key = RSA.importKey(data)
        self.data = self.key.exportKey(format='DER')

    # noinspection PyTypeChecker
    def encrypt(self, data: bytes) -> bytes:
        cipher = Cipher_PKCS1_v1_5.new(self.key)
        return cipher.encrypt(data)

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

    def __new__(cls, key: dict):
        """
        Create RSA private key

        :param key: key info
        :return: RSAPrivateKey object
        """
        if key is None:
            return None
        elif cls is RSAPrivateKey:
            if isinstance(key, RSAPrivateKey):
                # return RSAPrivateKey object directly
                return key
        # new RSAPrivateKey(dict)
        return super().__new__(cls, key)

    def __init__(self, key: dict):
        if self is key:
            # no need to init again
            return
        super().__init__(key)
        # data in 'PEM' format
        data: str = key.get('data')
        if data is None:
            # generate private key data
            private_key = RSA.generate(self.size)
            data: bytes = private_key.exportKey()
            self['data'] = data.decode('utf-8')
            self['mode'] = 'ECB'
            self['padding'] = 'PKCS1'
            self['digest'] = 'SHA256'
        else:
            tag1 = '-----BEGIN RSA PRIVATE KEY-----'
            tag2 = '-----END RSA PRIVATE KEY-----'
            pos2 = data.find(tag2)
            if pos2 > 0:
                pos1 = data.find(tag1)
                data = data[pos1: pos2 + len(tag2)]
        # create key
        self.key = RSA.importKey(data)

    @property
    def size(self):
        bits = self.get('keySizeInBits')
        if bits is None:
            return 1024
        else:
            return int(bits)

    @property
    def public_key(self) -> PublicKey:
        pk = self.key.publickey()
        data = pk.exportKey()
        info = {
            'algorithm': PublicKey.RSA,
            'data': data.decode('utf-8'),
            'mode': 'ECB',
            'padding': 'PKCS1',
            'digest': 'SHA256'
        }
        return RSAPublicKey(info)

    # noinspection PyTypeChecker
    def decrypt(self, data: bytes) -> Optional[bytes]:
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


# register public key class with algorithm
PublicKey.register(algorithm=PublicKey.RSA, key_class=RSAPublicKey)             # default
PublicKey.register(algorithm='SHA256withRSA', key_class=RSAPublicKey)
PublicKey.register(algorithm='RSA/ECB/PKCS1Padding', key_class=RSAPublicKey)

# register private key class with algorithm
PrivateKey.register(algorithm=PrivateKey.RSA, key_class=RSAPrivateKey)          # default
PrivateKey.register(algorithm='SHA256withRSA', key_class=RSAPrivateKey)
PrivateKey.register(algorithm='RSA/ECB/PKCS1Padding', key_class=RSAPrivateKey)
