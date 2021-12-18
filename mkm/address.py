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
from typing import Optional, Dict, Any

from .crypto import String
from .types import NetworkType, network_is_user, network_is_group
from .factories import Factories


class Address(ABC):
    """This class is used to build address for ID

        Address for MKM ID
        ~~~~~~~~~~~~~~~~~~

        properties:
            network - address type
    """

    @property
    def network(self) -> int:
        """
        Get network type of address

        :return: integer as NetworkType
        """
        raise NotImplemented

    @property
    def is_broadcast(self) -> bool:
        # return isinstance(self, BroadcastAddress)
        return False

    @property
    def is_user(self) -> bool:
        return network_is_user(network=self.network)

    @property
    def is_group(self) -> bool:
        return network_is_group(network=self.network)

    #
    #   Address factory
    #
    class Factory(ABC):

        @abstractmethod
        def generate_address(self, meta, network: int):  # -> Optional[Address]:
            """
            Generate address with meta & type

            :param meta: meta info
            :param network: address type
            :return: Address
            """
            raise NotImplemented

        @abstractmethod
        def create_address(self, address: str):  # -> Optional[Address]:
            """
            Create address from string

            :param address: address string
            :return: Address
            """
            raise NotImplemented

        @abstractmethod
        def parse_address(self, address: str):  # -> Optional[Address]:
            """
            Parse string object to address

            :param address: address string
            :return: Address
            """
            raise NotImplemented

    @classmethod
    def register(cls, factory: Factory):
        Factories.address_factory = factory

    @classmethod
    def factory(cls) -> Factory:
        return Factories.address_factory

    #
    #   Factory methods
    #

    @classmethod
    def generate(cls, meta, network: int):  # -> Address:
        factory = cls.factory()
        assert factory is not None, 'address factory not ready'
        return factory.generate_address(meta=meta, network=network)

    @classmethod
    def create(cls, address: str):  # -> Address:
        factory = cls.factory()
        assert factory is not None, 'address factory not ready'
        return factory.create_address(address=address)

    @classmethod
    def parse(cls, address: Any):  # -> Optional[Address]:
        if address is None:
            return None
        elif isinstance(address, Address):
            return address
        elif isinstance(address, String):
            address = address.string
        # assert isinstance(address, str), 'address error: %s' % address
        factory = cls.factory()
        assert factory is not None, 'address factory not ready'
        return factory.parse_address(address=address)


"""
    Address for broadcast
    ~~~~~~~~~~~~~~~~~~~~~
"""


class BroadcastAddress(String, Address):

    def __init__(self, address: str, network: NetworkType):
        super().__init__(string=address)
        self.__network = network.value

    @property  # Override
    def network(self) -> int:
        return self.__network

    @property  # Override
    def is_broadcast(self) -> bool:
        return True


ANYWHERE = BroadcastAddress(address='anywhere', network=NetworkType.MAIN)
EVERYWHERE = BroadcastAddress(address='everywhere', network=NetworkType.GROUP)


"""
    Address Factory
    ~~~~~~~~~~~~~~~
"""


class AddressFactory(Address.Factory, ABC):

    def __init__(self):
        super().__init__()
        # cache broadcast addresses
        self.__addresses: Dict[str, Address] = {
            str(ANYWHERE): ANYWHERE,
            str(EVERYWHERE): EVERYWHERE,
        }

    # Override
    def generate_address(self, meta, network: int) -> Optional[Address]:
        address = meta.generate_address(network=network)
        if address is not None:
            self.__addresses[str(address)] = address
        return address

    # Override
    def parse_address(self, address: str) -> Optional[Address]:
        add = self.__addresses.get(address)
        if add is None:
            add = Address.create(address=address)
            if add is not None:
                self.__addresses[address] = add
        return add
