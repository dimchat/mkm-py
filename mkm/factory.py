# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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

from typing import Optional, Iterable, Any, List, Dict

from .types import Converter
from .types import Wrapper
from .format import TransportableData
from .crypto import SignKey, VerifyKey

from .protocol import Address, AddressFactory
from .protocol import ID, IDFactory
from .protocol import Meta, MetaFactory
from .protocol import Document, DocumentFactory


class AccountGeneralFactory:

    def __init__(self):
        super().__init__()
        # AddressFactory
        self.__address_factory: Optional[AddressFactory] = None
        # IDFactory
        self.__id_factory: Optional[IDFactory] = None
        # str(type) -> MetaFactory
        self.__meta_factories: Dict[str, MetaFactory] = {}
        # str(type) -> DocumentFactory
        self.__document_factories: Dict[str, DocumentFactory] = {}

    #
    #   Address
    #

    def set_address_factory(self, factory: AddressFactory):
        self.__address_factory = factory

    def get_address_factory(self) -> Optional[AddressFactory]:
        return self.__address_factory

    def generate_address(self, meta: Meta, network: int = None) -> Address:
        factory = self.get_address_factory()
        assert factory is not None, 'address factory not set'
        return factory.generate_address(meta=meta, network=network)

    def create_address(self, address: str) -> Optional[Address]:
        factory = self.get_address_factory()
        assert factory is not None, 'address factory not set'
        return factory.create_address(address=address)

    def parse_address(self, address: Any) -> Optional[Address]:
        if address is None:
            return None
        elif isinstance(address, Address):
            return address
        string = Wrapper.get_str(address)
        assert string is not None, 'address error: %s' % address
        factory = self.get_address_factory()
        assert factory is not None, 'address factory not set'
        return factory.parse_address(address=string)

    #
    #   ID
    #

    def set_identifier_factory(self, factory: IDFactory):
        self.__id_factory = factory

    def get_identifier_factory(self) -> Optional[IDFactory]:
        return self.__id_factory

    def generate_identifier(self, meta: Meta, network: Optional[int], terminal: Optional[str]) -> ID:
        factory = self.get_identifier_factory()
        assert factory is not None, 'ID factory not set'
        return factory.generate_identifier(meta=meta, network=network, terminal=terminal)

    def create_identifier(self, name: Optional[str], address: Address, terminal: Optional[str]) -> ID:
        factory = self.get_identifier_factory()
        assert factory is not None, 'ID factory not set'
        return factory.create_identifier(name=name, address=address, terminal=terminal)

    def parse_identifier(self, identifier: Any) -> Optional[ID]:
        if identifier is None:
            return None
        elif isinstance(identifier, ID):
            return identifier
        string = Wrapper.get_str(identifier)
        assert string is not None, 'ID error: %s' % identifier
        factory = self.get_identifier_factory()
        assert factory is not None, 'ID factory not set'
        return factory.parse_identifier(identifier=string)

    def convert_identifiers(self, array: Iterable) -> List[ID]:
        """
        Convert ID list from string array

        :param array: ID string array
        :return: ID list
        """
        result = []
        for item in array:
            identifier = self.parse_identifier(identifier=item)
            if identifier is None:
                # id error
                continue
            result.append(identifier)
        return result

    # noinspection PyMethodMayBeStatic
    def revert_identifiers(self, array: Iterable[ID]) -> List[str]:
        """
        Revert ID list to string array

        :param array: ID list
        :return: string array
        """
        result = []
        for item in array:
            result.append(str(item))
        return result

    #
    #   Meta
    #

    def set_meta_factory(self, version: str, factory: MetaFactory):
        self.__meta_factories[version] = factory

    def get_meta_factory(self, version: str) -> Optional[MetaFactory]:
        return self.__meta_factories.get(version)

    # noinspection PyMethodMayBeStatic
    def get_meta_type(self, meta: Dict[str, Any], default: Optional[str]) -> Optional[str]:
        """ get meta type(version) """
        value = meta.get('type')
        return Converter.get_str(value=value, default=default)

    # def has_meta_seed(self, meta: Dict[str, Any]) -> bool:
    #     version = self.get_meta_type(meta=meta, default='')
    #     return version == '1' or type == 'MKM'
    #
    # def get_meta_seed(self, meta: Dict[str, Any]) -> Optional[str]:
    #     if self.has_meta_seed(meta=meta):
    #         value = meta.get('seed')
    #         return Converter.get_str(value=value, default='')

    def generate_meta(self, version: str, private_key: SignKey,
                      seed: Optional[str]) -> Meta:
        factory = self.get_meta_factory(version)
        assert factory is not None, 'failed to get meta factory: %d' % version
        return factory.generate_meta(private_key, seed=seed)

    def create_meta(self, version: str, public_key: VerifyKey,
                    seed: Optional[str], fingerprint: Optional[TransportableData]) -> Meta:
        factory = self.get_meta_factory(version)
        assert factory is not None, 'failed to get meta factory: %d' % version
        return factory.create_meta(public_key, seed=seed, fingerprint=fingerprint)

    def parse_meta(self, meta: Any) -> Optional[Meta]:
        if meta is None:
            return None
        elif isinstance(meta, Meta):
            return meta
        info = Wrapper.get_dict(meta)
        if info is None:
            # assert False, 'meta error: %s' % meta
            return None
        version = self.get_meta_type(meta=info, default='*')
        factory = self.get_meta_factory(version)
        if factory is None:
            factory = self.get_meta_factory('*')  # unknown
            assert factory is not None, 'default meta factory not found'
        return factory.parse_meta(meta=info)

    #
    #   Document
    #

    def set_document_factory(self, doc_type: str, factory: DocumentFactory):
        self.__document_factories[doc_type] = factory

    def get_document_factory(self, doc_type: str) -> Optional[DocumentFactory]:
        return self.__document_factories.get(doc_type)

    # noinspection PyMethodMayBeStatic
    def get_document_type(self, document: Dict[str, Any], default: Optional[str]) -> Optional[str]:
        value = document.get('type')
        return Converter.get_str(value=value, default=default)

    def create_document(self, doc_type: str, identifier: ID,
                        data: Optional[str], signature: Optional[TransportableData]) -> Document:
        factory = self.get_document_factory(doc_type)
        assert factory is not None, 'document factory not found for type: %s' % doc_type
        return factory.create_document(identifier=identifier, data=data, signature=signature)

    def parse_document(self, document: Any) -> Optional[Document]:
        if document is None:
            return None
        elif isinstance(document, Document):
            return document
        info = Wrapper.get_dict(document)
        if info is None:
            # assert False, 'document error: %s' % document
            return None
        doc_type = self.get_document_type(document=info, default='*')
        factory = self.get_document_factory(doc_type)
        if factory is None:
            assert doc_type != '*', 'document factory not ready: %s' % document
            factory = self.get_document_factory('*')  # unknown
            assert factory is not None, 'default document factory not found'
        return factory.parse_document(document=info)


# Singleton
class AccountFactoryManager:

    general_factory = AccountGeneralFactory()
