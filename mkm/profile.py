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

import json
from abc import ABC, abstractmethod
from typing import Optional, Union, Any

from .crypto.utils import base64_decode, base64_encode
from .crypto import PublicKey, EncryptKey, VerifyKey, SignKey
from .identifier import ID


class TAI(dict, ABC):
    """
        The Additional Information
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        'Meta' is the information for entity which never changed, which contains the key for verify signature;
        'TAI' is the variable part, which contains the key for asymmetric encryption.
    """

    def __init__(self, profile: dict):
        if self is profile:
            # no need to init again
            return
        super().__init__(profile)
        # lazy
        self.__identifier: str = None
        self.__data: bytes = None
        self.__signature: bytes = None
        self.__properties: dict = None
        self.__status: int = 0  # 1 for valid, -1 for invalid

    @property
    def identifier(self) -> str:
        """ Profile ID """
        if self.__identifier is None:
            self.__identifier = self['ID']
        return self.__identifier

    @property
    def data(self) -> bytes:
        """ Profile properties data """
        if self.__data is None:
            string: str = self.get('data')
            if string is not None:
                self.__data = string.encode('utf-8')
        return self.__data

    @property
    def signature(self) -> bytes:
        """ Profile properties signature """
        if self.__signature is None:
            base64: str = self.get('signature')
            if base64 is not None:
                self.__signature = base64_decode(base64)
        return self.__signature

    @property
    def valid(self) -> bool:
        return self.__status >= 0

    @property
    @abstractmethod
    def key(self) -> Optional[EncryptKey]:
        """
        Get public key for encryption

        :return: public key
        """
        raise NotImplemented

    """
        Profile Properties
        ~~~~~~~~~~~~~~~~~~
        Inner dictionary
    """

    def properties(self) -> Optional[dict]:
        """ Load properties from data """
        if self.__status == -1:
            # invalid
            return None
        if self.__properties is None:
            data = self.data
            if data is None:
                # create new properties
                self.__properties = {}
            else:
                # get properties from data
                self.__properties = json.loads(data)
                assert isinstance(self.__properties, dict)
        return self.__properties

    def get_property(self, key: str) -> Optional[Any]:
        """
        Get profile property data with key

        :param key: property key
        :return: property value
        """
        properties = self.properties()
        if properties is None:
            return None
        return properties.get(key)

    def set_property(self, key: str, value: Any=None):
        """
        Update profile property with key and data
        (this will reset 'data' and 'signature')

        :param key:   property key
        :param value: property value
        """
        self.__status = 0
        properties = self.properties()
        if value is None:
            properties.pop(key, None)
        else:
            properties[key] = value
        # clear data signature after properties changed
        self.pop('data', None)
        self.pop('signature', None)
        self.__data = None
        self.__signature = None

    """
        Sign/Verify profile data
        ~~~~~~~~~~~~~~~~~~~~~~~~
    """

    def verify(self, public_key: VerifyKey) -> bool:
        """
        Verify 'data' and 'signature' with public key

        :param public_key: public key in meta.key
        :return: True on signature matched
        """
        if self.__status == 1:
            # already verify OK
            return True
        data = self.data
        signature = self.signature
        if data is None or signature is None:
            # data error
            self.__status = -1
        elif public_key.verify(data, signature):
            # signature matched
            self.__status = 1
        # NOTICE: if status is 0, it doesn't mean the profile is invalid,
        #         try another key
        return self.__status == 1

    def sign(self, private_key: SignKey) -> bytes:
        """
        Encode properties to 'data' and sign it to 'signature'

        :param private_key: private key match meta.key
        :return: signature
        """
        if self.__status == 1:
            # already signed
            return self.__signature
        self.__status = 1
        data: str = json.dumps(self.properties())
        self.__data = data.encode('utf-8')
        self.__signature = private_key.sign(self.__data)
        self['data'] = data  # JsON string
        self['signature'] = base64_encode(self.__signature)
        return self.__signature


class Profile(TAI):

    # noinspection PyTypeChecker
    def __new__(cls, profile: dict):
        if profile is None:
            return None
        elif cls is Profile:
            if isinstance(profile, Profile):
                # return Profile object directly
                return profile
        # new Profile(dict)
        return super().__new__(cls, profile)

    def __init__(self, profile: dict):
        if self is profile:
            # no need to init again
            return
        super().__init__(profile)
        # lazy
        self.__key: PublicKey = None  # EncryptKey

    """
        Public Key for encryption
        ~~~~~~~~~~~~~~~~~~~~~~~~~
        For safety considerations, the profile.key which used to encrypt message data
        should be different with meta.key
    """

    @property
    def key(self) -> Union[PublicKey, EncryptKey, None]:
        if self.__key is None:
            key = self.get_property(key='key')
            if key is not None:
                self.__key = PublicKey(key=key)
        return self.__key

    @key.setter
    def key(self, value: Union[PublicKey, EncryptKey]):
        self.__key = value
        self.set_property('key', value)

    """
        Name
        ~~~~
        Nickname for user
        Title for group
    """

    @property
    def name(self) -> Optional[str]:
        value = self.get_property(key='name')
        if value is not None:
            return value
        # get from 'names'
        array = self.get_property(key='names')
        if array is not None and len(array) > 0:
            return array[0]

    @name.setter
    def name(self, value: str):
        self.set_property(key='name', value=value)

    @classmethod
    def new(cls, identifier: ID):
        """ Create new empty profile object with entity ID """
        profile = {
            'ID': identifier,
        }
        return cls(profile)
