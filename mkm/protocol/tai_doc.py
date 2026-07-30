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
from typing import Optional, Any, List
from typing import Iterable

from ..types import DateTime
from ..types import StrMap, MutableStrMap
from ..types import Mapper
from ..format import TransportableData

from .tai import TAI
from .entity import shared_account_extensions


class Document(TAI, Mapper, ABC):
    """
        User/Group Profile
        ~~~~~~~~~~~~~~~~~~
        This class is used to generate entity profile

            data format: {
                "did"       : "{EntityID}",      // entity ID
                "type"      : "visa",            // "bulletin", ...
                "data"      : "{JSON}",          // data = json_encode(info)
                "signature" : "{BASE64_ENCODE}"  // signature = sign(data, SK);
            }
    """

    @property
    @abstractmethod
    def time(self) -> Optional[DateTime]:
        """
        Get signature time from properties (data)

        :return: timestamp
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.time getter'
        )

    #
    #   Conveniences
    #

    @classmethod
    def convert(cls, array: Iterable):  # -> List[Document]:
        documents = []
        for item in array:
            doc = cls.parse(document=item)
            if doc is None:
                # document error
                continue
            documents.append(doc)
        return documents

    @classmethod
    def revert(cls, documents: Iterable) -> List[MutableStrMap]:
        array = []
        for doc in documents:
            assert isinstance(doc, Document), f'document error: {doc}'
            array.append(doc.to_map())
        return array

    #
    #   Factory Methods
    #

    @classmethod
    def create(cls, doc_type: str, data: str = None, signature: TransportableData = None):  # -> Document:
        helper = doc_helper()
        return helper.create_document(doc_type, data=data, signature=signature)

    @classmethod
    def parse(cls, document: Any):  # -> Optional[Document]:
        helper = doc_helper()
        return helper.parse_document(document)

    @classmethod
    def get_factory(cls, doc_type: str):  # -> Optional[DocumentFactory]:
        helper = doc_helper()
        return helper.get_document_factory(doc_type)

    @classmethod
    def set_factory(cls, doc_type: str, factory):
        helper = doc_helper()
        helper.set_document_factory(doc_type, factory=factory)


class DocumentFactory(ABC):
    """ Document Factory """

    @abstractmethod
    def create_document(self, data: Optional[str], signature: Optional[TransportableData]) -> Document:
        """
        1. Create a new empty document with entity ID

        2. Create document with data & signature loaded from local storage

        :param data:       document data
        :param signature:  document signature
        :return: Document
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_document()'
        )

    @abstractmethod
    def parse_document(self, document: StrMap) -> Optional[Document]:
        """
        Parse map object to entity document

        :param document:
        :return:
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_document()'
        )


# -----------------------------------------------------------------------------
#  Account Extensions
# -----------------------------------------------------------------------------


class DocumentHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_document_factory(self, doc_type: str, factory: DocumentFactory):
        """ Set document factory for type """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_document_factory()'
        )

    @abstractmethod
    def get_document_factory(self, doc_type: str) -> Optional[DocumentFactory]:
        """ Get document factory for type """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_document_factory()'
        )

    @abstractmethod
    def create_document(self, doc_type: str, data: Optional[str], signature: Optional[TransportableData]) -> Document:
        """ Create document with data and signature for type """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_document()'
        )

    @abstractmethod
    def parse_document(self, document: Any) -> Optional[Document]:
        """ Parse any object to document """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_document()'
        )


class DocumentExtension:

    @property
    def doc_helper(self) -> Optional[DocumentHelper]:
        """ Get document helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.doc_helper getter'
        )

    @doc_helper.setter
    def doc_helper(self, helper: DocumentHelper):
        """ Set document helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.doc_helper setter'
        )


shared_account_extensions.doc_helper: Optional[DocumentHelper] = None


def account_extensions() -> DocumentExtension:
    return shared_account_extensions


def doc_helper() -> DocumentHelper:
    ext = account_extensions()
    return ext.doc_helper
