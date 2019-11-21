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

from .crypto.utils import sha256, ripemd160, base58_encode, base58_decode
from .types import NetworkID


class Address(ABC):
    """This class is used to build address for ID

        Address for MKM ID
        ~~~~~~~~~~~~~~~~~~

        properties:
            network - address type
            number  - search number
    """

    def __new__(cls, address: str):
        """
        Create address object with string

        :param address: address string
        :return: Address object
        """
        if address is None:
            return None
        elif cls is Address:
            if isinstance(address, Address):
                # return Address object directly
                return address
            # Address for broadcast
            length = len(address)
            # anywhere
            if length == len(ANYWHERE) and address.lower() == ANYWHERE:
                return ANYWHERE
            # everywhere
            if length == len(EVERYWHERE) and address.lower() == EVERYWHERE:
                return EVERYWHERE
            # try to create address object
            for clazz in cls.address_classes():
                inst = clazz.__new__(clazz, address)
                if inst is not None:
                    return inst
            raise ValueError('unrecognized address: %s' % address)
        # subclass
        return super().__new__(cls, address)

    @property
    @abstractmethod
    def network(self) -> NetworkID:
        """
        Get network type of address

        :return: NetworkID
        """
        raise NotImplemented

    @property
    @abstractmethod
    def number(self) -> int:
        """
        Get search number of address

        :return: search number [0, 2^32)
        """
        raise NotImplemented

    @property
    def is_broadcast(self) -> bool:
        assert self.network is not None, 'address error: %s' % self
        value = self.network.value
        if value == NetworkID.Group.value:
            # group address
            return self == EVERYWHERE
        elif value == NetworkID.Main.value:
            # user address
            return self == ANYWHERE

    #
    #   Runtime
    #
    __address_classes = []  # class list

    @classmethod
    def register(cls, address_class) -> bool:
        """
        Register address class

        :param address_class: class for parsing ID.address
        :return: False on error
        """
        if issubclass(address_class, Address):
            cls.__address_classes.append(address_class)
        else:
            raise TypeError('%s must be subclass of Address' % address_class)
        return True

    @classmethod
    def address_classes(cls) -> list:
        """
        Get all address classes

        :return: address class list
        """
        return cls.__address_classes


"""
    Address like BitCoin
    ~~~~~~~~~~~~~~~~~~~~

    data format: "network+digest+check_code"
        network    --  1 byte
        digest     -- 20 bytes
        check_code --  4 bytes

    algorithm:
        fingerprint = sign(seed, SK);
        digest      = ripemd160(sha256(fingerprint));
        check_code  = sha256(sha256(network + digest)).prefix(4);
        address     = base58_encode(network + digest + check_code);
"""


def check_code(data: bytes) -> bytes:
    # check code in BTC address
    return sha256(sha256(data))[:4]


def user_number(code: bytes) -> int:
    # get user number, which for remembering and searching user
    return int.from_bytes(code, byteorder='little')


class DefaultAddress(str, Address):

    def __init__(self, address: str):
        if self is address:
            # no need to init again
            return
        super().__init__()
        # get fields from string
        prefix_digest_code = base58_decode(address)
        if len(prefix_digest_code) != 25:
            raise ValueError('BTC address length error: %s' % address)
        # split them
        prefix = prefix_digest_code[:1]
        digest = prefix_digest_code[1:-4]
        code = prefix_digest_code[-4:]
        # check them
        if check_code(prefix + digest) != code:
            raise ValueError('BTC address check code error: %s' % address)
        network = ord(prefix)
        self.__network = NetworkID(network)
        self.__number = user_number(code)

    @property
    def network(self) -> NetworkID:
        return self.__network

    @property
    def number(self) -> int:
        return self.__number

    #
    #   Factory
    #
    @classmethod
    def new(cls, data: bytes, network: NetworkID=0) -> Address:
        """
        Generate address with fingerprint and network ID

        :param data:    fingerprint (signature/key.data)
        :param network: address type
        :return:        Address object
        """
        prefix = chr(network).encode('latin1')
        digest = ripemd160(sha256(data))
        code = check_code(prefix + digest)
        address = base58_encode(prefix + digest + code)
        return cls(address)


# register default address class
Address.register(DefaultAddress)  # default


"""
    Address for broadcast
    ~~~~~~~~~~~~~~~~~~~~~
"""


class ConstantAddress(str, Address):

    def __new__(cls, address: str, network: NetworkID, number: int):
        self = super().__new__(cls, address)
        self.__network = network
        self.__number = number
        return self

    @property
    def network(self) -> NetworkID:
        return self.__network

    @property
    def number(self) -> int:
        return self.__number


ANYWHERE = ConstantAddress(address="anywhere", network=NetworkID.Main, number=9527)
EVERYWHERE = ConstantAddress(address="everywhere", network=NetworkID.Group, number=9527)
