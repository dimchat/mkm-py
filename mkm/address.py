# -*- coding: utf-8 -*-
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

from enum import IntEnum

from .utils import sha256, ripemd160, base58_encode, base58_decode


class NetworkID(IntEnum):
    """
        @enum MKMNetworkID

        @abstract A network type to indicate what kind the entity is.

        @discussion An address can identify a person, a group of people,
            a team, even a thing.

            MKMNetwork_Main indicates this entity is a person's account.
            An account should have a public key, which proved by meta data.

            MKMNetwork_Group indicates this entity is a group of people,
            which should have a founder (also the owner), and some members.

            MKMNetwork_Moments indicates a special personal social network,
            where the owner can share information and interact with its friends.
            The owner is the king here, it can do anything and no one can stop it.

            MKMNetwork_Polylogue indicates a virtual (temporary) social network.
            It's created to talk with multi-people (but not too much, e.g. < 100).
            Any member can invite people in, but only the founder can expel member.

            MKMNetwork_Chatroom indicates a massive (persistent) social network.
            It's usually more than 100 people in it, so we need administrators
            to help the owner to manage the group.

            MKMNetwork_SocialEntity indicates this entity is a social entity.

            MKMNetwork_Organization indicates an independent organization.

            MKMNetwork_Company indicates this entity is a company.

            MKMNetwork_School indicates this entity is a school.

            MKMNetwork_Government indicates this entity is a government department.

            MKMNetwork_Department indicates this entity is a department.

            MKMNetwork_Thing this is reserved for IoT (Internet of Things).

        Bits:
            0000 0001 - this entity's branch is independent (clear division).
            0000 0010 - this entity can contains other group (big organization).
            0000 0100 - this entity is top organization.
            0000 1000 - (Main) this entity acts like a human.

            0001 0000 - this entity contains members (Group)
            0010 0000 - this entity needs other administrators (big organization)
            0100 0000 - this is an entity in reality.
            1000 0000 - (IoT) this entity is a 'Thing'.

            (All above are just some advices to help choosing numbers :P)
    """
    ################################
    #  BTC Network
    ################################
    BTCMain = 0x00      # 0000 0000 (BitCoin Address)
    # BTCTest = 0x6f    # 0110 1111 (BitCoin Test)

    ################################
    #  Person Account
    ################################
    Main = 0x08         # 0000 1000 (Person)

    ################################
    #  Virtual Groups
    ################################
    Group = 0x10        # 0001 0000 (Multi-Persons)
    # Moments = 0x18    # 0001 1000 (Twitter)
    Polylogue = 0x10    # 0001 0000 (Multi-Persons Chat, N < 100)
    Chatroom = 0x30     # 0011 0000 (Multi-Persons Chat, N >= 100)

    ################################
    #  Social Entities in Reality
    ################################
    # SocialEntity = 0x50  # 0101 0000
    # Organization = 0x74  # 0111 0100
    # Company = 0x76       # 0111 0110
    # School = 0x77        # 0111 0111
    # Government = 0x73    # 0111 0011
    # Department = 0x52    # 0101 0010

    ################################
    #  Network
    ################################
    Provider = 0x76        # 0111 0110 (Service Provider)
    Station = 0x88         # 1000 1000 (Server Node)

    ################################
    #  Internet of Things
    ################################
    Thing = 0x80           # 1000 0000 (IoT)
    Robot = 0xC8           # 1100 1000

    def is_communicator(self) -> bool:
        return (self.value & self.Main) or (self.value == self.BTCMain)

    def is_person(self) -> bool:
        return (self.value == self.Main) or (self.value == self.BTCMain)

    def is_group(self) -> bool:
        return self.value & self.Group

    def is_station(self) -> bool:
        return self.value == self.Station

    def is_provider(self) -> bool:
        return self.value == self.Provider

    def is_thing(self) -> bool:
        return self.value & self.Thing

    def is_robot(self) -> bool:
        return self.value == self.Robot


def user_number(code: bytes) -> int:
    """ Get user number, which for remembering and searching user """
    return int.from_bytes(code, byteorder='little')


class Address(str):
    """
        This class is used to build address for ID
    """

    Algorithm_BTC = 0x01
    DefaultAlgorithm = Algorithm_BTC

    def __new__(cls, address: str='',
                fingerprint: bytes=None, network: NetworkID=0, algorithm: chr=DefaultAlgorithm):
        """
        Create address object with string

        :param address: address string
        :return: Address object
        """
        if address:
            # return Address object directly
            if isinstance(address, Address):
                return address
            # get fields from string
            data = base58_decode(address)
            if len(data) == 25:
                prefix = data[:1]
                digest = data[1:-4]
                code = data[-4:]
                if sha256(sha256(prefix + digest))[:4] == code:
                    network = ord(prefix)
                    number = user_number(code)
                    # algorithm = cls.Algorithm_BTC
                else:
                    raise ValueError('Address check code error')
            else:
                raise ValueError('Address length error')
        elif algorithm == cls.Algorithm_BTC and fingerprint:
            # calculate address string with fingerprint
            prefix = chr(network).encode('latin1')
            digest = ripemd160(sha256(fingerprint))
            code = sha256(sha256(prefix + digest))[:4]
            number = user_number(code)
            address = base58_encode(prefix + digest + code)
        else:
            raise AssertionError('Parameter error')
        # new Address(str)
        self = super().__new__(cls, address)
        self.network = NetworkID(network)
        self.number = number
        # self.algorithm = algorithm
        return self
