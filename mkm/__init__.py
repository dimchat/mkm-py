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

from .crypto import SignKey, VerifyKey, EncryptKey, DecryptKey
from .crypto import SymmetricKey, PrivateKey, PublicKey

from .crypto import BaseCoder, Base64, Base58, Hex
from .crypto import Digest, MD5, SHA1, SHA256, RIPEMD160
from .crypto import md5, sha1, sha256, ripemd160

from .types import NetworkID, MetaVersion
from .address import Address, ANYWHERE, EVERYWHERE
from .identifier import ID, ANYONE, EVERYONE
from .meta import Meta
from .profile import Profile
from .entity import Entity
from .user import User
from .group import Group
from .delegate import EntityDataSource, UserDataSource, GroupDataSource

name = "MingKeMing"

__author__ = 'Albert Moky'

__all__ = [

    # crypto
    'SignKey', 'VerifyKey', 'EncryptKey', 'DecryptKey',
    'SymmetricKey', 'PrivateKey', 'PublicKey',

    # data
    'BaseCoder',
    'Base64', 'Base58', 'Hex',
    'Digest',
    'MD5', 'SHA1', 'SHA256', 'RIPEMD160',
    'md5', 'sha1', 'sha256', 'ripemd160',

    # entity
    'NetworkID', 'MetaVersion',
    'Address', 'ID', 'Meta', 'Profile',
    'Entity', 'User', 'Group',

    # delegate
    'EntityDataSource', 'UserDataSource', 'GroupDataSource',

    'ANYONE', 'EVERYONE', 'ANYWHERE', 'EVERYWHERE',
]
