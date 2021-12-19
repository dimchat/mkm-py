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

from .crypto import *

from .types import NetworkType, MetaType
from .address import Address, AddressFactory
from .address_impl import BaseAddressFactory
from .address_impl import ANYWHERE, EVERYWHERE
from .identifier import ID
from .id_impl import ANYONE, EVERYONE, FOUNDER
from .meta import Meta, MetaFactory
from .meta_impl import BaseMeta
from .tai_doc import Document, DocumentFactory
from .tai_docs import Visa, Bulletin
from .profile import BaseDocument, BaseVisa, BaseBulletin

name = "MingKeMing"

__author__ = 'Albert Moky'

__all__ = [

    'NetworkType', 'MetaType',
    'Address', 'AddressFactory', 'BaseAddressFactory',
    'ANYWHERE', 'EVERYWHERE',
    'ID', 'ANYONE', 'EVERYONE', 'FOUNDER',
    'Meta', 'BaseMeta',
    'MetaFactory',
    'DocumentFactory',
    'Document', 'BaseDocument',
    'Visa', 'BaseVisa',
    'Bulletin', 'BaseBulletin',
]
