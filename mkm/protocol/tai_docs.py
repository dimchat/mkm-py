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
from typing import Optional, Union, List

from ..crypto import EncryptKey, VerifyKey

from .file import PortableNetworkFile
from .identifier import ID
from .tai_doc import Document


class Visa(Document, ABC):
    """
        User Document
        ~~~~~~~~~~~~~
        This interface is defined for authorizing other apps to login,
        which can generate a temporary asymmetric key pair for messaging.
    """

    @property
    @abstractmethod
    def key(self) -> Union[EncryptKey, VerifyKey, None]:
        """
        Get public key to encrypt message for user

        :return: public key
        """
        raise NotImplemented

    @key.setter
    @abstractmethod
    def key(self, value: Union[EncryptKey, VerifyKey]):
        """
        Set public key for other user to encrypt message

        :param value: public key as visa.key
        """
        raise NotImplemented

    @property
    @abstractmethod
    def avatar(self) -> Optional[PortableNetworkFile]:
        """
        Get avatar file

        :return: transportable file
        """
        raise NotImplemented

    @avatar.setter
    @abstractmethod
    def avatar(self, file: PortableNetworkFile):
        """
        Set avatar file/url

        :param file: transportable file, or URL string
        """
        raise NotImplemented


class Bulletin(Document, ABC):
    """
        Group Document
        ~~~~~~~~~~~~~~
    """

    @property
    @abstractmethod
    def founder(self) -> Optional[ID]:
        """
        Get group founder

        :return: user ID
        """
        raise NotImplemented

    @property
    @abstractmethod
    def assistants(self) -> Optional[List[ID]]:
        """
        Get group assistants

        :return: bot ID list
        """
        raise NotImplemented

    @assistants.setter
    @abstractmethod
    def assistants(self, bots: List[ID]):
        """
        Set group assistants

        :param bots: bot ID list
        """
        raise NotImplemented

    """
        Times
        ~~~~~
    """

    @property
    @abstractmethod
    def created_time(self) -> Optional[float]:
        raise NotImplemented

    @property
    @abstractmethod
    def modified_time(self) -> Optional[float]:
        raise NotImplemented
