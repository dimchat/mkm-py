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

from typing import Optional, Union, Any, List, Dict

from ..types import Wrapper
from ..crypto import SignKey, VerifyKey
from ..crypto import utf8_encode
from ..protocol import Address, AddressFactory
from ..protocol import ID, IDFactory
from ..protocol import Meta, MetaType, MetaFactory
from ..protocol import meta_has_seed
from ..protocol import Document, DocumentFactory


class GeneralFactory:

    def __init__(self):
        super().__init__()
        # AddressFactory
        self.__address_factory: Optional[AddressFactory] = None
        # IDFactory
        self.__id_factory: Optional[IDFactory] = None
        # int(type) -> MetaFactory
        self.__meta_factories: Dict[int, MetaFactory] = {}
        # str(type) -> DocumentFactory
        self.__document_factories: Dict[str, DocumentFactory] = {}

    #
    #   Address
    #

    def set_address_factory(self, factory: AddressFactory):
        self.__address_factory = factory

    def get_address_factory(self) -> Optional[AddressFactory]:
        return self.__address_factory

    def generate_address(self, meta: Meta, network: int) -> Optional[Address]:
        factory = self.get_address_factory()
        # assert factory is not None, 'address factory not set'
        return factory.generate_address(meta=meta, network=network)

    def create_address(self, address: str) -> Optional[AddressFactory]:
        factory = self.get_address_factory()
        # assert factory is not None, 'address factory not set'
        return factory.create_address(address=address)

    def parse_address(self, address: Any) -> Optional[Address]:
        if address is None:
            return None
        elif isinstance(address, Address):
            return address
        string = Wrapper.get_string(address)
        # assert string is not None, 'address error: %s' % address
        factory = self.get_address_factory()
        # assert factory is not None, 'address factory not set'
        return factory.parse_address(address=string)

    #
    #   ID
    #

    def set_id_factory(self, factory: IDFactory):
        self.__id_factory = factory

    def get_id_factory(self) -> Optional[IDFactory]:
        return self.__id_factory

    def generate_id(self, meta: Meta, network: int, terminal: Optional[str] = None) -> Optional[ID]:
        factory = self.get_id_factory()
        # assert factory is not None, 'ID factory not set'
        return factory.generate_id(meta=meta, network=network, terminal=terminal)

    def create_id(self, name: Optional[str], address: Address, terminal: Optional[str] = None) -> ID:
        factory = self.get_id_factory()
        # assert factory is not None, 'ID factory not set'
        return factory.create_id(name=name, address=address, terminal=terminal)

    def parse_id(self, identifier: Any) -> Optional[ID]:
        if identifier is None:
            return None
        elif isinstance(identifier, ID):
            return identifier
        string = Wrapper.get_string(identifier)
        # assert string is not None, 'ID error: %s' % identifier
        factory = self.get_id_factory()
        # assert factory is not None, 'ID factory not set'
        return factory.parse_id(identifier=string)

    def convert_id_list(self, array: List[str]) -> List[ID]:
        """
        Convert ID list from string array

        :param array: ID string array
        :return: ID list
        """
        result = []
        for item in array:
            identifier = self.parse_id(identifier=item)
            if identifier is None:
                # id error
                continue
            result.append(identifier)
        return result

    # noinspection PyMethodMayBeStatic
    def revert_id_list(self, array: List[ID]) -> List[str]:
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

    def set_meta_factory(self, version: Union[MetaType, int], factory):
        if isinstance(version, MetaType):
            version = version.value
        self.__meta_factories[version] = factory

    def get_meta_factory(self, version: Union[MetaType, int]) -> Optional[MetaFactory]:
        if isinstance(version, MetaType):
            version = version.value
        return self.__meta_factories.get(version)

    # noinspection PyMethodMayBeStatic
    def get_meta_type(self, meta: Dict[str, Any]) -> int:
        """ get meta type(version) """
        version = meta.get('type')
        if version is None:
            version = meta.get('version')
        return 0 if version is None else int(version)

    # noinspection PyMethodMayBeStatic
    def meta_has_seed(self, version: int) -> bool:
        return (version & MetaType.MKM) == MetaType.MKM

    def generate_meta(self, version: Union[MetaType, int], key: SignKey,
                      seed: Optional[str] = None) -> Meta:
        factory = self.get_meta_factory(version=version)
        # assert factory is not None, 'failed to get meta factory: %d' % version
        return factory.generate_meta(key=key, seed=seed)

    def create_meta(self, version: Union[MetaType, int], key: VerifyKey,
                    seed: Optional[str] = None, fingerprint: Union[bytes, str, None] = None) -> Meta:
        factory = self.get_meta_factory(version=version)
        # assert factory is not None, 'failed to get meta factory: %d' % version
        return factory.create_meta(key=key, seed=seed, fingerprint=fingerprint)

    def parse_meta(self, meta: Any) -> Optional[Meta]:
        if meta is None:
            return None
        elif isinstance(meta, Meta):
            return meta
        info = Wrapper.get_dictionary(meta)
        # assert info is not None, 'meta error: %s' % meta
        version = self.get_meta_type(meta=info)
        factory = self.get_meta_factory(version=version)
        if factory is None:
            factory = self.get_meta_factory(version=0)  # unknown
            # assert factory is not None, 'meta factory not found: %d' % version
        return factory.parse_meta(meta=info)

    # noinspection PyMethodMayBeStatic
    def check_meta(self, meta: Meta) -> bool:
        key = meta.key
        # meta.key should not be empty
        if isinstance(key, VerifyKey):
            if meta_has_seed(version=meta.type):
                # check seed with signature
                seed = meta.seed
                fingerprint = meta.fingerprint
                # seed and fingerprint should not be empty
                if seed is not None and fingerprint is not None:
                    # verify fingerprint
                    return key.verify(data=utf8_encode(string=seed), signature=fingerprint)
            else:
                # this meta has no seed, so no signature too
                return True

    # noinspection PyMethodMayBeStatic
    def meta_match_id(self, meta: Meta, identifier: ID) -> bool:
        """ Check whether meta match with entity ID
            (must call this when received a new meta from network) """
        # check ID.name
        if meta.seed == identifier.name:
            # check ID.address
            old = identifier.address
            gen = Address.generate(meta=meta, network=old.type)
            return old == gen

    # noinspection PyMethodMayBeStatic
    def meta_match_key(self, meta: Meta, key: VerifyKey) -> bool:
        """ Check whether meta match with public key """
        if key == meta.key:
            # NOTICE: ID with BTC/ETH address has no username, so
            #         just compare the key.data to check matching
            return True
        # check with seed & fingerprint
        if meta_has_seed(version=meta.type):
            # check whether keys equal by verifying signature
            seed = utf8_encode(string=meta.seed)
            fingerprint = meta.fingerprint
            return key.verify(data=seed, signature=fingerprint)

    #
    #   Document
    #

    def set_document_factory(self, doc_type: str, factory):
        self.__document_factories[doc_type] = factory

    def get_document_factory(self, doc_type: str) -> Optional[DocumentFactory]:
        return self.__document_factories.get(doc_type)

    # noinspection PyMethodMayBeStatic
    def get_document_type(self, document: Dict[str, Any]) -> str:
        return document.get('type')

    def create_document(self, doc_type: str, identifier: ID,
                        data: Optional[str] = None, signature: Union[bytes, str] = None) -> Document:
        factory = self.get_document_factory(doc_type=doc_type)
        # assert factory is not None, 'document factory not found for type: %s' % doc_type
        return factory.create_document(identifier=identifier, data=data, signature=signature)

    def parse_document(self, document: Any) -> Optional[Document]:
        if document is None:
            return None
        elif isinstance(document, Document):
            return document
        info = Wrapper.get_dictionary(document)
        # assert info is not None, 'document error: %s' % key
        doc_type = self.get_document_type(document=info)
        factory = self.get_document_factory(doc_type=doc_type)
        if factory is None:
            factory = self.get_document_factory(doc_type='*')  # unknown
            # assert factory is not None, 'document factory not found for type: %s' % doc_type
        return factory.parse_document(document=info)


# Singleton
class FactoryManager:

    general_factory = GeneralFactory()
