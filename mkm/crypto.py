#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Crypto
    ~~~~~~

    Crypto Keys
"""

import numpy
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_PKCS1_v1_5

from mkm.utils import *


class SymmetricKey(dict):
    """ Symmetric Key """

    @classmethod
    def new(cls, key: object):
        if isinstance(key, SymmetricKey):
            return key
        elif isinstance(key, dict):
            algorithm = key['algorithm']
            if algorithm == 'AES':
                return AESKey.new(key)

    def encrypt(self, plaintext: bytes) -> bytes:
        pass

    def decrypt(self, data: bytes) -> bytes:
        pass


class AESKey(SymmetricKey):
    """ AES """

    data: bytes = None
    iv: bytes = None

    @classmethod
    def new(cls, key: dict) -> SymmetricKey:
        # data
        if 'data' in key:
            # import key from data
            data = base64_decode(key['data'])
        else:
            # generate key
            if 'size' in key:
                size = int(key['size'])
            else:
                size = 32
            data = bytes(numpy.random.bytes(size))
            key['data'] = base64_encode(data)
        # iv
        if 'iv' in key:
            iv = key['iv']
            iv = base64_decode(iv)
            # self.key = AES.new(data, AES.MODE_CBC, iv)
        else:
            iv = b'0000000000000000'
        # create key
        self = AESKey(key)
        self.data = data
        self.iv = iv
        return self

    def encrypt(self, plaintext: bytes) -> bytes:
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        size = key.block_size
        pad = (size - len(plaintext) % size) * chr(0)
        return key.encrypt(plaintext + pad.encode('utf-8'))

    def decrypt(self, data: bytes) -> bytes:
        key = AES.new(self.data, AES.MODE_CBC, self.iv)
        plaintext = key.decrypt(data)
        pad = chr(0).encode('utf-8')
        return plaintext.rstrip(pad)


class PublicKey(dict):
    """ Public Key """

    @classmethod
    def new(cls, key: object):
        if isinstance(key, PublicKey):
            return key
        elif isinstance(key, dict):
            algorithm = key['algorithm']
            if algorithm == 'RSA':
                return RSAPublicKey.new(key)

    def encrypt(self, plaintext: bytes) -> bytes:
        pass

    def verify(self, data: bytes, signature: bytes) -> bool:
        pass

    def match(self, private_key) -> bool:
        promise = 'Moky loves May Lee forever!'
        data = promise.encode('utf-8')
        signature = private_key.sign(data)
        return self.verify(data, signature)


class RSAPublicKey(PublicKey):
    """ RSA Public Key """

    data: bytes = None
    key = None

    @classmethod
    def new(cls, key: dict) -> PublicKey:
        # data
        if 'data' in key:
            data = base64_decode(key['data'])
        else:
            raise ValueError('Public key data empty')
        # create key
        self = RSAPublicKey(key)
        self.data = data
        self.key = RSA.importKey(data)
        return self

    def encrypt(self, plaintext: bytes) -> bytes:
        """

        :Raises ValueError:
            If the RSA key length is not sufficiently long to deal with the given
            message.

        """
        cipher = Cipher_PKCS1_v1_5.new(self.key)
        return cipher.encrypt(plaintext)

    def verify(self, data: bytes, signature: bytes) -> bool:
        """

        :raise ValueError: if the signature is not valid.

        """
        hash_obj = SHA256.new(data)
        verifier = Signature_PKCS1_v1_5.new(self.key)
        try:
            verifier.verify(hash_obj, signature)
        except ValueError:
            # raise ValueError("Invalid signature")
            return False

        return True


class PrivateKey(dict):
    """ Private Key """

    @classmethod
    def new(cls, key: object):
        if isinstance(key, PublicKey):
            return key
        elif isinstance(key, dict):
            algorithm = key['algorithm']
            if algorithm == 'RSA':
                return RSAPrivateKey.new(key)

    def decrypt(self, data: bytes) -> bytes:
        pass

    def sign(self, data: bytes) -> bytes:
        pass

    def publicKey(self) -> PublicKey:
        pass


class RSAPrivateKey(PrivateKey):
    """ RSA Private Key """

    data: bytes = None
    key = None

    @classmethod
    def new(cls, key: dict) -> PrivateKey:
        # data
        if 'data' in key:
            data = base64_decode(key['data'])
        else:
            # generate key
            if 'keySizeInBits' in key:
                bits = int(key['keySizeInBits'])
            else:
                bits = 1024
            sk = RSA.generate(bits)
            data = sk.export_key()
            key = {
                'algorithm': 'RSA',
                'data': base64_encode(data),
                'keySizeInBits': bits,
            }
        # create key
        self = RSAPrivateKey(key)
        self.data = data
        self.key = RSA.importKey(data)
        return self

    def decrypt(self, data: bytes) -> bytes:
        """

        :Raises ValueError:
            If the data length is incorrect
        :Raises TypeError:
            If the RSA key has no private half (i.e. it cannot be used for decyption).

]       """
        cipher = Cipher_PKCS1_v1_5.new(self.key)
        sentinel = 'whenever'
        plaintext = cipher.decrypt(data, sentinel)
        if sentinel:
            print('error: ' + sentinel)
        return plaintext

    def sign(self, data: bytes) -> bytes:
        """

        :raise ValueError: if the RSA key is not long enough for the given hash algorithm.
        :raise TypeError: if the RSA key has no private half.

        """
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
        return RSAPublicKey.new(info)
