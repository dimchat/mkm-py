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

from .wrappers import MapWrapper

from .crypto import utf8_encode
from .crypto import VerifyKey, SignKey

from .types import MetaType, meta_has_seed
from .address import Address
from .identifier import ID
from .factories import Factories


class Meta(MapWrapper, ABC):
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

    @classmethod
    def check(cls, meta) -> bool:
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

    @classmethod
    def matches(cls, meta, identifier: ID = None, key: VerifyKey = None) -> bool:
        if identifier is not None:
            """ Check whether meta match with entity ID
                (must call this when received a new meta from network) """
            # check ID.name
            if meta.seed == identifier.name:
                # check ID.address
                address = Address.generate(meta=meta, network=identifier.type)
                return address == identifier.address
        elif key is not None:
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
    #   Factory methods
    #

    @classmethod
    def generate(cls, version: Union[MetaType, int], key: SignKey, seed: Optional[str] = None):  # -> Optional[Meta]:
        factory = cls.factory(version=version)
        assert isinstance(factory, MetaFactory), 'meta type not support: %d, %s' % (version, factory)
        return factory.generate_meta(key=key, seed=seed)

    @classmethod
    def create(cls, version: Union[MetaType, int], key: VerifyKey,
               seed: Optional[str] = None, fingerprint: Union[bytes, str, None] = None):  # -> Optional[Meta]:
        factory = cls.factory(version=version)
        assert isinstance(factory, MetaFactory), 'meta type not support: %d, %s' % (version, factory)
        return factory.create_meta(key=key, seed=seed, fingerprint=fingerprint)

    @classmethod
    def parse(cls, meta: Any):  # -> Optional[Meta]:
        if meta is None:
            return None
        elif isinstance(meta, cls):
            return meta
        elif isinstance(meta, MapWrapper):
            meta = meta.dictionary
        # assert isinstance(meta, dict), 'meta error: %s' % meta
        version = meta_type(meta=meta)
        factory = cls.factory(version=version)
        if factory is None:
            factory = cls.factory(version=0)  # unknown
            assert factory is not None, 'cannot parse meta: %s' % meta
        assert isinstance(factory, MetaFactory), 'meta factory error: %s' % factory
        return factory.parse_meta(meta=meta)

    @classmethod
    def factory(cls, version: Union[MetaType, int]):  # -> Optional[MetaFactory]:
        if isinstance(version, MetaType):
            version = version.value
        return Factories.meta_factories.get(version)

    @classmethod
    def register(cls, version: Union[MetaType, int], factory):
        if isinstance(version, MetaType):
            version = version.value
        Factories.meta_factories[version] = factory


def meta_type(meta: dict) -> int:
    """ get meta type(version) """
    version = meta.get('type')
    if version is None:
        version = meta.get('version')
    return int(version)


class MetaFactory(ABC):

    @abstractmethod
    def generate_meta(self, key: SignKey, seed: Optional[str]) -> Meta:
        """
        Generate meta

        :param key:  private key
        :param seed: ID.name
        :return: Meta
        """
        raise NotImplemented

    @abstractmethod
    def create_meta(self, key: VerifyKey, seed: Optional[str], fingerprint: Union[bytes, str, None]) -> Meta:
        """
        Create meta

        :param key:         public key
        :param seed:        ID.name
        :param fingerprint: sKey.sign(seed)
        :return: Meta
        """
        raise NotImplemented

    @abstractmethod
    def parse_meta(self, meta: dict) -> Optional[Meta]:
        """
        Parse map object to meta

        :param meta: meta info
        :return: Meta
        """
        raise NotImplemented
