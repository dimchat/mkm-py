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

from ..types import Mapper
from ..crypto import VerifyKey, SignKey

from .version import MetaType
from .address import Address
from .identifier import ID


class Meta(Mapper, ABC):
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
    @abstractmethod
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
    @abstractmethod
    def key(self) -> VerifyKey:
        """
        Public key (used for signature)

            RSA
            ECC

        :return: public key
        """
        raise NotImplemented

    @property
    @abstractmethod
    def seed(self) -> Optional[str]:
        """
        Seed to generate fingerprint

        :return: ID.name
        """
        raise NotImplemented

    @property
    @abstractmethod
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
        Generate Address with network ID

        :param network:  Address.type
        :return: Address
        """
        raise NotImplemented

    @classmethod
    def check(cls, meta) -> bool:
        gf = general_factory()
        return gf.check_meta(meta=meta)

    @classmethod
    def match_id(cls, meta, identifier: ID) -> bool:
        gf = general_factory()
        return gf.meta_match_id(meta=meta, identifier=identifier)

    @classmethod
    def match_key(cls, meta, key: VerifyKey) -> bool:
        gf = general_factory()
        return gf.meta_match_key(meta=meta, key=key)

    #
    #   Factory methods
    #

    @classmethod
    def generate(cls, version: Union[MetaType, int], key: SignKey, seed: Optional[str] = None):  # -> Optional[Meta]:
        gf = general_factory()
        return gf.generate_meta(version=version, key=key, seed=seed)

    @classmethod
    def create(cls, version: Union[MetaType, int], key: VerifyKey,
               seed: Optional[str] = None, fingerprint: Union[bytes, str, None] = None):  # -> Optional[Meta]:
        gf = general_factory()
        return gf.create_meta(version=version, key=key, seed=seed, fingerprint=fingerprint)

    @classmethod
    def parse(cls, meta: Any):  # -> Optional[Meta]:
        gf = general_factory()
        return gf.parse_meta(meta=meta)

    @classmethod
    def factory(cls, version: Union[MetaType, int]):  # -> Optional[MetaFactory]:
        gf = general_factory()
        return gf.get_meta_factory(version=version)

    @classmethod
    def register(cls, version: Union[MetaType, int], factory):
        gf = general_factory()
        gf.set_meta_factory(version=version, factory=factory)


def general_factory():
    from ..core.factory import FactoryManager
    return FactoryManager.general_factory


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
    def parse_meta(self, meta: Dict[str, Any]) -> Optional[Meta]:
        """
        Parse map object to meta

        :param meta: meta info
        :return: Meta
        """
        raise NotImplemented
