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

import json

from mkm.utils import base64_decode, base64_encode

from mkm import ID, PublicKey, PrivateKey


class TAO(dict):
    """
        The Additional Object
        ~~~~~~~~~~~~~~~~~~~~~

        'Meta' is the information for entity which never changed, which contains the key for verify signature;
        'TAO' is the variable part, which contains the key for asymmetric encryption.
    """

    @classmethod
    def __tao(cls, identifier: ID = None, data: str = None, signature: bytes = None):
        profile = {
            'ID': identifier
        }
        if data is not None:
            profile['data'] = data
        if signature is not None:
            profile['signature'] = base64_encode(signature)
        return profile

    def __new__(cls, profile: dict = None,
                identifier: ID = None, data: str = None, signature: bytes = None):
        """
        Create The Additional Object for Identifier

        :param profile:    A dictionary as profile info
        :param identifier: A string as entity ID
        :param data:       A json string encoded for profile properties
        :param signature:  A signature with data
        :return: The Additional Object
        """
        if profile is None:
            profile = TAO.__tao(identifier=identifier, data=data, signature=signature)
        elif isinstance(profile, TAO):
            # return Profile object directly
            return profile
        # new Profile(dict)
        return super().__new__(cls, profile)

    def __init__(self, profile: dict = None,
                 identifier: ID = None, data: str = None, signature: bytes = None):
        if profile is None:
            profile = TAO.__tao(identifier=identifier, data=data, signature=signature)
        else:
            # get fields from dictionary
            identifier = ID(profile.get('ID'))
            data = profile.get('data')
            signature = base64_decode(profile.get("signature"))
        super().__init__(profile)
        self.identifier = identifier
        self.properties = {}
        self.data = data
        self.signature = signature
        self.valid = False
        self.__key = None

    def get_property(self, key):
        if self.valid:
            return self.properties.get(key)

    def set_property(self, key, value):
        if value is None:
            self.properties.pop(key, None)
        else:
            self.properties[key] = value
        self.reset()

    def reset(self):
        """ Reset data signature after properties changed """
        self.pop('data', None)
        self.pop('signature', None)
        self.data = ''
        self.signature = None
        self.valid = False
        self.__key = None

    def verify(self, public_key: PublicKey) -> bool:
        """
        Verify 'data' and 'signature', if OK, refresh properties from 'data'

        :param public_key: public key in meta.key
        :return: True on signature matched
        """
        if self.valid:
            # already verify
            return True
        if self.data is None or self.signature is None:
            # data error
            return False
        if public_key.verify(self.data.encode('utf-8'), self.signature):
            self.valid = True
            # refresh properties
            self.properties = json.loads(self.data)
            # get public key
            self.__key = PublicKey(self.properties.get('key'))
        else:
            self.data = None
            self.signature = None
        return self.valid

    def sign(self, private_key: PrivateKey) -> bytes:
        """
        Encode properties to 'data' and sign it to 'signature'

        :param private_key: private key match meta.key
        :return: signature
        """
        if self.valid:
            # already signed
            return self.signature
        self.data = json.dumps(self.properties)
        self.signature = private_key.sign(self.data.encode('utf-8'))
        self['data'] = self.data
        self['signature'] = base64_encode(self.signature)
        self.valid = True
        return self.signature

    @property
    def key(self) -> PublicKey:
        if self.valid:
            return self.__key

    @key.setter
    def key(self, public_key: PublicKey):
        self.set_property(key='key', value=public_key)


class Profile(TAO):

    @property
    def name(self) -> str:
        return self.get_property(key='name')

    @name.setter
    def name(self, value: str):
        self.set_property(key='name', value=value)
