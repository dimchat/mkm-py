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

from abc import ABC, abstractmethod
from typing import Optional, Any

from .crypto import VerifyKey, SignKey, EncryptKey


class TAI(ABC):
    """
        The Additional Information
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        'Meta' is the information for entity which never changed,
            which contains the key for verify signature;
        'TAI' is the variable part,
            which could contain a public key for asymmetric encryption.
    """

    # noinspection PyTypeChecker
    def __new__(cls, profile: dict):
        if profile is None:
            return None
        assert cls is TAI, 'call TAI() directly'
        if isinstance(profile, TAI):
            # return Profile object directly
            return profile
        # try to create Profile object
        for clazz in cls.__tai_classes:
            inst = clazz.__new__(clazz, profile)
            if inst is not None:
                return inst

    @property
    @abstractmethod
    def identifier(self) -> str:
        """
        Entity ID

        :return: Entity ID
        """
        raise NotImplemented

    @property
    @abstractmethod
    def valid(self) -> bool:
        """
        If signature matched

        :return: True on valid
        """
        raise NotImplemented

    @property
    def key(self) -> Optional[EncryptKey]:
        """
        Get public key to encrypt message for user

        :return: public key
        """
        return None

    """
        Properties
        ~~~~~~~~~~
        
        Inner dictionary which will be serialized to 'data'
    """

    @property
    @abstractmethod
    def _properties(self) -> Optional[dict]:
        """
        Get all properties when valid

        :return: inner dictionary
        """
        raise NotImplemented

    def get_property(self, key: str) -> Optional[Any]:
        """
        Get property value with key

        :param key: property key
        :return: property value
        """
        properties = self._properties
        if properties is None:
            return None
        return properties.get(key)

    @abstractmethod
    def set_property(self, key: str, value: Any=None):
        """
        Update property with key and data
        (this will clear 'data' and 'signature')

        :param key:   property key
        :param value: property value
        """
        properties = self._properties
        assert properties is not None, 'failed to get properties'
        if value is None:
            properties.pop(key, None)
        else:
            properties[key] = value

    """
        Sign/Verify profile data
        ~~~~~~~~~~~~~~~~~~~~~~~~
    """

    @abstractmethod
    def verify(self, public_key: VerifyKey) -> bool:
        """
        Verify 'data' and 'signature' with public key

        :param public_key: public key in meta.key
        :return: True on signature matched
        """
        raise NotImplemented

    @abstractmethod
    def sign(self, private_key: SignKey) -> bytes:
        """
        Encode properties to 'data' and sign it to 'signature'

        :param private_key: private key match meta.key
        :return: signature
        """
        raise NotImplemented

    #
    #   Runtime
    #
    __tai_classes = []  # class list

    @classmethod
    def register(cls, tai_class) -> bool:
        """
        Register TAI class

        :param tai_class: class for parsing Profile
        :return: False on error
        """
        from .profile import Profile
        assert tai_class is not TAI, 'should not register TAI itself!'
        assert tai_class is not Profile, 'cannot register Profile!'
        if issubclass(tai_class, TAI):
            cls.__tai_classes.append(tai_class)
        else:
            raise TypeError('%s must be subclass of TAI' % tai_class)
        return True
