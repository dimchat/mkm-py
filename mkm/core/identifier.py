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

from ..types import ConstantString
from ..protocol import ID, IDFactory
from ..protocol import Address

from .address import ANYWHERE, EVERYWHERE


class Identifier(ConstantString, ID):

    def __init__(self, identifier: str, name: Optional[str], address: Address, terminal: Optional[str]):
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
        return self.address.network

    @property  # Override
    def is_broadcast(self) -> bool:
        return self.address.is_broadcast

    @property  # Override
    def is_user(self) -> bool:
        return self.address.is_user

    @property  # Override
    def is_group(self) -> bool:
        return self.address.is_group


class IdentifierFactory(IDFactory):

    def __init__(self):
        super().__init__()
        self.__ids = {}

    # Override
    def generate_identifier(self, meta, network: int, terminal: Optional[str]) -> ID:
        address = Address.generate(meta=meta, network=network)
        assert address is not None, 'failed to generate ID with meta: %s' % meta
        return ID.create(address=address, name=meta.seed, terminal=terminal)

    # Override
    def create_identifier(self, address: Address, name: Optional[str] = None, terminal: Optional[str] = None) -> ID:
        identifier = concat(address=address, name=name, terminal=terminal)
        cid = self.__ids.get(identifier)
        if cid is None:
            cid = Identifier(identifier=identifier, address=address, name=name, terminal=terminal)
            self.__ids[identifier] = cid
        return cid

    # Override
    def parse_identifier(self, identifier: str) -> Optional[ID]:
        cid = self.__ids.get(identifier)
        if cid is None:
            cid = parse(string=identifier)
            if cid is not None:
                self.__ids[identifier] = cid
        return cid


def parse(string: str) -> Optional[ID]:
    # split ID string
    pair = string.split('/', 1)
    # terminal
    if len(pair) == 1:
        # no terminal
        terminal = None
    else:
        # got terminal
        terminal = pair[1]
    # name @ address
    assert len(pair[0]) > 0, 'ID error: %s' % string
    pair = pair[0].split('@', 1)
    if len(pair) == 1:
        # got address without name
        name = None
        address = Address.parse(address=pair[0])
    else:
        # got name & address
        name = pair[0]
        address = Address.parse(address=pair[1])
    if address is not None:
        return Identifier(identifier=string, address=address, name=name, terminal=terminal)


def concat(address: Address, name: Optional[str] = None, terminal: Optional[str] = None) -> str:
    string = str(address)
    if name is not None and len(name) > 0:
        string = name + '@' + string
    if terminal is not None and len(terminal) > 0:
        string = string + '/' + terminal
    return string


# register ID factory
ID.register(factory=IdentifierFactory())


"""
    ID for Broadcast
    ~~~~~~~~~~~~~~~~
"""

ANYONE = ID.create(name='anyone', address=ANYWHERE)
EVERYONE = ID.create(name='everyone', address=EVERYWHERE)

# DIM Founder
FOUNDER = ID.create(name='moky', address=ANYWHERE)
