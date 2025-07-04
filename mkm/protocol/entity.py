# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2022 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

from enum import IntEnum


class EntityType(IntEnum):
    """
        @enum MKMEntityType

        @abstract A network ID to indicate what kind the entity is.

        @discussion An address can identify a person, a group of people,
            a team, even a thing.

            MKMEntityType_User indicates this entity is a person's account.
            An account should have a public key, which proved by meta data.

            MKMEntityType_Group indicates this entity is a group of people,
            which should have a founder (also the owner), and some members.

            MKMEntityType_Station indicates this entity is a DIM network station.

            MKMEntityType_ISP indicates this entity is a group for stations.

            MKMEntityType_Bot indicates this entity is a bot user.

            MKMEntityType_Company indicates a company for stations and/or bots.

        Bits:
            0000 0001 - group flag
            0000 0010 - node flag
            0000 0100 - bot flag
            0000 1000 - CA flag
            ...         (reserved)
            0100 0000 - customized flag
            1000 0000 - broadcast flag

            (All above are just some advices to help choosing numbers :P)
    """
    ################################
    #  Main: 0, 1
    ################################
    USER = 0x00             # 0000 0000
    GROUP = 0x01            # 0000 0001 (User Group)

    ################################
    #  Network: 2, 3
    ################################
    STATION = 0x02          # 0000 0010 (Server Node)
    ISP = 0x03              # 0000 0011 (Service Provider)
    # STATION_GROUP = 0x03  # 0000 0011

    ################################
    #  Bot: 4, 5
    ################################
    BOT = 0x04              # 0000 0100 (Business Node)
    ICP = 0x05              # 0000 0101 (Content Provider)
    # BOT_GROUP = 0x05      # 0000 0101

    ################################
    #  Management: 6, 7, 8
    ################################
    # SUPERVISOR = 0x06     # 0000 0110 (Company CEO)
    # COMPANY = 0x07        # 0000 0111 (Super Group for ISP/ICP)
    # CA = 0x08             # 0000 1000 (Certification Authority)

    ################################
    #  Customized: 64, 65
    ################################
    # APP_USER = 0x40       # 0100 0000 (Application Customized User)
    # APP_GROUP = 0x41      # 0100 0001 (Application Customized Group)

    ################################
    #  Broadcast: 128, 129
    ################################
    ANY = 0x80              # 1000 0000 (anyone@anywhere)
    EVERY = 0x81            # 1000 0001 (everyone@everywhere)

    @classmethod
    def is_user(cls, network: int) -> bool:
        return (network & cls.GROUP) == cls.USER

    @classmethod
    def is_group(cls, network: int) -> bool:
        return (network & cls.GROUP) == cls.GROUP

    @classmethod
    def is_broadcast(cls, network: int) -> bool:
        return (network & cls.ANY) == cls.ANY
