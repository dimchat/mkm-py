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
from typing import Optional, Union, Any, Dict

from ..types import Mapper, Wrapper

from .factories import Factories
from .identifier import ID
from .tai import TAI


class Document(TAI, Mapper, ABC):

    #
    #  Document types
    #
    VISA = 'visa'          # for login/communication
    PROFILE = 'profile'    # for user info
    BULLETIN = 'bulletin'  # for group info

    @property
    @abstractmethod
    def type(self) -> str:
        """
        Get document type

        :return: doc type
        """
        raise NotImplemented

    @property
    @abstractmethod
    def identifier(self) -> ID:
        """
        Get entity ID

        :return: Entity ID
        """
        raise NotImplemented

    @property
    @abstractmethod
    def time(self) -> float:
        """
        Get sign time

        :return: timestamp
        """
        raise NotImplemented

    #
    #  properties getter/setter
    #
    @property
    @abstractmethod
    def name(self) -> str:
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
    #   Factory Methods
    #

    @classmethod
    def create(cls, doc_type: str, identifier: ID, data: Optional[str] = None, signature: Union[bytes, str] = None):
        factory = cls.factory(doc_type=doc_type)
        assert isinstance(factory, DocumentFactory), 'doc_type not support: %s, %s' % (doc_type, factory)
        return factory.create_document(identifier=identifier, data=data, signature=signature)

    @classmethod
    def parse(cls, document: Any):  # -> Optional[Document]:
        if document is None:
            return None
        elif isinstance(document, Document):
            return document
        info = Wrapper.get_dictionary(document)
        # assert info is not None, 'document error: %s' % key
        doc_type = document_type(document=info)
        factory = cls.factory(doc_type=doc_type)
        if factory is None:
            factory = cls.factory(doc_type='*')  # unknown
        # assert isinstance(factory, DocumentFactory), 'document factory error: %s' % factory
        return factory.parse_document(document=info)

    @classmethod
    def register(cls, doc_type: str, factory):
        Factories.document_factories[doc_type] = factory

    @classmethod
    def factory(cls, doc_type: str):  # -> Optional[DocumentFactory]:
        return Factories.document_factories.get(doc_type)


def document_type(document: Dict[str, Any]) -> str:
    return document.get('type')


class DocumentFactory(ABC):

    @abstractmethod
    def create_document(self, identifier: ID, data: Optional[str], signature: Union[bytes, str, None]) -> Document:
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
    def parse_document(self, document: Dict[str, Any]) -> Optional[Document]:
        """
        Parse map object to entity document

        :param document:
        :return:
        """
        raise NotImplemented
