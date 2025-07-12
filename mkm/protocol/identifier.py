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
from typing import Optional, Iterable, List, Any

from ..types import Stringer

from .address import Address
from .helpers import AccountExtensions


class ID(Stringer, ABC):
    """
        ID for entity (User/Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: "name@address[/terminal]"

        fields:
            name     - entity name, the seed of fingerprint to generate address
            address  - a string to identify an entity
            terminal - location (device), RESERVED
    """

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        raise NotImplemented

    @property
    @abstractmethod
    def address(self) -> Address:
        raise NotImplemented

    @property
    @abstractmethod
    def terminal(self) -> Optional[str]:
        raise NotImplemented

    @property
    @abstractmethod
    def type(self) -> int:
        # return self.address.type
        raise NotImplemented

    @property
    @abstractmethod
    def is_broadcast(self) -> bool:
        # return EntityType.is_broadcast(type)
        raise NotImplemented

    @property
    @abstractmethod
    def is_user(self) -> bool:
        # return EntityType.is_user(type)
        raise NotImplemented

    @property
    @abstractmethod
    def is_group(self) -> bool:
        # return EntityType.is_group(type)
        raise NotImplemented

    #
    #   Conveniences
    #

    @classmethod
    def convert(cls, array: Iterable):  # -> List[ID]:
        """
        Convert ID list from string array

        :param array: string array
        :return: ID list
        """
        members = []
        for item in array:
            did = cls.parse(identifier=item)
            if did is None:
                # id error
                continue
            members.append(did)
        return members

    @classmethod
    def revert(cls, identifiers: Iterable) -> List[str]:
        """
        Revert ID list to string array

        :param identifiers: ID list
        :return: string array
        """
        array = []
        for did in identifiers:
            assert isinstance(did, ID), 'ID error: %s' % did
            array.append(str(did))
        return array

    #
    #   Factory methods
    #

    @classmethod
    def generate(cls, meta, network: int = None, terminal: Optional[str] = None):  # -> ID:
        helper = id_helper()
        return helper.generate_identifier(meta=meta, network=network, terminal=terminal)

    @classmethod
    def create(cls, name: Optional[str], address: Address, terminal: Optional[str] = None):  # -> ID:
        helper = id_helper()
        return helper.create_identifier(name=name, address=address, terminal=terminal)

    @classmethod
    def parse(cls, identifier: Any):  # -> Optional[ID]:
        helper = id_helper()
        return helper.parse_identifier(identifier=identifier)

    @classmethod
    def get_factory(cls):  # -> Optional[IDFactory]:
        helper = id_helper()
        return helper.get_identifier_factory()

    @classmethod
    def set_factory(cls, factory):
        helper = id_helper()
        helper.set_identifier_factory(factory=factory)


def id_helper():
    helper = AccountExtensions.id_helper
    assert isinstance(helper, IdentifierHelper), 'ID helper error: %s' % helper
    return helper


class IDFactory(ABC):
    """ ID Factory """

    @abstractmethod
    def generate_identifier(self, meta, network: Optional[int], terminal: Optional[str]) -> ID:
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


########################
#                      #
#   Plugins: Helpers   #
#                      #
########################


class IdentifierHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_identifier_factory(self, factory: IDFactory):
        raise NotImplemented

    @abstractmethod
    def get_identifier_factory(self) -> Optional[IDFactory]:
        raise NotImplemented

    @abstractmethod
    def generate_identifier(self, meta, network: Optional[int], terminal: Optional[str]) -> ID:
        raise NotImplemented

    @abstractmethod
    def create_identifier(self, name: Optional[str], address: Address, terminal: Optional[str]) -> ID:
        raise NotImplemented

    @abstractmethod
    def parse_identifier(self, identifier: Any) -> Optional[ID]:
        raise NotImplemented
