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
from typing import Any, Optional

from ..types import Stringer

from .helpers import AccountExtensions


class Address(Stringer, ABC):
    """This class is used to build address for ID

        Address for MKM ID
        ~~~~~~~~~~~~~~~~~~

        properties:
            network - network id
    """

    @property
    @abstractmethod
    def network(self) -> int:
        """
        Get address type

        :return: 0 ~ 255
        """
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def generate(cls, meta, network: int = None):  # -> Address:
        helper = address_helper()
        return helper.generate_address(meta=meta, network=network)

    @classmethod
    def parse(cls, address: Any):  # -> Optional[Address]:
        helper = address_helper()
        return helper.parse_address(address=address)

    @classmethod
    def get_factory(cls):  # -> Optional[AddressFactory]:
        helper = address_helper()
        return helper.get_address_factory()

    @classmethod
    def set_factory(cls, factory):
        helper = address_helper()
        helper.set_address_factory(factory=factory)


def address_helper():
    helper = AccountExtensions.address_helper
    assert isinstance(helper, AddressHelper), 'address helper error: %s' % helper
    return helper


class AddressFactory(ABC):
    """ Address Factory """

    @abstractmethod
    def generate_address(self, meta, network: Optional[int]) -> Address:
        """
        Generate address with meta & type

        :param meta: meta info
        :param network: address type
        :return: Address
        """
        raise NotImplemented

    @abstractmethod
    def parse_address(self, address: str) -> Optional[Address]:
        """
        Parse string object to address

        :param address: address string
        :return: Address
        """
        raise NotImplemented


########################
#                      #
#   Plugins: Helpers   #
#                      #
########################


class AddressHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_address_factory(self, factory: AddressFactory):
        raise NotImplemented

    @abstractmethod
    def get_address_factory(self) -> Optional[AddressFactory]:
        raise NotImplemented

    @abstractmethod
    def generate_address(self, meta, network: Optional[int]) -> Address:
        raise NotImplemented

    @abstractmethod
    def parse_address(self, address: Any) -> Optional[Address]:
        raise NotImplemented
