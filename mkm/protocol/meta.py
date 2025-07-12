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
from typing import Optional, Any, Dict

from ..types import Mapper
from ..crypto import VerifyKey, SignKey
from ..format import TransportableData

from .address import Address
from .helpers import AccountExtensions


class Meta(Mapper, ABC):
    """This class is used to generate entity ID

        User/Group Meta data
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            type        : 1,              // algorithm version
            key         : "{public key}", // PK = secp256k1(SK);
            seed        : "moKy",         // user/group name
            fingerprint : "..."           // CT = sign(seed, SK);
        }

        algorithm:
            fingerprint = sign(seed, SK);
    """

    @property
    @abstractmethod
    def type(self) -> str:
        """
        Meta algorithm version

            1 = MKM : username@address (default)
            2 = BTC : btc_address
            4 = ETH : eth_address
            ...
        """
        raise NotImplemented

    @property
    @abstractmethod
    def public_key(self) -> VerifyKey:
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

    #
    #   Validation
    #

    @property
    @abstractmethod
    def valid(self) -> bool:
        """
        Check meta valid
        (must call this when received a new meta from network)

        :return: True on valid
        """
        raise NotImplemented

    @abstractmethod
    def generate_address(self, network: int = None) -> Address:
        """
        Generate Address with network ID

        :param network:  Address.type
        :return: Address
        """
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def generate(cls, version: str, private_key: SignKey, seed: str = None):  # -> Meta:
        helper = meta_helper()
        return helper.generate_meta(version, private_key, seed=seed)

    @classmethod
    def create(cls, version: str, public_key: VerifyKey,
               seed: str = None, fingerprint: TransportableData = None):  # -> Meta:
        helper = meta_helper()
        return helper.create_meta(version, public_key, seed=seed, fingerprint=fingerprint)

    @classmethod
    def parse(cls, meta: Any):  # -> Optional[Meta]:
        helper = meta_helper()
        return helper.parse_meta(meta=meta)

    @classmethod
    def get_factory(cls, version: str):  # -> Optional[MetaFactory]:
        helper = meta_helper()
        return helper.get_meta_factory(version)

    @classmethod
    def set_factory(cls, version: str, factory):
        helper = meta_helper()
        helper.set_meta_factory(version, factory=factory)


def meta_helper():
    helper = AccountExtensions.meta_helper
    assert isinstance(helper, MetaHelper), 'meta helper error: %s' % helper
    return helper


class MetaFactory(ABC):
    """ Meta Factory """

    @abstractmethod
    def generate_meta(self, private_key: SignKey, seed: Optional[str]) -> Meta:
        """
        Generate meta

        :param private_key: asymmetric private key
        :param seed:        ID.name
        :return: Meta
        """
        raise NotImplemented

    @abstractmethod
    def create_meta(self, public_key: VerifyKey, seed: Optional[str], fingerprint: Optional[TransportableData]) -> Meta:
        """
        Create meta

        :param public_key:  asymmetric public key
        :param seed:        ID.name
        :param fingerprint: private_key.sign(seed)
        :return: Meta
        """
        raise NotImplemented

    @abstractmethod
    def parse_meta(self, meta: Dict) -> Optional[Meta]:
        """
        Parse map object to meta

        :param meta: meta info
        :return: Meta
        """
        raise NotImplemented


########################
#                      #
#   Plugins: Helpers   #
#                      #
########################


class MetaHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_meta_factory(self, version: str, factory: MetaFactory):
        raise NotImplemented

    @abstractmethod
    def get_meta_factory(self, version: str) -> Optional[MetaFactory]:
        raise NotImplemented

    @abstractmethod
    def generate_meta(self, version: str, private_key: SignKey, seed: Optional[str]) -> Meta:
        raise NotImplemented

    @abstractmethod
    def create_meta(self, version: str, public_key: VerifyKey,
                    seed: Optional[str], fingerprint: Optional[TransportableData]) -> Meta:
        raise NotImplemented

    @abstractmethod
    def parse_meta(self, meta: Any) -> Optional[Meta]:
        raise NotImplemented
