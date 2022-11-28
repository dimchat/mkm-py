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

from abc import ABC
from typing import Optional, Union, Dict

from ..types import ConstantString
from ..protocol import EntityType
from ..protocol import Address, AddressFactory


"""
    Address for Broadcast
    ~~~~~~~~~~~~~~~~~~~~~
"""


class BroadcastAddress(ConstantString, Address):

    def __init__(self, address: str, network: Union[int, EntityType]):
        super().__init__(string=address)
        if isinstance(network, EntityType):
            network = network.value
        self.__type = network

    @property  # Override
    def type(self) -> int:
        return self.__type

    @property  # Override
    def is_broadcast(self) -> bool:
        return True

    @property  # Override
    def is_user(self) -> bool:
        return self.type == EntityType.ANY

    @property  # Override
    def is_group(self) -> bool:
        return self.type == EntityType.EVERY


ANYWHERE = BroadcastAddress(address='anywhere', network=EntityType.ANY)
EVERYWHERE = BroadcastAddress(address='everywhere', network=EntityType.EVERY)


"""
    Base Address Factory
    ~~~~~~~~~~~~~~~~~~~~
    
    abstractmethod:
        - create_address(address)
"""


class BaseAddressFactory(AddressFactory, ABC):

    def __init__(self):
        super().__init__()
        # cache broadcast addresses
        self._addresses: Dict[str, Address] = {
            str(ANYWHERE): ANYWHERE,
            str(EVERYWHERE): EVERYWHERE,
        }

    # Override
    def generate_address(self, meta, network: int) -> Optional[Address]:
        address = meta.generate_address(network=network)
        if address is not None:
            self._addresses[str(address)] = address
        return address

    # Override
    def parse_address(self, address: str) -> Optional[Address]:
        add = self._addresses.get(address)
        if add is None:
            add = Address.create(address=address)
            if add is not None:
                self._addresses[address] = add
        return add
