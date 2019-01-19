# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized user identity authentication
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

from mkm.crypto import SymmetricKey, PrivateKey, PublicKey
from mkm.cryptokeys import AESKey, RSAPrivateKey, RSAPublicKey
from mkm.address import NetworkID, Address
from mkm.meta import Meta
from mkm.entity import ID, Entity
from mkm.account import Account, User
from mkm.group import Group

name = "MingKeMing"

__author__ = 'Albert Moky'

__all__ = [
    # Crypto
    'SymmetricKey',
    'PrivateKey', 'PublicKey',

    # MingKeMing
    'NetworkID', 'Address', 'ID', 'Meta',
    'Entity',
    'Account', 'User',
    'Group',
]
