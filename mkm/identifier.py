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

from .wrappers import String

from .address import Address
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
    #   Factory methods
    #

    @classmethod
    def generate(cls, meta, network: int, terminal: Optional[str] = None):  # -> ID:
        factory = cls.factory()
        assert isinstance(factory, IDFactory), 'ID factory error: %s' % factory
        return factory.generate_identifier(meta=meta, network=network, terminal=terminal)

    @classmethod
    def create(cls, address: Address, name: Optional[str] = None, terminal: Optional[str] = None):  # -> ID:
        factory = cls.factory()
        assert isinstance(factory, IDFactory), 'ID factory error: %s' % factory
        return factory.create_identifier(name=name, address=address, terminal=terminal)

    @classmethod
    def parse(cls, identifier: Any):  # -> Optional[ID]:
        if identifier is None:
            return None
        elif isinstance(identifier, cls):
            return identifier
        elif isinstance(identifier, String):
            identifier = identifier.string
        # assert isinstance(identifier, str), 'ID error: %s' % identifier
        factory = cls.factory()
        assert isinstance(factory, IDFactory), 'ID factory error: %s' % factory
        return factory.parse_identifier(identifier=identifier)

    @classmethod
    def register(cls, factory):
        Factories.id_factory = factory

    @classmethod
    def factory(cls):  # -> IDFactory:
        return Factories.id_factory


class IDFactory(ABC):

    @abstractmethod
    def generate_identifier(self, meta, network: int, terminal: Optional[str]) -> ID:
        """
        Generate ID

        :param meta:     meta info
        :param network:  ID.type
        :param terminal: ID.terminal
        :return: ID
        """
        raise NotImplemented

    @abstractmethod
    def create_identifier(self, name: Optional[str], address: Address, terminal: Optional[str]) -> ID:
        """
        Create ID

        :param name:     ID.name
        :param address:  ID.address
        :param terminal: ID.terminal
        :return: ID
        """
        raise NotImplemented

    @abstractmethod
    def parse_identifier(self, identifier: str) -> Optional[ID]:
        """
        Parse string object to ID

        :param identifier: ID string
        :return: ID
        """
        raise NotImplemented
