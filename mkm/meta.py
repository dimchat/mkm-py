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
from typing import Optional, Union, Any

from .crypto import base64_encode, base64_decode, utf8_encode
from .crypto import Map, Dictionary
from .crypto import VerifyKey, SignKey, PublicKey

from .types import MetaType, meta_has_seed
from .address import Address
from .identifier import ID
from .factories import Factories


class Meta(Map, ABC):
    """This class is used to generate entity ID

        User/Group Meta data
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            type: 1,             // meta version
            seed: "moKy",        // user/group name
            key: "{public key}", // PK = secp256k1(SK);
            fingerprint: "..."   // CT = sign(seed, SK);
        }

        algorithm:
            fingerprint = sign(seed, SK);
    """

    @property
    def type(self) -> int:
        """
        Meta algorithm version

            0x01 - username@address
            0x02 - btc_address
            0x03 - username@btc_address
            0x04 - eth_address
            0x05 - username@eth_address
            ...
        """
        raise NotImplemented

    @property
    def key(self) -> VerifyKey:
        """
        Public key (used for signature)

            RSA
            ECC

        :return: public key
        """
        raise NotImplemented

    @property
    def seed(self) -> Optional[str]:
        """
        Seed to generate fingerprint

        :return: ID.name
        """
        raise NotImplemented

    @property
    def fingerprint(self) -> Optional[bytes]:
        """
        Fingerprint to verify ID and public key

            Build: fingerprint = sign(seed, privateKey)
            Check: verify(seed, fingerprint, publicKey)

        :return: signature
        """
        raise NotImplemented

    @abstractmethod
    def generate_address(self, network: int) -> Optional[Address]:
        """
        Generate Address with network type

        :param network:  Address.network
        :return: Address
        """
        raise NotImplemented

    #
    #   Meta factory
    #
    class Factory(ABC):

        @abstractmethod
        def create_meta(self, key: VerifyKey, seed: Optional[str], fingerprint: Union[bytes, str, None]):  # -> Meta:
            """
            Create meta

            :param key:         public key
            :param seed:        ID.name
            :param fingerprint: sKey.sign(seed)
            :return: Meta
            """
            raise NotImplemented

        @abstractmethod
        def generate_meta(self, key: SignKey, seed: Optional[str]):  # -> Meta:
            """
            Generate meta

            :param key:  private key
            :param seed: ID.name
            :return: Meta
            """
            raise NotImplemented

        @abstractmethod
        def parse_meta(self, meta: dict):  # -> Optional[Meta]:
            """
            Parse map object to meta

            :param meta: meta info
            :return: Meta
            """
            raise NotImplemented

    @classmethod
    def register(cls, version: Union[MetaType, int], factory: Factory):
        if isinstance(version, MetaType):
            version = version.value
        Factories.meta_factories[version] = factory

    @classmethod
    def factory(cls, version: Union[MetaType, int]) -> Optional[Factory]:
        if isinstance(version, MetaType):
            version = version.value
        return Factories.meta_factories.get(version)

    #
    #   Factory methods
    #

    @classmethod
    def create(cls, version: Union[MetaType, int], key: VerifyKey,
               seed: Optional[str] = None, fingerprint: Union[bytes, str, None] = None):  # -> Optional[Meta]:
        factory = cls.factory(version=version)
        assert factory is not None, 'meta type not support: %d' % version
        return factory.create_meta(key=key, seed=seed, fingerprint=fingerprint)

    @classmethod
    def generate(cls, version: Union[MetaType, int], key: SignKey, seed: Optional[str] = None):  # -> Optional[Meta]:
        factory = cls.factory(version=version)
        assert factory is not None, 'meta type not support: %d' % version
        return factory.generate_meta(key=key, seed=seed)

    @classmethod
    def parse(cls, meta: Any):  # -> Optional[Meta]:
        if meta is None:
            return None
        elif isinstance(meta, Meta):
            return meta
        elif isinstance(meta, Map):
            meta = meta.dictionary
        # assert isinstance(meta, dict), 'meta error: %s' % meta
        version = meta_type(meta=meta)
        factory = cls.factory(version=version)
        if factory is None:
            factory = cls.factory(version=0)  # unknown
            assert factory is not None, 'cannot parse meta: %s' % meta
        return factory.parse_meta(meta=meta)


"""
    Implements
    ~~~~~~~~~~
"""


def meta_type(meta: dict) -> int:
    version = meta.get('type')
    if version is None:
        version = meta.get('version')
    return int(version)


def check_meta(meta: Meta) -> bool:
    key = meta.key
    if key is None:
        # meta.key should not be empty
        return False
    if not meta_has_seed(version=meta.type):
        # this meta has no seed, so no signature too
        return True
    # check seed with signature
    seed = meta.seed
    fingerprint = meta.fingerprint
    if seed is None or fingerprint is None:
        # seed and fingerprint should not be empty
        return False
    # verify fingerprint
    return key.verify(data=utf8_encode(string=seed), signature=fingerprint)


def meta_match_id(identifier: ID, meta: Meta) -> bool:
    """
    Check whether meta match with entity ID
    (must call this when received a new meta from network)

    :param identifier: entity ID
    :param meta:       meta info
    :return: True on matched
    """
    # check ID.name
    if meta.seed != identifier.name:
        return False
    # check ID.address
    address = Address.generate(meta=meta, network=identifier.type)
    return address == identifier.address


def meta_match_key(key: VerifyKey, meta: Meta) -> bool:
    """
    Check whether meta match with public key

    :param key:  public key
    :param meta: meta info
    :return: True on matched
    """
    # check whether the public key equals to meta.key
    if key == meta.key:
        return True
    # check with seed & fingerprint
    if not meta_has_seed(version=meta.type):
        # NOTICE: ID with BTC/ETH address has no username, so
        #         just compare the key.data to check matching
        return False
    # check whether keys equal by verifying signature
    seed = utf8_encode(string=meta.seed)
    fingerprint = meta.fingerprint
    return key.verify(data=seed, signature=fingerprint)


class BaseMeta(Dictionary, Meta, ABC):

    def __init__(self, meta: Optional[dict] = None,
                 version: Union[MetaType, int] = 0, key: Optional[VerifyKey] = None,
                 seed: Optional[str] = None, fingerprint: Union[bytes, str, None] = None):
        # check parameters
        if isinstance(version, MetaType):
            version = version.value
        if fingerprint is None:
            base64 = None
        elif isinstance(fingerprint, bytes):
            base64 = base64_encode(data=fingerprint)
        else:
            assert isinstance(fingerprint, str), 'meta.fingerprint error: %s' % fingerprint
            base64 = fingerprint
            fingerprint = base64_decode(string=base64)
        if meta is None:
            assert version > 0 and key is not None, 'meta error: %d, %s, %s, %s' % (version, key, seed, fingerprint)
            # build meta info
            if seed is None or base64 is None:
                meta = {
                    'type': version,
                    'key': key.dictionary,
                }
            else:
                meta = {
                    'type': version,
                    'key': key.dictionary,
                    'seed': seed,
                    'fingerprint': base64,
                }
        # initialize with meta info
        super().__init__(dictionary=meta)
        # lazy load
        self.__type = version
        self.__key = key
        self.__seed = seed
        self.__fingerprint = fingerprint

    @property  # Override
    def type(self) -> int:
        if self.__type == 0:
            self.__type = meta_type(meta=self.dictionary)
        return self.__type

    @property  # Override
    def key(self) -> VerifyKey:
        if self.__key is None:
            key = self.get('key')
            self.__key = PublicKey.parse(key=key)
        return self.__key

    @property  # Override
    def seed(self) -> Optional[str]:
        if self.__seed is None and meta_has_seed(version=self.type):
            self.__seed = self.get('seed')
        return self.__seed

    @property  # Override
    def fingerprint(self) -> Optional[bytes]:
        if self.__fingerprint is None and meta_has_seed(version=self.type):
            fingerprint = self.get('fingerprint')
            if fingerprint is not None:
                self.__fingerprint = base64_decode(string=fingerprint)
        return self.__fingerprint
