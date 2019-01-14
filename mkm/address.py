#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

from mkm.utils import sha256, ripemd160, base58_encode, base58_decode


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
            where the owner can share informations and interact with its friends.
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
    # Person Account
    Main = 0x08         # 0000 1000 (Person)

    # Virtual Groups
    Group = 0x10        # 0001 0000 (Multi-Persons)
    Polylogue = 0x10    # 0001 0000 (Multi-Persons Chat, N < 100)
    Chatroom = 0x30     # 0011 0000 (Multi-Persons Chat, N >= 100)

    # Network
    Provider = 0x76     # 0111 0110 (Service Provider)
    Station = 0x88      # 1000 1000 (Server Node)

    # Internet of Things
    Thing = 0x80        # 1000 0000 (IoT)
    Robot = 0xC8        # 1100 1000

    def is_communicator(self):
        return self.value & self.Main

    def is_person(self):
        return self.value == self.Main

    def is_group(self):
        return self.value & self.Group

    def is_station(self):
        return self.value == self.Station

    def is_provider(self):
        return self.value == self.Provider

    def is_thing(self):
        return self.value & self.Thing

    def is_robot(self):
        return self.value == self.Robot


def user_number(code: bytes) -> int:
    """ Get user number, which for remembering and searching user """
    return int.from_bytes(code, byteorder='little')


class Address(str):
    """
        This class is used to build address for ID
    """

    network: NetworkID = 0x00
    number: int = 0

    def __new__(cls, address: str=''):
        """
        Create address object with string

        :param address: address string
        :return: Address object
        """
        if address:
            # return Address object directory
            if isinstance(address, Address):
                return address
            # get fields from string
            data = base58_decode(address)
            prefix = data[:1]
            digest = data[1:-4]
            code = data[-4:]
            network = ord(prefix)
            number = user_number(code)
        else:
            raise AssertionError('Parameter error')
        # verify
        if sha256(sha256(prefix + digest))[:4] == code:
            # new Address(str)
            self = super(Address, cls).__new__(cls, address)
            self.network = NetworkID(network)
            self.number = number
            return self
        else:
            raise ValueError('Invalid address')

    @classmethod
    def generate(cls, fingerprint: bytes, network: NetworkID, version: chr=0x01):
        """ Generate address with fingerprint and network ID """
        if version == 0x01 and fingerprint and network:
            # calculate address string with fingerprint
            prefix = chr(network).encode('utf-8')
            digest = ripemd160(sha256(fingerprint))
            code = sha256(sha256(prefix + digest))[:4]
            string = base58_encode(prefix + digest + code)
            return Address(string)
        else:
            raise AssertionError('Parameters error')
