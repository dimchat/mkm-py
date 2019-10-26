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

from .address import Address, NetworkID, ANYWHERE, EVERYWHERE
from .address import is_broadcast as is_broadcast_address


class ID(str):
    """
        ID for entity (User/Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: "name@address[/terminal]"

        fields:
            name     - entity name, the seed of fingerprint to generate address
            address  - a string to identify an entity
            terminal - entity login resource(device), OPTIONAL
    """

    def __new__(cls, identifier: str=None,
                name: str=None, address: Address=None, terminal: str=None):
        """
        Create ID object with ID string or name + address

        :param identifier: ID string with format 'name@address/terminal'
        :param name:       A string for ID.name
        :param address:    An Address object for ID.address
        :param terminal:   A string for login point
        :return: ID object
        """
        if identifier is None and address is None:
            return None
        elif cls is ID:
            if identifier is None:
                # concatenate ID string
                assert address is not None, 'would not happen'
                identifier = str(address)
                if name is not None:
                    identifier = name + '@' + identifier
                if terminal is not None:
                    identifier = identifier + '/' + terminal
            elif isinstance(identifier, ID):
                # return ID object directly
                return identifier
            else:
                # split ID string
                pair = identifier.split('/', 1)
                if len(pair) == 2:
                    # got terminal
                    terminal = pair[1]
                pair = pair[0].split('@', 1)
                if len(pair) == 2:
                    # got name & address
                    name = pair[0]
                    address = Address(pair[1])
                else:
                    # got address
                    address = Address(pair[0])
        # verify ID.address, which number must not be ZERO
        assert address.number > 0, 'Invalid ID (address) string: %s' % address
        # new ID(str)
        self = super().__new__(cls, identifier)
        self.__name = name
        self.__address = address
        self.__terminal = terminal
        return self

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if super().__eq__(other):
            return True
        identifier = ID(other)
        assert identifier.valid, 'other ID not valid: %s' % other
        return self.name == identifier.name and self.address == identifier.address

    def __hash__(self) -> int:
        string = str(self.__address)
        if self.__name is not None and len(self.__name) > 0:
            string = self.__name + '@' + string
        if self.__terminal is not None and len(self.__terminal) > 0:
            string = string + '/' + self.__terminal
        return hash(string)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def address(self) -> Address:
        return self.__address

    @property
    def terminal(self) -> str:
        return self.__terminal

    @property
    def type(self) -> NetworkID:
        """ ID type """
        return self.__address.network

    @property
    def number(self) -> int:
        """ Search number of this ID """
        return self.__address.number

    @property
    def valid(self) -> bool:
        return self.__address is not None and self.__address.number > 0

    #
    #   Factory
    #
    @classmethod
    def new(cls, address: Address, name: str=None, terminal: str=None):
        # SUGGEST:
        #     Do NOT call 'ID(name=name, address=address)' directly,
        #     call 'ID.new(name=name, address=address)' instead
        return ID(name=name, address=address, terminal=terminal)


"""
    ID for broadcast
    ~~~~~~~~~~~~~~~~
"""


ANYONE = ID.new(name="anyone", address=ANYWHERE)
EVERYONE = ID.new(name="everyone", address=EVERYWHERE)


def is_broadcast(identifier: ID) -> bool:
    return is_broadcast_address(identifier.address)
