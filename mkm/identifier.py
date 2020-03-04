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

from typing import Optional

from .address import Address, ANYWHERE, EVERYWHERE


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
        if not isinstance(other, str):
            # other ID empty
            return False
        if super().__eq__(other):
            # same object
            return True
        if isinstance(other, ID):
            # check address
            address = self.address
            if address != other.address:
                return False
            # check name
            name = self.name
            if name is None or len(name) == 0:
                return other.name is None or len(other.name) == 0
            else:
                return name == other.name
        assert isinstance(other, str), 'ID error: %s' % other
        # comparing without terminal
        pair = other.split('/', 1)
        assert len(pair[0]) > 0, 'ID error: %s' % other
        terminal = self.terminal
        if terminal is None or len(terminal) == 0:
            return super().__eq__(pair[0])
        else:
            return pair[0] == self.split('/', 1)[0]

    def __hash__(self) -> int:
        # get address string
        string = str(self.address)
        # append name
        name = self.name
        if name is not None and len(name) > 0:
            string = name + '@' + string
        # append terminal
        terminal = self.terminal
        if terminal is not None and len(terminal) > 0:
            string = string + '/' + terminal
        return hash(string)

    @property
    def name(self) -> Optional[str]:
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
    def terminal(self) -> Optional[str]:
        if self.valid:
            return self.__terminal

    @property
    def type(self) -> int:
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
        return self.number > 0

    @property
    def is_broadcast(self) -> bool:
        assert self.address is not None, 'ID error: %s' % self
        return self.address.is_broadcast

    @property
    def is_user(self) -> bool:
        assert self.address is not None, 'ID error: %s' % self
        return self.address.is_user

    @property
    def is_group(self) -> bool:
        assert self.address is not None, 'ID error: %s' % self
        return self.address.is_group

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
