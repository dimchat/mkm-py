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
from typing import Optional, Any, Dict

from ..crypto import VerifyKey, SignKey


class TAI(ABC):
    """
        The Additional Information
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        'Meta' is the information for entity which never changed,
            which contains the key for verify signature;
        'TAI' is the variable part,
            which could contain a public key for asymmetric encryption.
    """

    @property
    @abstractmethod
    def valid(self) -> bool:
        """
        Check if signature matched

        :return: True on matched
        """
        raise NotImplemented

    #
    #  signature
    #

    @abstractmethod
    def verify(self, public_key: VerifyKey) -> bool:
        """
        Verify 'data' and 'signature' with public key

        :param public_key: public key in meta.key
        :return: True on signature matched
        """
        raise NotImplemented

    @abstractmethod
    def sign(self, private_key: SignKey) -> Optional[bytes]:
        """
        Encode properties to 'data' and sign it to 'signature'

        :param private_key: private key match meta.key
        :return: signature, None on error
        """
        raise NotImplemented

    #
    #  properties
    #

    @property
    @abstractmethod
    def properties(self) -> Optional[Dict]:
        """
        Get all properties when valid

        :return: inner dictionary
        """
        raise NotImplemented

    @abstractmethod
    def get_property(self, name: str) -> Optional[Any]:
        """
        Get property value with key

        :param name: property key
        :return: property value
        """
        raise NotImplemented

    @abstractmethod
    def set_property(self, name: str, value: Optional[Any]):
        """
        Update property with key and data
        (this will clear 'data' and 'signature')

        :param name:  property key
        :param value: property value
        """
        raise NotImplemented
