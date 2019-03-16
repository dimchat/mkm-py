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

from abc import abstractmethod, ABCMeta, ABC

from .crypto import PublicKey, PrivateKey
from .identifier import ID
from .entity import Entity, IEntityDataSource


class Account(Entity):
    """
        Account for communication
        ~~~~~~~~~~~~~~~~~~~~~~~~~

        Account with ID and Public Key
    """

    @property
    def publicKey(self) -> PublicKey:
        return self.meta.key


class User(Account):
    """
        User with private key
        ~~~~~~~~~~~~~~~~~~~~~
    """

    def __init__(self, identifier: ID, private_key: PrivateKey):
        """
        Create User With ID and Private Key

        :param identifier:  User ID
        :param private_key: User Private key
        """
        super().__init__(identifier)
        self.privateKey = private_key

    @property
    def contacts(self) -> list:
        return self.delegate.user_contacts(user=self)


#
#  Delegates
#


class IAccountDelegate(metaclass=ABCMeta):
    """
        Account Delegate
        ~~~~~~~~~~~~~~~~
    """

    @abstractmethod
    def account_create(self, identifier: ID) -> Account:
        """ Create account with ID """
        pass


class IUserDelegate(IAccountDelegate, ABC):
    """
        User Delegate
        ~~~~~~~~~~~~~
    """

    @abstractmethod
    def user_create(self, identifier: ID) -> User:
        """ Create user with ID """
        pass

    @abstractmethod
    def user_add_contact(self, user: User, contact: ID) -> bool:
        """ Add contact to user """
        pass

    @abstractmethod
    def user_remove_contact(self, user: User, contact: ID) -> bool:
        """ Remove contact from user """
        pass


class IUserDataSource(IEntityDataSource, ABC):
    """
        User Data Source
        ~~~~~~~~~~~~~~~~
    """

    @abstractmethod
    def user_contacts(self, user: User) -> int:
        """ Get all contacts of user """
        pass
