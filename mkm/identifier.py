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
from typing import Optional, List, Any

from .crypto import String
from .address import Address, ANYWHERE, EVERYWHERE
from .factories import Factories


class ID(ABC):
    """
        ID for entity (User/Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: "name@address[/terminal]"

        fields:
            name     - entity name, the seed of fingerprint to generate address
            address  - a string to identify an entity
            terminal - entity login resource(device), OPTIONAL
    """

    @property
    def name(self) -> Optional[str]:
        raise NotImplemented

    @property
    def address(self) -> Address:
        raise NotImplemented

    @property
    def terminal(self) -> Optional[str]:
        raise NotImplemented

    @property
    def type(self) -> int:
        """ ID type """
        return self.address.network

    @property
    def is_broadcast(self) -> bool:
        return self.address.is_broadcast

    @property
    def is_user(self) -> bool:
        return self.address.is_user

    @property
    def is_group(self) -> bool:
        return self.address.is_group

    @classmethod
    def convert(cls, members: List[str]):  # -> List[ID]:
        """
        Convert ID list from string array

        :param members: string array
        :return: ID list
        """
        array: List[ID] = []
        for item in members:
            identifier = cls.parse(identifier=item)
            if identifier is None:
                continue
            array.append(identifier)
        return array

    @classmethod
    def revert(cls, members) -> List[str]:
        """
        Revert ID list to string array

        :param members: ID list
        :return: string array
        """
        array = []
        for item in members:
            array.append(str(item))
        return array

    #
    #   ID factory
    #
    class Factory(ABC):

        @abstractmethod
        def generate_identifier(self, meta, network: int, terminal: Optional[str]):
            """
            Generate ID

            :param meta:     meta info
            :param network:  ID.type
            :param terminal: ID.terminal
            :return: ID
            """
            raise NotImplemented

        @abstractmethod
        def create_identifier(self, address: Address, name: Optional[str], terminal: Optional[str]):
            """
            Create ID

            :param address:  ID.address
            :param name:     ID.name
            :param terminal: ID.terminal
            :return: ID
            """
            raise NotImplemented

        @abstractmethod
        def parse_identifier(self, identifier: str):  # -> Optional[ID]:
            """
            Parse string object to ID

            :param identifier: ID string
            :return: ID
            """
            raise NotImplemented

    @classmethod
    def register(cls, factory: Factory):
        Factories.id_factory = factory

    @classmethod
    def factory(cls) -> Factory:
        return Factories.id_factory

    #
    #   Factory methods
    #

    @classmethod
    def generate(cls, meta, network: int, terminal: Optional[str] = None):  # -> ID:
        factory = cls.factory()
        assert factory is not None, 'ID factory not ready'
        return factory.generate_identifier(meta=meta, network=network, terminal=terminal)

    @classmethod
    def create(cls, address: Address, name: Optional[str] = None, terminal: Optional[str] = None):  # -> ID:
        factory = cls.factory()
        assert factory is not None, 'ID factory not ready'
        return factory.create_identifier(address=address, name=name, terminal=terminal)

    @classmethod
    def parse(cls, identifier: Any):  # -> Optional[ID]:
        if identifier is None:
            return None
        elif isinstance(identifier, ID):
            return identifier
        elif isinstance(identifier, String):
            identifier = identifier.string
        # assert isinstance(identifier, str), 'ID error: %s' % identifier
        factory = cls.factory()
        assert factory is not None, 'ID factory not ready'
        return factory.parse_identifier(identifier=identifier)


"""
    Implements
    ~~~~~~~~~~
"""


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


class Identifier(String, ID):

    def __init__(self, identifier: str, address: Address, name: Optional[str] = None, terminal: Optional[str] = None):
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


"""
    ID factory
    ~~~~~~~~~~
"""


class IDFactory(ID.Factory):

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


"""
    ID for Broadcast
    ~~~~~~~~~~~~~~~~
"""

# register ID factory
ID.register(factory=IDFactory())

ANYONE = ID.create(name='anyone', address=ANYWHERE)
EVERYONE = ID.create(name='everyone', address=EVERYWHERE)

# DIM Founder
FOUNDER = ID.create(name='moky', address=ANYWHERE)
