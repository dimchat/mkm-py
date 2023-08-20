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

from ..types import Stringer

from .address import Address


class ID(Stringer, ABC):
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
        # return self.address.is_broadcast
        raise NotImplemented

    @property
    @abstractmethod
    def is_user(self) -> bool:
        # return self.address.is_user
        raise NotImplemented

    @property
    @abstractmethod
    def is_group(self) -> bool:
        # return self.address.is_group
        raise NotImplemented

    @classmethod
    def convert(cls, array: List[str]):  # -> List[ID]:
        """
        Convert ID list from string array

        :param array: string array
        :return: ID list
        """
        gf = general_factory()
        return gf.convert_id_list(array=array)

    @classmethod
    def revert(cls, array) -> List[str]:
        """
        Revert ID list to string array

        :param array: ID list
        :return: string array
        """
        gf = general_factory()
        return gf.revert_id_list(array=array)

    #
    #   Factory methods
    #

    @classmethod
    def generate(cls, meta, network: int, terminal: Optional[str] = None):  # -> ID:
        gf = general_factory()
        return gf.generate_id(meta=meta, network=network, terminal=terminal)

    @classmethod
    def create(cls, name: Optional[str], address: Address, terminal: Optional[str] = None):  # -> ID:
        gf = general_factory()
        return gf.create_id(name=name, address=address, terminal=terminal)

    @classmethod
    def parse(cls, identifier: Any):  # -> Optional[ID]:
        gf = general_factory()
        return gf.parse_id(identifier=identifier)

    @classmethod
    def factory(cls):  # -> Optional[IDFactory]:
        gf = general_factory()
        return gf.get_id_factory()

    @classmethod
    def register(cls, factory):
        gf = general_factory()
        gf.set_id_factory(factory=factory)


def general_factory():
    from ..factory import AccountFactoryManager
    return AccountFactoryManager.general_factory


class IDFactory(ABC):

    @abstractmethod
    def generate_id(self, meta, network: int, terminal: Optional[str]) -> ID:
        """
        Generate ID

        :param meta:     meta info
        :param network:  ID.type
        :param terminal: ID.terminal
        :return: ID
        """
        raise NotImplemented

    @abstractmethod
    def create_id(self, name: Optional[str], address: Address, terminal: Optional[str]) -> ID:
        """
        Create ID

        :param name:     ID.name
        :param address:  ID.address
        :param terminal: ID.terminal
        :return: ID
        """
        raise NotImplemented

    @abstractmethod
    def parse_id(self, identifier: str) -> Optional[ID]:
        """
        Parse string object to ID

        :param identifier: ID string
        :return: ID
        """
        raise NotImplemented
