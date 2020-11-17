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
from typing import Optional, Union, Any

from .crypto import PublicKey, EncryptKey, VerifyKey, SignKey
from .crypto import Base64

from .identifier import ID
from .tai import TAI


class Profile(dict, TAI):

    # noinspection PyTypeChecker
    def __new__(cls, profile: dict):
        if profile is None:
            return None
        elif cls is Profile:
            inst = TAI.__new__(TAI, profile)
            if inst is not None:
                # created by subclass
                return inst
        # new Profile(dict)
        return super().__new__(cls, profile)

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
    def _data(self) -> Optional[bytes]:
        """ Profile properties data """
        if self.__data is None:
            string: str = self.get('data')
            if string is not None:
                self.__data = string.encode('utf-8')
        return self.__data

    @property
    def _signature(self) -> Optional[bytes]:
        """ Profile properties signature """
        if self.__signature is None:
            base64: str = self.get('signature')
            if base64 is not None:
                self.__signature = Base64.decode(base64)
        return self.__signature

    @property
    def valid(self) -> bool:
        return self.__status >= 0

    """
        Profile Properties
        ~~~~~~~~~~~~~~~~~~
    """

    @property
    def _properties(self) -> Optional[dict]:
        """ Load properties from data """
        if self.__status < 0:
            # invalid
            return None
        if self.__properties is None:
            data = self._data
            if data is None:
                # create new properties
                self.__properties = {}
            else:
                # get properties from data
                self.__properties = json.loads(data)
                assert isinstance(self.__properties, dict)
        return self.__properties

    def set_property(self, key: str, value: Any=None):
        """ Update profile property with key and data """
        # 1. reset status
        self.__status = 0
        # 2. update property value with name
        super().set_property(key=key, value=value)
        # 3. clear data signature after properties changed
        self.pop('data', None)
        self.pop('signature', None)
        self.__data = None
        self.__signature = None

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

    @name.setter
    def name(self, value: str):
        self.set_property(key='name', value=value)

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
        if self.__status > 0:
            # already verify OK
            return True
        data = self._data
        signature = self._signature
        if data is None:
            # NOTICE: if data is empty, signature should be empty at the same time
            #         this happen while profile not found
            if signature is None:
                self.__status = 0
            else:
                # data signature error
                self.__status = -1
        elif signature is None:
            # signature error
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
        if self.__status > 0:
            # already signed
            return self.__signature
        self.__status = 1
        data: str = json.dumps(self._properties)
        self.__data = data.encode('utf-8')
        self.__signature = private_key.sign(self.__data)
        self['data'] = data  # JsON string
        self['signature'] = Base64.encode(self.__signature)
        return self.__signature

    @classmethod
    def new(cls, identifier: ID):
        """ Create new empty profile object with entity ID """
        profile = {
            'ID': identifier,
        }
        return cls(profile)


class UserProfile(Profile):

    # noinspection PyTypeChecker
    def __new__(cls, profile: dict):
        if profile is None:
            return None
        elif cls is UserProfile:
            # 1. if ID type is user, convert to UserProfile
            # 2. if public key not exists, no need to convert to UserProfile
            identifier = profile.get('ID')
            if isinstance(identifier, ID):
                if not identifier.is_user:
                    return None
            # elif 'avatar' not in profile and 'key' not in profile:
            #     # not a user profile
            #     return None
        # new UserProfile(dict)
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
        Nickname
        ~~~~~~~~
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

    """
        Avatar
        ~~~~~~
    """
    @property
    def avatar(self) -> Optional[str]:
        value = self.get_property(key='avatar')
        if value is not None:
            return value
        # get from 'names'
        array = self.get_property(key='photos')
        if array is not None and len(array) > 0:
            return array[0]

    @avatar.setter
    def avatar(self, value: str):
        self.set_property(key='avatar', value=value)


# register user profile class
Profile.register(UserProfile)
