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

from .types import ConstantString
from .protocol import ID, Address, EntityType

from .address import ANYWHERE, EVERYWHERE


class Identifier(ConstantString, ID):

    def __init__(self, identifier: str, name: Optional[str], address: Address, terminal: Optional[str] = None):
        super().__init__(string=identifier)
        self.__name = name
        self.__address = address
        self.__terminal = terminal

    @property  # Override
    def name(self) -> Optional[str]:
        return self.__name

    @property  # Override
    def address(self) -> Address:
        return self.__address

    @property  # Override
    def terminal(self) -> Optional[str]:
        return self.__terminal

    @property  # Override
    def type(self) -> int:
        return self.__address.network

    @property  # Override
    def is_broadcast(self) -> bool:
        network = self.type
        return EntityType.is_broadcast(network=network)

    @property  # Override
    def is_user(self) -> bool:
        network = self.type
        return EntityType.is_user(network=network)

    @property  # Override
    def is_group(self) -> bool:
        network = self.type
        return EntityType.is_group(network=network)

    #
    #   Factory
    #

    @classmethod
    def new(cls, name: Optional[str], address: Address, terminal: Optional[str] = None) -> ID:
        identifier = cls.concat(name=name, address=address, terminal=terminal)
        return Identifier(identifier=identifier, name=name, address=address, terminal=terminal)

    @classmethod
    def concat(cls, name: Optional[str], address: Address, terminal: Optional[str] = None) -> str:
        string = str(address)
        if name is not None and len(name) > 0:
            string = name + '@' + string
        if terminal is not None and len(terminal) > 0:
            string = string + '/' + terminal
        return string


"""
    ID for Broadcast
    ~~~~~~~~~~~~~~~~
"""

ANYONE = Identifier.new(name='anyone', address=ANYWHERE)
EVERYONE = Identifier.new(name='everyone', address=EVERYWHERE)

# DIM Founder
FOUNDER = Identifier.new(name='moky', address=ANYWHERE)
