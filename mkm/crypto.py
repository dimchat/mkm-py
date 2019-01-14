#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Crypto
    ~~~~~~

    Crypto Keys: SymmetricKey(AES, ...), PrivateKey(RSA, ...), PublicKey(RSA, ...)
"""

import numpy
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_PKCS1_v1_5

from mkm.utils import base64_encode, base64_decode


class SymmetricKey(dict):
    """
        This class is used to encrypt or decrypt message data
    """

    def __new__(cls, key: dict):
        """

        :param key: key info with algorithm='AES'
        :return: symmetric key
        """
        if cls is not SymmetricKey:
            # subclass
            if issubclass(cls, SymmetricKey):
                return super(SymmetricKey, cls).__new__(cls, key)
            else:
                raise TypeError('Not subclass of SymmetricKey')
        elif isinstance(key, SymmetricKey):
            # key object
            return key
        elif isinstance(key, dict):
            # get class by algorithm name
            algorithm = key['algorithm']
            clazz = symmetric_key_classes[algorithm]
            if issubclass(clazz, SymmetricKey):
                return clazz(key)
            else:
                raise ModuleNotFoundError('Invalid algorithm: ' + algorithm)
        else:
            raise AssertionError('Invalid symmetric key')

    def encrypt(self, plaintext: bytes) -> bytes:
        pass

    def decrypt(self, data: bytes) -> bytes:
        pass

    @classmethod
    def generate(cls, key: dict):
        # get class by algorithm name
        algorithm = key['algorithm']
        clazz = symmetric_key_classes[algorithm]
        if issubclass(clazz, SymmetricKey):
            return clazz.generate(key)
        else:
            raise ModuleNotFoundError('Invalid algorithm: ' + algorithm)


class PublicKey(dict):
    """
        This class is used to encrypt symmetric key or verify signature with message data
    """

    def __new__(cls, key: dict):
        """

        :param key: key info with algorithm='RSA'
        :return: public key
        """
        if cls is not PublicKey:
            # subclass
            if issubclass(cls, PublicKey):
                return super(PublicKey, cls).__new__(cls, key)
            else:
                raise TypeError('Not subclass of PublicKey')
        elif isinstance(key, PublicKey):
            # key object
            return key
        elif isinstance(key, dict):
            # get class by algorithm name
            algorithm = key['algorithm']
            clazz = public_key_classes[algorithm]
            if issubclass(clazz, PublicKey):
                return clazz(key)
            else:
                raise ModuleNotFoundError('Invalid algorithm: ' + algorithm)
        else:
            raise ValueError('Invalid public key')

    def encrypt(self, plaintext: bytes) -> bytes:
        pass

    def verify(self, data: bytes, signature: bytes) -> bool:
        pass

    def match(self, private_key) -> bool:
        promise = 'Moky loves May Lee forever!'
        data = promise.encode('utf-8')
        signature = private_key.sign(data)
        return self.verify(data, signature)


class PrivateKey(dict):
    """
        This class is used to decrypt symmetric key or sign message data
    """

    def __new__(cls, key: dict):
        """

        :param key: key info with algorithm='RSA'
        :return: private key
        """
        if cls is not PrivateKey:
            # subclass
            if issubclass(cls, PrivateKey):
                return super(PrivateKey, cls).__new__(cls, key)
            else:
                raise TypeError('Not subclass of PrivateKey')
        elif isinstance(key, PublicKey):
            # key object
            return key
        elif isinstance(key, dict):
            # get class by algorithm name
            algorithm = key['algorithm']
            clazz = private_key_classes[algorithm]
            if issubclass(clazz, PrivateKey):
                return clazz(key)
            else:
                raise ModuleNotFoundError('Invalid algorithm: ' + algorithm)
        else:
            raise ValueError('Invalid private key')

    def decrypt(self, data: bytes) -> bytes:
        pass

    def sign(self, data: bytes) -> bytes:
        pass

    def publicKey(self) -> PublicKey:
        pass

    @classmethod
    def generate(cls, key: dict):
        # get algorithm name
        algorithm = key['algorithm']
        clazz = private_key_classes[algorithm]
        if issubclass(clazz, PrivateKey):
            return clazz.generate(key)
        else:
            raise ModuleNotFoundError('Invalid algorithm: ' + algorithm)


"""
    Extends Crypto Keys
    
    AESKey        as SymmetricKey
    RSAPublicKey  as PublicKey
    RSAPrivateKey as PrivateKey
"""


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
            iv = b'0000000000000000'
            key['iv'] = base64_encode(iv)
        # create key
        self = super(AESKey, cls).__new__(cls, key)
        self.data = data
        self.iv = iv
        return self

    @classmethod
    def generate(cls, key: dict) -> SymmetricKey:
        if 'size' in key:
            size = int(key['size'])
        else:
            size = 32
        data = bytes(numpy.random.bytes(size))
        key['data'] = base64_encode(data)
        return AESKey(key)

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
        self = super(RSAPublicKey, cls).__new__(cls, key)
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
        self = super(RSAPrivateKey, cls).__new__(cls, key)
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

symmetric_key_classes = {
    'AES': AESKey,
}

public_key_classes = {
    'RSA': RSAPublicKey,
}

private_key_classes = {
    'RSA': RSAPrivateKey,
}
