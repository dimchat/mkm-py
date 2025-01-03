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

from .entity import EntityType
from .address import Address, AddressFactory
from .identifier import ID, IDFactory
from .meta import Meta, MetaFactory
from .tai import TAI
from .tai_doc import Document, DocumentFactory

# from .address import AddressHelper
# from .identifier import IdentifierHelper
# from .meta import MetaHelper
# from .tai_doc import DocumentHelper
# from .helpers import AccountExtensions

__all__ = [

    'EntityType',
    'Address',   # 'AddressFactory',
    'ID',        # 'IDFactory',
    'Meta',      # 'MetaFactory',
    'TAI',
    'Document',  # 'DocumentFactory',

    #
    #   Plugins
    #

    # 'AddressHelper', 'IdentifierHelper',
    # 'MetaHelper', 'DocumentHelper',
    # 'AccountExtensions',

]
