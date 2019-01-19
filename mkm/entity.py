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

from mkm.address import Address, NetworkID


class ID(str):
    """
        ID for entity (Account/Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: "name@address[/terminal]"

        filed(s):
            name     - entity name, the seed of fingerprint to generate address
            address  - a string to identify an entity
            terminal - entity login resource(device), OPTIONAL
    """

    def __new__(cls, identifier: str='',
                name: str='', address: Address=None, terminal: str=None):
        """
        Create ID object with ID string or name + address

        :param identifier: ID string with format 'name@address/terminal'
        :param name:       A string for ID.name
        :param address:    An Address object for ID.address
        :param terminal:   A string for login point
        :return: ID object
        """
        if identifier:
            # return ID object directly
            if isinstance(identifier, ID):
                return identifier
            # get fields from string
            pair = identifier.split('@', 1)
            if len(pair) == 2:
                name = pair[0]
                pair = pair[1].split('/', 1)
                address = Address(pair[0])
                if len(pair) == 2:
                    terminal = pair[1]
                else:
                    terminal = None
            else:
                raise ValueError('Invalid ID string')
        elif name and address:
            # concatenate ID string
            if terminal:
                identifier = name + '@' + address + '/' + terminal
            else:
                identifier = name + '@' + address
        else:
            raise AssertionError('Parameters error')
        # verify ID.address, which number must not be ZERO
        if address.number > 0:
            # new str
            self = super().__new__(cls, identifier)
            self.name = name
            self.address = address
            self.terminal = terminal
            return self
        else:
            raise ValueError('Invalid ID (address) string')

    @property
    def number(self) -> int:
        return self.address.number

    @classmethod
    def generate(cls, seed: str, fingerprint: bytes, network: NetworkID, version: chr=Address.DefaultVersion):
        """ Generate ID with seed, fingerprint and network ID """
        address = Address.generate(fingerprint=fingerprint, network=network, version=version)
        if address.number > 0 and seed:
            return ID(name=seed, address=address)
        else:
            raise ValueError('ID parameters error')


class Entity:
    """
        Entity (Account/Group)
        ~~~~~~~~~~~~~~~~~~~~~~

        Entity with ID and name
    """

    def __init__(self, identifier: ID):
        """
        Create Entity with ID

        :param identifier: User/Group ID
        """
        if identifier.name and identifier.address.number > 0:
            super().__init__()
            self.identifier = identifier
            self.name = identifier.name
        else:
            raise ValueError('Invalid ID')

    def __str__(self):
        clazz = self.__class__.__name__
        identifier = self.identifier
        network = identifier.address.network
        number = identifier.address.number
        name = self.name
        return '<%s: %s(%d|%d) "%s">' % (clazz, identifier, network, number, name)

    @property
    def number(self) -> int:
        return self.identifier.address.number
