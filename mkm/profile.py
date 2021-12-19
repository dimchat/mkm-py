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

import time
from typing import Optional, Union, Any, List

from .crypto import json_encode, json_decode, utf8_encode, utf8_decode, base64_encode, base64_decode
from .crypto import Dictionary
from .crypto import PublicKey, EncryptKey, VerifyKey, SignKey

from .identifier import ID
from .tai_doc import Document, document_type
from .tai_docs import Visa, Bulletin


"""
    Base Documents
    ~~~~~~~~~~~~~~
    
    Implementations of Document/Visa/Bulletin
"""


def document_identifier(document: dict) -> ID:
    identifier = document.get('ID')
    return ID.parse(identifier=identifier)


class BaseDocument(Dictionary, Document):

    def __init__(self, document: Optional[dict] = None,
                 doc_type: Optional[str] = None, identifier: Optional[ID] = None,
                 data: Union[bytes, str, None] = None, signature: Union[bytes, str, None] = None):
        # check parameters
        if data is None:
            utf8 = None
        elif isinstance(data, bytes):
            utf8 = utf8_decode(data=data)
        else:
            assert isinstance(data, str), 'document data error: %s' % data
            utf8 = data
            data = utf8_encode(string=utf8)
        if signature is None:
            base64 = None
        elif isinstance(signature, bytes):
            base64 = base64_encode(data=signature)
        else:
            assert isinstance(signature, str), 'document signature error: %s' % signature
            base64 = signature
            signature = base64_decode(string=base64)
        properties = None
        status = 0
        if document is None:
            assert identifier is not None, 'doc ID should not be empty'
            if utf8 is None or base64 is None:
                """ Create a new empty document with ID and doc type """
                document = {
                    'ID': str(identifier),
                }
                if doc_type is not None:
                    properties = {
                        'type': doc_type,
                    }
            else:
                """ Create document with ID, data and signature loaded from local storage """
                document = {
                    'ID': str(identifier),
                    'data': utf8,
                    'signature': base64
                }
                # all documents must be verified before saving into local storage
                status = 1
        # initialize with document info
        super().__init__(dictionary=document)
        # lazy load
        self.__identifier = identifier
        self.__data = data            # JsON.encode(properties)
        self.__signature = signature  # LocalUser(identifier).sign(data)
        self.__properties = properties
        self.__status = status        # 1 for valid, -1 for invalid

    @property  # Override
    def type(self) -> str:
        doc_type = self.get_property(key='type')
        if doc_type is None:
            doc_type = document_type(document=self.dictionary)
        return doc_type

    @property  # Override
    def identifier(self) -> ID:
        if self.__identifier is None:
            self.__identifier = document_identifier(document=self.dictionary)
        return self.__identifier

    @property
    def data(self) -> Optional[bytes]:
        """
        Get serialized properties

        :return: JsON string
        """
        if self.__data is None:
            utf8 = self.get('data')
            if utf8 is not None:
                self.__data = utf8_encode(string=utf8)
        return self.__data

    @property
    def signature(self) -> Optional[bytes]:
        """
        Get signature for serialized properties

        :return: signature data
        """
        if self.__signature is None:
            base64 = self.get('signature')
            if base64 is not None:
                self.__signature = base64_decode(string=base64)
        return self.__signature

    @property  # Override
    def valid(self) -> bool:
        return self.__status > 0

    #
    #  signature
    #

    # Override
    def verify(self, public_key: VerifyKey) -> bool:
        """
        Verify 'data' and 'signature' with public key

        :param public_key: public key in meta.key
        :return: True on signature matched
        """
        if self.__status > 0:
            # already verify OK
            return True
        data = self.data
        signature = self.signature
        if data is None:
            # NOTICE: if data is empty, signature should be empty at the same time
            #         this happen while profile not found
            if signature is None:
                self.__status = 0
            else:
                # data signature error
                self.__status = -1
        elif signature is None:
            # signature error
            self.__status = -1
        elif public_key.verify(data=data, signature=signature):
            # signature matched
            self.__status = 1
        # NOTICE: if status is 0, it doesn't mean the profile is invalid,
        #         try another key
        return self.__status == 1

    # Override
    def sign(self, private_key: SignKey) -> bytes:
        """
        Encode properties to 'data' and sign it to 'signature'

        :param private_key: private key match meta.key
        :return: signature
        """
        if self.__status > 0:
            # already signed/verified
            return self.__signature
        # update sign time
        self.set_property(key='time', value=int(time.time()))
        # update status
        self.__status = 1
        # sign
        self.__data = json_encode(self.properties)
        self.__signature = private_key.sign(data=self.__data)
        self['data'] = utf8_decode(data=self.__data)  # JsON string
        self['signature'] = base64_encode(data=self.__signature)
        return self.__signature

    #
    #  properties
    #

    @property  # Override
    def properties(self) -> Optional[dict]:
        """ Load properties from data """
        if self.__status < 0:
            # invalid
            return None
        if self.__properties is None:
            data = self.data
            if data is None:
                # create new properties
                self.__properties = {}
            else:
                # get properties from data
                self.__properties = json_decode(data=data)
                assert isinstance(self.__properties, dict), 'document data error: %s' % self
        return self.__properties

    # Override
    def get_property(self, key: str) -> Optional[Any]:
        info = self.properties
        if info is not None:
            return info.get(key)

    # Override
    def set_property(self, key: str, value: Optional[Any]):
        """ Update profile property with key and value """
        # 1. reset status
        assert self.__status >= 0, 'status error: %s' % self
        self.__status = 0
        # 2. update property value with name
        info = self.properties
        assert isinstance(info, dict), 'failed to get properties: %s' % self
        if value is None:
            info.pop(key, None)
        else:
            info[key] = value
        # 3. clear data signature after properties changed
        self.pop('data', None)
        self.pop('signature', None)
        self.__data = None
        self.__signature = None

    #
    #  properties getter/setter
    #

    @property  # Override
    def time(self) -> int:
        timestamp = self.get_property(key='time')
        if timestamp is None:
            return 0
        else:
            return int(timestamp)

    @property  # Override
    def name(self) -> Optional[str]:
        return self.get_property(key='name')

    @name.setter  # Override
    def name(self, value: str):
        self.set_property(key='name', value=value)


class BaseVisa(BaseDocument, Visa):

    def __init__(self, document: Optional[dict] = None, identifier: Optional[ID] = None,
                 data: Union[bytes, str, None] = None, signature: Union[bytes, str, None] = None):
        super().__init__(document, doc_type=Document.VISA, identifier=identifier, data=data, signature=signature)
        self.__key = None

    """
        Public Key for encryption
        ~~~~~~~~~~~~~~~~~~~~~~~~~
        For safety considerations, the profile.key which used to encrypt message data
        should be different with meta.key
    """
    @property  # Override
    def key(self) -> Union[EncryptKey, VerifyKey, None]:
        if self.__key is None:
            info = self.get_property(key='key')
            if info is not None:
                self.__key = PublicKey.parse(key=info)
        return self.__key

    @key.setter  # Override
    def key(self, value: Union[EncryptKey, VerifyKey]):
        self.set_property(key='key', value=value.dictionary)
        self.__key = value

    """
        Avatar
        ~~~~~~
    """
    @property  # Override
    def avatar(self) -> Optional[str]:
        return self.get_property(key='avatar')

    @avatar.setter  # Override
    def avatar(self, value: str):
        self.set_property(key='avatar', value=value)


class BaseBulletin(BaseDocument, Bulletin):

    def __init__(self, document: Optional[dict] = None, identifier: Optional[ID] = None,
                 data: Union[bytes, str, None] = None, signature: Union[bytes, str, None] = None):
        super().__init__(document, doc_type=Document.BULLETIN, identifier=identifier, data=data, signature=signature)
        self.__assistants = None

    @property  # Override
    def assistants(self) -> Optional[List[ID]]:
        if self.__assistants is None:
            assistants = self.get_property(key='assistants')
            if assistants is not None:
                self.__assistants = ID.convert(members=assistants)
        return self.__assistants

    @assistants.setter  # Override
    def assistants(self, bots: List[ID]):
        self.set_property(key='assistants', value=ID.revert(members=bots))
        self.__assistants = bots
