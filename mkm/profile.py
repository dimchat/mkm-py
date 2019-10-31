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
from typing import Optional

from .crypto.utils import base64_decode, base64_encode
from .crypto import PublicKey, PrivateKey
from .identifier import ID


class TAI(dict):
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
        # protected
        self._properties: dict = {}
        self._valid: bool = False

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
        return self._valid

    """
        Profile Properties
        ~~~~~~~~~~~~~~~~~~
        Inner dictionary
    """

    def get_property(self, key: str) -> Optional[object]:
        if self._valid:
            return self._properties.get(key)

    def set_property(self, key: str, value: object=None):
        if value is None:
            self._properties.pop(key, None)
        else:
            self._properties[key] = value
        self._reset()

    def _reset(self):
        """ Reset data signature after properties changed """
        self.pop('data', None)
        self.pop('signature', None)
        self.__data = None
        self.__signature = None
        self._valid = False

    """
        Sign/Verify profile data
        ~~~~~~~~~~~~~~~~~~~~~~~~
    """

    def verify(self, public_key: PublicKey) -> bool:
        """
        Verify 'data' and 'signature', if OK, refresh properties from 'data'

        :param public_key: public key in meta.key
        :return: True on signature matched
        """
        if self._valid:
            # already verify
            return True
        data = self.data
        signature = self.signature
        if data is None or signature is None:
            # data error
            return False
        if public_key.verify(data, signature):
            # signature matched
            self._valid = True
            # refresh properties
            dictionary = json.loads(data)
            if isinstance(dictionary, dict):
                self._properties = dictionary
            else:
                self._properties = {}
        return self._valid

    def sign(self, private_key: PrivateKey) -> bytes:
        """
        Encode properties to 'data' and sign it to 'signature'

        :param private_key: private key match meta.key
        :return: signature
        """
        if self._valid:
            # already signed
            return self.__signature
        self._valid = True
        data: str = json.dumps(self._properties)
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
        self.__key: PublicKey = None

    def _reset(self):
        super()._reset()
        self.__key = None

    """
        Public Key for encryption
        ~~~~~~~~~~~~~~~~~~~~~~~~~
        For safety considerations, the profile.key which used to encrypt message data should be different with meta.key
    """

    def verify(self, public_key: PublicKey) -> bool:
        if self._valid:
            # already verify
            return True
        if super().verify(public_key=public_key):
            # get public key
            self.__key = PublicKey(self._properties.get('key'))
            return True

    @property
    def key(self) -> Optional[PublicKey]:
        return self.__key

    @key.setter
    def key(self, value: PublicKey):
        self.__key = value
        self.set_property('key', value)

    """
        Name
        ~~~~
        Nickname for user
        Group name for group
    """

    @property
    def name(self) -> Optional[str]:
        return self.get_property(key='name')

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
