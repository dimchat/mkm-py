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
from typing import Optional, Iterable, Any, List, Dict

from ..types import DateTime
from ..types import Mapper
from ..format import TransportableData

from .identifier import ID
from .tai import TAI
from .helpers import AccountExtensions


class Document(TAI, Mapper, ABC):
    """
        User/Group Profile
        ~~~~~~~~~~~~~~~~~~
        This class is used to generate entity profile

            data format: {
                did       : "{EntityID}",      // entity ID
                type      : "visa",            // "bulletin", ...
                data      : "{JSON}",          // data = json_encode(info)
                signature : "{BASE64_ENCODE}"  // signature = sign(data, SK);
            }
    """

    @property
    @abstractmethod
    def identifier(self) -> ID:
        """
        Get entity ID

        :return: Entity ID
        """
        raise NotImplemented

    #
    #  properties getter/setter
    #

    @property
    @abstractmethod
    def time(self) -> Optional[DateTime]:
        """
        Get sign time

        :return: timestamp
        """
        raise NotImplemented

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """
        Get entity name

        :return: name string
        """
        raise NotImplemented

    @name.setter
    @abstractmethod
    def name(self, string: str):
        """
        Set entity name

        :param string: name string
        :return:
        """
        raise NotImplemented

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
    def revert(cls, documents: Iterable) -> List[Dict]:
        array = []
        for doc in documents:
            assert isinstance(doc, Document), 'document error: %s' % doc
            array.append(doc.dictionary)
        return array

    #
    #   Factory Methods
    #

    @classmethod
    def create(cls, doc_type: str, identifier: ID,
               data: str = None, signature: TransportableData = None):  # -> Document:
        helper = doc_helper()
        return helper.create_document(doc_type, identifier=identifier, data=data, signature=signature)

    @classmethod
    def parse(cls, document: Any):  # -> Optional[Document]:
        helper = doc_helper()
        return helper.parse_document(document=document)

    @classmethod
    def get_factory(cls, doc_type: str):  # -> Optional[DocumentFactory]:
        helper = doc_helper()
        return helper.get_document_factory(doc_type)

    @classmethod
    def set_factory(cls, doc_type: str, factory):
        helper = doc_helper()
        helper.set_document_factory(doc_type, factory=factory)


def doc_helper():
    helper = AccountExtensions.doc_helper
    assert isinstance(helper, DocumentHelper), 'document helper error: %s' % helper
    return helper


class DocumentFactory(ABC):
    """ Document Factory """

    @abstractmethod
    def create_document(self, identifier: ID, data: Optional[str], signature: Optional[TransportableData]) -> Document:
        """
        1. Create a new empty document with entity ID

        2. Create document with data & signature loaded from local storage

        :param identifier: entity ID
        :param data:       document data
        :param signature:  document signature
        :return: Document
        """
        raise NotImplemented

    @abstractmethod
    def parse_document(self, document: Dict) -> Optional[Document]:
        """
        Parse map object to entity document

        :param document:
        :return:
        """
        raise NotImplemented


########################
#                      #
#   Plugins: Helpers   #
#                      #
########################


class DocumentHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_document_factory(self, doc_type: str, factory: DocumentFactory):
        raise NotImplemented

    @abstractmethod
    def get_document_factory(self, doc_type: str) -> Optional[DocumentFactory]:
        raise NotImplemented

    @abstractmethod
    def create_document(self, doc_type: str, identifier: ID,
                        data: Optional[str], signature: Optional[TransportableData]) -> Document:
        raise NotImplemented

    @abstractmethod
    def parse_document(self, document: Any) -> Optional[Document]:
        raise NotImplemented
