# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2024 Albert Moky
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
from typing import Optional, Dict

from ..types import Singleton

from ..protocol.address import AddressHelper
from ..protocol.identifier import IdentifierHelper
from ..protocol.meta import MetaHelper
from ..protocol.tai_doc import DocumentHelper
from ..protocol.helpers import AccountExtensions


# class GeneralAccountHelper(AddressHelper, IdentifierHelper, MetaHelper, DocumentHelper, ABC):
class GeneralAccountHelper(ABC):
    """ Account GeneralFactory """

    @abstractmethod
    def get_meta_type(self, meta: Dict, default: Optional[str] = None) -> Optional[str]:
        raise NotImplemented

    @abstractmethod
    def get_document_type(self, document: Dict, default: Optional[str] = None) -> Optional[str]:
        raise NotImplemented


@Singleton
class SharedAccountExtensions:
    """ Account FactoryManager """

    def __init__(self):
        super().__init__()
        self.__helper: Optional[GeneralAccountHelper] = None

    @property
    def helper(self) -> Optional[GeneralAccountHelper]:
        return self.__helper

    @helper.setter
    def helper(self, helper: GeneralAccountHelper):
        self.__helper = helper

    #
    #   Address
    #

    @property
    def address_helper(self) -> Optional[AddressHelper]:
        return AccountExtensions.address_helper

    @address_helper.setter
    def address_helper(self, helper: AddressHelper):
        AccountExtensions.address_helper = helper

    #
    #   ID
    #

    @property
    def id_helper(self) -> Optional[IdentifierHelper]:
        return AccountExtensions.id_helper

    @id_helper.setter
    def id_helper(self, helper: IdentifierHelper):
        AccountExtensions.id_helper = helper

    #
    #   Meta
    #

    @property
    def meta_helper(self) -> Optional[MetaHelper]:
        return AccountExtensions.meta_helper

    @meta_helper.setter
    def meta_helper(self, helper: MetaHelper):
        AccountExtensions.meta_helper = helper

    #
    #   Document
    #

    @property
    def doc_helper(self) -> Optional[DocumentHelper]:
        return AccountExtensions.doc_helper

    @doc_helper.setter
    def doc_helper(self, helper: DocumentHelper):
        AccountExtensions.doc_helper = helper
