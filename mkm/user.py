# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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

from .crypto import EncryptKey, DecryptKey, SignKey, VerifyKey
from .entity import Entity
from .delegate import UserDataSource


class User(Entity):
    """This class is for creating user

        User for communication
        ~~~~~~~~~~~~~~~~~~~~~~

        functions:
            (User)
            1. verify(data, signature) - verify (encrypted content) data and signature
            2. encrypt(data)           - encrypt (symmetric key) data
            (LocalUser)
            3. sign(data)    - calculate signature of (encrypted content) data
            4. decrypt(data) - decrypt (symmetric key) data
    """

    @Entity.delegate.getter
    def delegate(self) -> Optional[UserDataSource]:
        facebook = super().delegate
        assert facebook is None or isinstance(facebook, UserDataSource), 'error: %s' % facebook
        return facebook

    # @delegate.setter
    # def delegate(self, value: UserDataSource):
    #     super(User, User).delegate.__set__(self, value)

    @property
    def contacts(self) -> Optional[list]:
        """
        Get all contacts of the user

        :return: contacts list
        """
        return self.delegate.contacts(identifier=self.identifier)

    def __meta_key(self) -> VerifyKey:
        meta = self.meta
        assert meta is not None, 'failed to get meta for user: %s' % self.identifier
        return meta.key

    def __profile_key(self) -> Optional[EncryptKey]:
        profile = self.profile
        if profile is None or not profile.valid:
            # profile not found or not valid
            return None
        return profile.key

    # NOTICE: meta.key will never changed, so use profile.key to encrypt
    #         is the better way
    def __encrypt_key(self) -> EncryptKey:
        # 0. get key from data source
        key = self.delegate.public_key_for_encryption(identifier=self.identifier)
        if key is not None:
            return key
        # 1. get key from profile
        key = self.__profile_key()
        if key is not None:
            return key
        # 2. get key from meta
        key = self.__meta_key()
        if isinstance(key, EncryptKey):
            return key
        raise LookupError('failed to get encrypt key for user: %s' % self.identifier)

    # NOTICE: I suggest using the private key paired with meta.key to sign message
    #         so here should return the meta.key
    def __verify_keys(self) -> list:
        # 0. get keys from data source
        keys = self.delegate.public_keys_for_verification(identifier=self.identifier)
        if keys is not None and len(keys) > 0:
            return keys
        keys = []
        # # 1. get key from profile
        # key = self.__profile_key()
        # if isinstance(key, VerifyKey):
        #     keys.append(key)
        # 2. get key from meta
        key = self.__meta_key()
        assert key is not None, 'meta.key not found: %s' % self.identifier
        keys.append(key)
        return keys

    def verify(self, data: bytes, signature: bytes) -> bool:
        """
        Verify data and signature with user's public keys

        :param data:
        :param signature:
        :return:
        """
        keys = self.__verify_keys()
        for key in keys:
            if key.verify(data=data, signature=signature):
                # matched!
                return True

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data, try profile.key first, if not found, use meta.key

        :param data: plaintext
        :return: ciphertext
        """
        key = self.__encrypt_key()
        assert key is not None, 'failed to get encrypt key for user: %s' % self.identifier
        return key.encrypt(data=data)

    #
    #   interfaces for local user
    #

    # NOTICE: I suggest use the private key which paired to meta.key
    #         to sign message
    def __sign_key(self) -> SignKey:
        return self.delegate.private_key_for_signature(identifier=self.identifier)

    # NOTICE: if you provide a public key in profile for encryption
    #         here you should return the private key paired with profile.key
    def __decrypt_keys(self) -> list:
        return self.delegate.private_keys_for_decryption(identifier=self.identifier)

    def sign(self, data: bytes) -> bytes:
        """
        Sign data with user's private key

        :param data: message data
        :return: signature
        """
        key = self.__sign_key()
        assert key is not None, 'failed to get sign key for user: %s' % self.identifier
        return key.sign(data=data)

    def decrypt(self, data: bytes) -> Optional[bytes]:
        """
        Decrypt data with user's private key(s)

        :param data: ciphertext
        :return: plaintext
        """
        keys = self.__decrypt_keys()
        assert keys is not None and len(keys) > 0, 'failed to get decrypt keys: %s' % self.identifier
        for key in keys:
            assert isinstance(key, DecryptKey), 'decrypt key error: %s' % key
            try:
                # try decrypting it with each private key
                plaintext = key.decrypt(data=data)
                if plaintext is not None:
                    # OK!
                    return plaintext
            except ValueError:
                # this key not match, try next one
                continue
