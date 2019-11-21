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

"""
    Immortals
    ~~~~~~~~~

    Built-in users
"""

import os
from typing import Optional

from mkm import PublicKey
from .dos import JSONFile
from .crypto import PrivateKey
from .types import NetworkID
from .identifier import ID
from .meta import Meta
from .profile import Profile
from .user import User
from .delegate import UserDataSource


def load_resource_file(filename: str) -> dict:
    directory = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(directory, 'res', filename)
    file = JSONFile(path=path)
    return file.read()


class Immortals(UserDataSource):

    def __init__(self):
        super().__init__()
        # caches
        self.__ids = {}
        self.__metas = {}
        self.__private_keys = {}
        self.__profiles = {}
        self.__users = {}
        # load built-in users
        self.__load_user(username='hulk')
        self.__load_user(username='moki')

    def __load_user(self, username: str):
        # load meta and generate ID
        identifier = self.identifier_from_meta(filename=username+'_meta.js')
        if identifier is None:
            return
        # load private key
        self.load_private_key(identifier=identifier, filename=username+'_secret.js')
        # load profile
        self.load_profile(identifier=identifier, filename=username+'_profile.js')

    def identifier_from_meta(self, filename: str, network: NetworkID=NetworkID.Main) -> Optional[ID]:
        # load meta
        meta = Meta(load_resource_file(filename=filename))
        if meta is None:
            return None
        # generate
        identifier = meta.generate_identifier(network=network)
        # cache them
        self.cache_id(identifier=identifier)
        self.cache_meta(meta=meta, identifier=identifier)
        return identifier

    def load_private_key(self, filename: str, identifier: ID) -> Optional[PrivateKey]:
        key = PrivateKey(load_resource_file(filename=filename))
        if key is None:
            return None
        # cache it
        self.cache_private_key(private_key=key, identifier=identifier)
        return key

    def load_profile(self, filename: str, identifier: ID) -> Optional[Profile]:
        profile = Profile(load_resource_file(filename=filename))
        if profile is None:
            return None
        assert profile.identifier == identifier, 'profile ID not match: %s, %s' % (identifier, profile)
        # copy 'name'
        name = profile.get('name')
        if name is None:
            names = profile.get('names')
            if names is not None and len(names) > 0:
                profile.set_property('name', names[0])
        # copy 'avatar'
        avatar = profile.get('avatar')
        if avatar is None:
            photos = profile.get('photos')
            if photos is not None and len(photos) > 0:
                profile.set_property('avatar', photos[0])
        # sign and cache
        self.sign_profile(profile=profile)
        self.cache_profile(profile=profile)
        return profile

    def cache_id(self, identifier: ID) -> bool:
        assert identifier.valid, 'ID not valid: %s' % identifier
        self.__ids[identifier] = identifier
        return True

    def cache_meta(self, meta: Meta, identifier: ID) -> bool:
        assert meta.match_identifier(identifier), 'meta not match ID: %s, %s' % (identifier, meta)
        self.__metas[identifier] = meta
        return True

    def cache_private_key(self, private_key: PrivateKey, identifier: ID) -> bool:
        self.__private_keys[identifier] = private_key
        return True

    def cache_profile(self, profile: Profile) -> bool:
        assert profile.valid, 'profile not valid: %s' % profile
        self.__profiles[profile.identifier] = profile
        return True

    def verify_profile(self, profile: Profile) -> bool:
        identifier = self.identifier(profile.identifier)
        meta = self.meta(identifier=identifier)
        if meta is None:
            return False
        return profile.verify(public_key=meta.key)

    def sign_profile(self, profile: Profile) -> Optional[Profile]:
        identifier = self.identifier(profile.identifier)
        key = self.private_key_for_signature(identifier)
        if key is None:
            return None
        profile.sign(private_key=key)
        return profile

    def identifier(self, string: str) -> Optional[ID]:
        return self.__ids.get(string)

    def user(self, identifier: ID) -> Optional[User]:
        #  get from barrack cache
        user = self.__users.get(identifier)
        if user is not None:
            return user
        # check meta and private key
        meta = self.meta(identifier=identifier)
        if meta is not None:
            user = User(identifier=identifier)
            # cache it in barrack
            user.delegate = self
            self.__users[identifier] = user
            return user

    #
    #   EntityDataSource
    #
    def meta(self, identifier: ID) -> Optional[Meta]:
        return self.__metas.get(identifier)

    def profile(self, identifier: ID) -> Optional[Profile]:
        return self.__profiles.get(identifier)

    #
    #   UserDataSource
    #
    def contacts(self, identifier: ID) -> Optional[list]:
        if identifier not in self.__ids:
            return None
        array = []
        for key, value in self.__ids.items():
            if key == identifier:
                continue
            array.append(value)
        return array

    def public_key_for_encryption(self, identifier: ID) -> PublicKey:
        pass

    def private_keys_for_decryption(self, identifier: ID) -> Optional[list]:
        key = self.__private_keys.get(identifier)
        if key is not None:
            return [key]

    def private_key_for_signature(self, identifier: ID) -> Optional[PrivateKey]:
        return self.__private_keys.get(identifier)

    def public_keys_for_verification(self, identifier: ID) -> Optional[list]:
        pass
