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

from abc import abstractmethod, ABC

from .crypto import PublicKey, PrivateKey
from .identifier import ID
from .entity import Entity, IEntityDataSource
from .profile import Profile


class User(Entity):
    """This class is for creating user

        User for communication
        ~~~~~~~~~~~~~~~~~~~~~~

            functions:
                verify(data, signature) - verify (encrypted content) data and signature
                encrypt(data)           - encrypt (symmetric key) data
    """

    def __meta_key(self) -> PublicKey:
        meta = self.meta
        if meta is not None:
            return meta.key

    def __profile_key(self) -> PublicKey:
        profile = self.profile
        if profile is not None:
            return profile.key

    @property
    def profile(self) -> Profile:
        tai = super().profile
        if tai is not None:
            if tai.valid:
                # no need to verify
                return tai
            # try to verify with meta.key
            key = self.__meta_key()
            if tai.verify(public_key=key):
                # signature correct
                return tai
            # profile error? continue to process by subclass
            return tai

    def verify(self, data: bytes, signature: bytes) -> bool:
        """Verify data with signature, use meta.key

        :param data:
        :param signature:
        :return:
        """
        # # 1. get public key from profile
        # key = self.__profile_key()
        # if key is not None and key.verify(data=data, signature=signature):
        #     return True
        # 2. get public key from meta
        key = self.__meta_key()
        # 3. verify it
        return key.verify(data=data, signature=signature)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data, try profile.key first, if not found, use meta.key

        :param data: plaintext
        :return: ciphertext
        """
        # 1. get key for encryption from profile
        key = self.__profile_key()
        if key is None:
            # 2. get key for encryption from meta instead
            # NOTICE: meta.key will never changed, so use profile.key to encrypt is the better way
            key = self.__meta_key()
        # 3. encrypt it
        return key.encrypt(data=data)


class IUserDataSource(IEntityDataSource, ABC):
    """This interface is for getting private information for local user

        Local User Data Source
        ~~~~~~~~~~~~~~~~~~~~~~

        1. private key for signature, is the key matching with meta.key;
        2. private key for decryption, is the key matching with profile.key,
           if profile.key not exists, means it is the same key pair with meta.key
    """

    @abstractmethod
    def private_key_for_signature(self, identifier: ID) -> PrivateKey:
        """
        Get user's private key for signature

        :param identifier: user ID
        :return: private key
        """
        pass

    @abstractmethod
    def private_keys_for_decryption(self, identifier: ID) -> list:
        """
        Get user's private keys for decryption

        :param identifier: user ID
        :return: private keys
        """
        pass

    @abstractmethod
    def contacts(self, identifier: ID) -> list:
        """
        Get user's contacts list

        :param identifier: user ID
        :return: contacts list (ID)
        """
        pass


class LocalUser(User):
    """This class is for creating local user

        User for communication
        ~~~~~~~~~~~~~~~~~~~~~~

            functions:
                sign(data)    - calculate signature of (encrypted content) data
                decrypt(data) - decrypt (symmetric key) data
    """

    def __sign_key(self) -> PrivateKey:
        delegate: IUserDataSource = self.delegate
        return delegate.private_key_for_signature(identifier=self.identifier)

    def __decrypt_keys(self) -> list:
        delegate: IUserDataSource = self.delegate
        return delegate.private_keys_for_decryption(identifier=self.identifier)

    @property
    def contacts(self) -> list:
        """
        Get all contacts of the user

        :return: contacts list
        """
        delegate: IUserDataSource = self.delegate
        return delegate.contacts(identifier=self.identifier)

    def sign(self, data: bytes) -> bytes:
        """
        Sign data with user's private key

        :param data: message data
        :return: signature
        """
        key = self.__sign_key()
        return key.sign(data=data)

    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypt data with user's private key(s)

        :param data: ciphertext
        :return: plaintext
        """
        keys = self.__decrypt_keys()
        # try decrypting it with each private key
        for key in keys:
            try:
                plaintext = key.decrypt(data=data)
                if plaintext is not None:
                    # OK!
                    return plaintext
            except ValueError:
                # this key not match, try next one
                continue
