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

    def __new__(cls, identifier: str):
        """
        Create ID object with string

        :param identifier: ID string with format 'name@address/terminal'
        :return: ID object
        """
        if identifier is None:
            return None
        elif cls is ID:
            if isinstance(identifier, ID):
                # return ID object directly
                return identifier
        # new ID(str)
        return super().__new__(cls, identifier)

    def __init__(self, identifier: str):
        if self is identifier:
            # no need to init again
            return
        super().__init__()
        # lazy
        self.__name: str = None
        self.__address: Address = None
        self.__terminal: str = None

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
        if self.valid:
            return self.__name

    @property
    def address(self) -> Address:
        if self.__address is None:
            # split ID string
            pair = self.split('/', 1)
            if len(pair) == 2:
                # got terminal
                self.__terminal = pair[1]
            else:
                self.__terminal = ''
            pair = pair[0].split('@', 1)
            if len(pair) == 2:
                # got name & address
                self.__name = pair[0]
                self.__address = Address(pair[1])
            else:
                # got address
                self.__name = ''
                self.__address = Address(pair[0])
        return self.__address

    @property
    def terminal(self) -> str:
        if self.valid:
            return self.__terminal

    @property
    def type(self) -> NetworkID:
        """ ID type """
        address = self.address
        if address is not None:
            return address.network

    @property
    def number(self) -> int:
        """ Search number of this ID """
        address = self.address
        if address is not None:
            return address.number

    @property
    def valid(self) -> bool:
        address = self.address
        if address is not None:
            return address.number > 0

    #
    #   Factory
    #
    @classmethod
    def new(cls, address: Address, name: str=None, terminal: str=None):
        # concatenate ID string
        string = str(address)
        if name is not None:
            string = name + '@' + string
        if terminal is not None:
            string = string + '/' + terminal
        # new ID(str)
        identifier = cls(string)
        identifier.__name = name
        identifier.__address = address
        identifier.__terminal = terminal
        return identifier


"""
    ID for broadcast
    ~~~~~~~~~~~~~~~~
"""


ANYONE = ID.new(name="anyone", address=ANYWHERE)
EVERYONE = ID.new(name="everyone", address=EVERYWHERE)


def is_broadcast(identifier: ID) -> bool:
    return is_broadcast_address(identifier.address)
