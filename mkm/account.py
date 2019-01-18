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

from mkm.crypto import PublicKey, PrivateKey
from mkm.entity import ID, Entity


class Account(Entity):

    def __init__(self, identifier: ID, public_key: PublicKey):
        if identifier.address.network.is_communicator():
            super().__init__(identifier)
            # must verify the ID with meta info before creating an account with meta.key
            self.publicKey = public_key
        else:
            raise ValueError('Account ID error')


class User(Account):

    def __init__(self, identifier: ID, private_key: PrivateKey):
        if identifier.address.network.is_person():
            super().__init__(identifier, private_key.publicKey())
            self.privateKey = private_key
            self.contacts: list = []
        else:
            raise ValueError('User ID error')

    def addContact(self, contact: ID):
        if not contact.address.network.is_person():
            raise AssertionError('Contact must be a person')
        if contact not in self.contacts:
            self.contacts.append(contact)

    def removeContact(self, contact: ID):
        if contact in self.contacts:
            self.contacts.remove(contact)

    def hasContact(self, contact: ID) -> bool:
        return contact in self.contacts
