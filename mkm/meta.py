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

from abc import ABCMeta, abstractmethod
from typing import Optional

from .crypto.utils import base64_encode, base64_decode
from .crypto import PublicKey, PrivateKey

from .address import NetworkID, Address, DefaultAddress
from .identifier import ID


class Meta(dict, metaclass=ABCMeta):
    """This class is used to generate entity ID

        User/Group Meta data
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            version: 1,          // meta version
            seed: "moKy",        // user/group name
            key: "{public key}", // PK = secp256k1(SK);
            fingerprint: "..."   // CT = sign(seed, SK);
        }

        algorithm:
            fingerprint = sign(seed, SK);
    """

    """
        @enum MKMMetaVersion

        @abstract Defined for meta data structure to generate identifier.

        @discussion Generate & check ID/Address

            MKMMetaVersion_MKM give a seed string first, and sign this seed to get
            fingerprint; after that, use the fingerprint to generate address.
            This will get a firmly relationship between (username, address & key).

            MKMMetaVersion_BTC use the key data to generate address directly.
            This can build a BTC address for the entity ID without username.

            MKMMetaVersion_ExBTC use the key data to generate address directly, and
            sign the seed to get fingerprint (just for binding username & key).
            This can build an entity ID with username and BTC address.
    """
    Version_MKM = 0x01    # 0000 0001
    Version_BTC = 0x02    # 0000 0010
    Version_ExBTC = 0x03  # 0000 0011
    Version_ETH = 0x04    # 0000 0100
    Version_ExETH = 0x05  # 0000 0101
    DefaultVersion = Version_MKM

    # noinspection PyTypeChecker
    def __new__(cls, meta: dict):
        """
        Create meta for entity

        :param meta: meta info
        :return: Meta object
        """
        if meta is None:
            return None
        elif cls is Meta:
            if isinstance(meta, Meta):
                # return Meta object directly
                return meta
            # get class by meta version
            clazz = cls.meta_class(version=int(meta['version']))
            if clazz is not None:
                assert issubclass(clazz, Meta), '%s must be sub-class of Meta' % clazz
                return clazz.__new__(clazz, meta)
            else:
                raise ModuleNotFoundError('Invalid meta version: %s' % meta)
        # subclass
        return super().__new__(cls, meta)

    def __init__(self, meta: dict):
        if self is meta:
            # no need to init again
            return
        super().__init__(meta)
        # lazy
        self.__version: int = 0
        self.__key: PublicKey = None
        self.__seed: str = None
        self.__fingerprint: bytes = None
        self.__status: int = 0

    def __eq__(self, other) -> bool:
        """ Check whether they can generate same IDs """
        if not isinstance(other, dict):
            return False
        if super().__eq__(other):
            return True
        # check with ID
        other = Meta(other)
        id1 = self.generate_identifier(network=NetworkID.Main)
        id2 = other.generate_identifier(network=NetworkID.Main)
        return id1 == id2

    @property
    def version(self) -> int:
        if self.__version is 0:
            self.__version = int(self['version'])
        return self.__version

    @property
    def key(self) -> PublicKey:
        if self.__key is None:
            self.__key = PublicKey(self['key'])
        return self.__key

    @property
    def seed(self) -> Optional[str]:
        if self.__seed is None and (self.version & Meta.Version_MKM):
            # MKM, ExBTC, ExETH, ...
            self.__seed = self['seed']
        return self.__seed

    @property
    def fingerprint(self) -> Optional[bytes]:
        if self.__fingerprint is None and (self.version & Meta.Version_MKM):
            # MKM, ExBTC, ExETH, ...
            self.__fingerprint = base64_decode(self['fingerprint'])
        return self.__fingerprint

    @property
    def valid(self) -> bool:
        if self.__status is 0:
            key = self.key
            if key is None:
                # meta.key should not be empty
                self.__status = -1
            elif self.version & Meta.Version_MKM:
                # MKM, ExBTC, ExETH, ...
                un = self.seed
                ct = self.fingerprint
                if un is not None and ct is not None and key.verify(data=un.encode('utf-8'), signature=ct):
                    # fingerprint matched
                    self.__status = 1
                else:
                    # fingerprint not matched
                    self.__status = -1
            else:
                # BTC, ETH, ...
                self.__status = 1
        return self.__status == 1

    def match_public_key(self, public_key: PublicKey) -> bool:
        """ Check whether match public key """
        if self.key == public_key:
            return True
        if self.version & Meta.Version_MKM:  # MKM, ExBTC, ExETH, ...
            # check whether keys equal by verifying signature
            return public_key.verify(data=self.seed.encode('utf-8'), signature=self.fingerprint)
        else:  # BTC, ETH, ...
            # ID with BTC/ETH address has no username
            # so we can just compare the key.data to check matching
            return False

    def match_identifier(self, identifier: ID) -> bool:
        """ Check ID(name+address) with meta info """
        if identifier is None:
            return False
        return self.generate_identifier(identifier.address.network) == identifier

    def match_address(self, address: Address) -> bool:
        """ Check address with meta info """
        if address is None:
            return False
        return self.generate_address(network=address.network) == address

    def generate_identifier(self, network: NetworkID) -> Optional[ID]:
        """ Generate ID with meta info and network ID """
        address = self.generate_address(network=network)
        if address is not None:
            return ID.new(name=self.seed, address=address)

    @abstractmethod
    def generate_address(self, network: NetworkID) -> Optional[Address]:
        """ Generate address with meta info and network ID """
        pass

    #
    #  Factories
    #
    @classmethod
    def new(cls, key: PublicKey, seed: str=None, fingerprint: bytes=None, version: int=DefaultVersion):
        """
        Create new meta info

        :param version:     - meta version
        :param key:         - public key
        :param seed:        - user/group name
        :param fingerprint: - signature
        :return: Meta object
        """
        if version & Meta.Version_MKM:  # MKM, ExBTC, ExETH, ...
            meta = {
                'version': version,
                'seed': seed,
                'key': key,
                'fingerprint': base64_encode(fingerprint),
            }
        else:  # BTC, ETH, ...
            meta = {
                'version': version,
                'key': key,
            }
        # new Meta(dict)
        return cls(meta)

    @classmethod
    def generate(cls, private_key: PrivateKey, seed: str='', version: int=DefaultVersion):
        """
        Generate meta info with seed and private key

        :param private_key: - user/founder private key
        :param seed:        - user/group name
        :param version:     - meta version
        :return:
        """
        if version & Meta.Version_MKM:  # MKM, ExBTC, ExETH, ...
            # generate fingerprint with private key
            fingerprint = private_key.sign(seed.encode('utf-8'))
            dictionary = {
                'version': version,
                'seed': seed,
                'key': private_key.public_key,
                'fingerprint': base64_encode(fingerprint),
            }
        else:  # BTC, ETH, ...
            dictionary = {
                'version': version,
                'key': private_key.public_key,
            }
        # new Meta(dict)
        return cls(dictionary)

    #
    #   Runtime
    #
    __meta_classes = {}  # class map

    @classmethod
    def register(cls, version: int, meta_class=None) -> bool:
        """
        Register meta class with version

        :param version:  meta version for different meta algorithms
        :param meta_class: if content class is None, then remove with type
        :return: False on error
        """
        if meta_class is None:
            cls.__meta_classes.pop(version, None)
        elif issubclass(meta_class, Meta):
            cls.__meta_classes[version] = meta_class
        else:
            raise TypeError('%s must be subclass of Meta' % meta_class)
        return True

    @classmethod
    def meta_class(cls, version: int):
        """
        Get meta class with version

        :param version: meta version for different meta algorithm
        :return: meta class
        """
        return cls.__meta_classes.get(version)


"""
    Default Meta for generate ID with address
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    version:
        0x01 - MKM
        
    algorithm:
        CT      = fingerprint;
        hash    = ripemd160(sha256(CT));
        code    = sha256(sha256(network + hash)).prefix(4);
        address = base58_encode(network + hash + code);
        number  = u_int(code);
"""


class DefaultMeta(Meta):

    def generate_address(self, network: NetworkID) -> Optional[Address]:
        assert self.version == Meta.Version_MKM, 'meta version error: %d' % self.version
        if self.valid:
            return DefaultAddress.new(data=self.fingerprint, network=network)


# register meta class with version
Meta.register(version=Meta.Version_MKM, meta_class=DefaultMeta)
