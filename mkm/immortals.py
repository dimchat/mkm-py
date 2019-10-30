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

from .crypto import PrivateKey
from .address import NetworkID
from .identifier import ID
from .meta import Meta
from .profile import Profile
from .user import User, LocalUser, UserDataSource
from .dos import JSONFile


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
        self.__load_user('hulk')
        self.__load_user('moki')

    def __load_user(self, username: str):
        # load meta
        meta = Meta(load_resource_file(filename=username+'_meta.js'))
        if meta is None:
            # meta not found
            return False
        # generate ID
        identifier = meta.generate_identifier(network=NetworkID.Main)
        # cache them
        self.cache_identifier(identifier=identifier)
        self.cache_meta(meta=meta, identifier=identifier)
        # load private key
        private_key = PrivateKey(load_resource_file(filename=username+'_secret.js'))
        if private_key is not None:
            # cache key
            self.cache_private_key(private_key=private_key, identifier=identifier)
        # load profile
        profile = Profile(load_resource_file(filename=username+'_profile.js'))
        if profile is None:
            # profile not found
            return True
        if self.verify_profile(profile=profile):
            # profile contains signature
            return True
        if private_key is None:
            return False
        # copy 'name'
        name = profile.get('name')
        if name is None:
            names = profile.get('names')
            if names is not None and len(names) > 0:
                profile.set_property('name', names[0])
        else:
            profile.set_property('name', name)
        # copy 'avatar'
        avatar = profile.get('avatar')
        if avatar is None:
            photos = profile.get('photos')
            if photos is not None and len(photos) > 0:
                profile.set_property('avatar', photos[0])
        else:
            profile.set_property('avatar', avatar)
        # sign and cache
        self.sign_profile(profile=profile)
        self.cache_profile(profile=profile)
        return True

    def cache_identifier(self, identifier: ID) -> bool:
        self.__ids[identifier] = identifier
        return True

    def cache_meta(self, meta: Meta, identifier: ID) -> bool:
        if not meta.match_identifier(identifier):
            return False
        self.__metas[identifier] = meta
        return True

    def cache_private_key(self, private_key: PrivateKey, identifier: ID) -> bool:
        self.__private_keys[identifier] = private_key
        return True

    def cache_profile(self, profile: Profile) -> bool:
        if not self.verify_profile(profile=profile):
            return False
        self.__profiles[profile.identifier] = profile
        return True

    def verify_profile(self, profile: Profile) -> bool:
        if profile.valid:
            return True
        identifier = self.identifier(profile.identifier)
        meta = self.meta(identifier=identifier)
        if meta is None:
            return False
        return profile.verify(public_key=meta.key)

    def sign_profile(self, profile: Profile) -> Optional[Profile]:
        if profile.valid:
            return profile
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
            key = self.private_key_for_signature(identifier=identifier)
            if key is None:
                user = User(identifier=identifier)
            else:
                user = LocalUser(identifier=identifier)
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
    def private_key_for_signature(self, identifier: ID) -> Optional[PrivateKey]:
        return self.__private_keys.get(identifier)

    def private_keys_for_decryption(self, identifier: ID) -> Optional[list]:
        key = self.__private_keys.get(identifier)
        if key is not None:
            return [key]

    def contacts(self, identifier: ID) -> Optional[list]:
        if identifier not in self.__ids:
            return None
        array = []
        for key, value in self.__ids.items():
            if key == identifier:
                continue
            array.append(value)
        return array
