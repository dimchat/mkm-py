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
from typing import Optional, Union

from .crypto import PublicKey, PrivateKey, EncryptKey
from .crypto import Base64

from .types import NetworkID, MetaVersion
from .address import Address, DefaultAddress
from .identifier import ID


class Meta(dict, ABC):
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
            version = meta['version']
            if isinstance(version, MetaVersion):
                version = version.value
            else:
                version = int(version)
            clazz = cls.__meta_classes.get(version)
            if clazz is None:
                raise ModuleNotFoundError('meta version not supported: %s' % meta)
            return clazz.__new__(clazz, meta)
        # subclass
        return super().__new__(cls, meta)

    def __init__(self, meta: dict):
        if self is meta:
            # no need to init again
            return
        super().__init__(meta)
        # Meta algorithm version
        version = meta['version']
        if isinstance(version, MetaVersion):
            version = version.value
        else:
            version = int(version)
        self.__version = version
        # lazy
        self.__key: Union[PublicKey, EncryptKey, None] = None
        self.__seed: str = None
        self.__fingerprint: bytes = None
        self.__status: int = 0  # 1 for valid, -1 for invalid

    def __eq__(self, other) -> bool:
        """ Check whether they can generate same IDs """
        if not isinstance(other, dict):
            return False
        if super().__eq__(other):
            return True
        # check with ID
        other = Meta(other)
        identifier = other.generate_identifier(network=NetworkID.Main)
        return self.match_identifier(identifier)

    @property
    def version(self) -> int:
        """
        Meta algorithm version

            0x01 - username@address
            0x02 - btc_address
            0x03 - username@btc_address
            0x04 - eth_address
            0x05 - username@eth_address
            ...
        """
        return self.__version

    @property
    def has_seed(self) -> bool:
        return MetaVersion.has_seed(version=self.version)

    @property
    def key(self) -> Union[PublicKey, EncryptKey]:
        """
        Public key (used for signature)

            RSA
            ECC

        :return: public key
        """
        if self.__key is None:
            self.__key = PublicKey(self['key'])
        return self.__key

    @property
    def seed(self) -> Optional[str]:
        """
        Seed to generate fingerprint

        :return: ID.name
        """
        if self.__seed is None and self.has_seed:
            # MKM, ExBTC, ExETH, ...
            self.__seed = self['seed']
        return self.__seed

    @property
    def fingerprint(self) -> Optional[bytes]:
        """
        Fingerprint to verify ID and public key

            Build: fingerprint = sign(seed, privateKey)
            Check: verify(seed, fingerprint, publicKey)

        :return: signature
        """
        if self.__fingerprint is None and self.has_seed:
            # MKM, ExBTC, ExETH, ...
            self.__fingerprint = Base64.decode(self['fingerprint'])
        return self.__fingerprint

    @property
    def valid(self) -> bool:
        """
        Check meta valid
        (must call this when received a new meta from network)

        :return: True on valid
        """
        if self.__status is 0:
            key = self.key
            if key is None:
                # meta.key should not be empty
                self.__status = -1
            elif self.has_seed:
                seed = self.seed
                fingerprint = self.fingerprint
                if seed is None or fingerprint is None:
                    # seed and fingerprint should not be empty
                    self.__status = -1
                elif key.verify(data=seed.encode('utf-8'), signature=fingerprint):
                    # fingerprint matched
                    self.__status = 1
                else:
                    # fingerprint not matched
                    self.__status = -1
            else:
                # BTC, ETH, ...
                self.__status = 1
        return self.__status == 1

    def match(self, public_key: PublicKey=None, identifier: ID=None, address: Address=None):
        if public_key is not None:
            return self.match_public_key(public_key=public_key)
        elif identifier is not None:
            return self.match_identifier(identifier=identifier)
        elif address is not None:
            return self.match_address(address=address)

    def match_public_key(self, public_key: PublicKey) -> bool:
        """
        Check whether match public key

        :param public_key: user's public key
        :return: True on matched
        """
        if not self.valid:
            return False
        if self.key == public_key:
            return True
        if self.has_seed:
            # check whether keys equal by verifying signature
            seed = self.seed
            fingerprint = self.fingerprint
            return public_key.verify(data=seed.encode('utf-8'), signature=fingerprint)
        else:
            # NOTICE: ID with BTC/ETH address has no username, so
            #         just compare the key.data to check matching
            return False

    def match_identifier(self, identifier: ID) -> bool:
        """
        Check ID(name+address) with meta info
        (must call this when received a new meta from network)

        :param identifier: user ID
        :return: True on matched
        """
        if identifier is None:
            return False
        return self.generate_identifier(identifier.address.network) == identifier

    def match_address(self, address: Address) -> bool:
        """
        Check address with meta info

        :param address: user's ID.address
        :return: True on matched
        """
        if address is None:
            return False
        return self.generate_address(network=address.network) == address

    def generate_identifier(self, network: Union[NetworkID, int]) -> ID:
        """
        Generate ID with meta info and network ID

        :param network: ID type
        :return: ID object
        """
        if isinstance(network, NetworkID):
            network = network.value
        address = self.generate_address(network=network)
        if address is not None:
            return ID.new(name=self.seed, address=address)

    @abstractmethod
    def generate_address(self, network: int) -> Address:
        """
        Generate address with meta info and network ID

        :param network: address type
        :return: Address object
        """
        # NOTICE: must check meta valid before generate address
        raise NotImplemented

    #
    #  Factories
    #
    @classmethod
    def new(cls, key: PublicKey, seed: str=None, fingerprint: bytes=None, version: MetaVersion=MetaVersion.Default):
        """
        Create new meta info

        :param version:     - meta version
        :param key:         - public key
        :param seed:        - user/group name
        :param fingerprint: - signature
        :return: Meta object
        """
        if isinstance(version, MetaVersion):
            version = version.value
        if MetaVersion.has_seed(version=version):
            # MKM, ExBTC, ExETH, ...
            meta = {
                'version': version,
                'seed': seed,
                'key': key,
                'fingerprint': Base64.encode(fingerprint),
            }
        else:
            # BTC, ETH, ...
            meta = {
                'version': version,
                'key': key,
            }
        # new Meta(dict)
        return cls(meta)

    @classmethod
    def generate(cls, private_key: PrivateKey, seed: str='', version: MetaVersion=MetaVersion.Default):
        """
        Generate meta info with seed and private key

        :param private_key: - user/founder private key
        :param seed:        - user/group name
        :param version:     - meta version
        :return:
        """
        if isinstance(version, MetaVersion):
            version = version.value
        if MetaVersion.has_seed(version=version):
            # MKM, ExBTC, ExETH, ...
            # generate fingerprint with private key
            fingerprint = private_key.sign(seed.encode('utf-8'))
            dictionary = {
                'version': version,
                'seed': seed,
                'key': private_key.public_key,
                'fingerprint': Base64.encode(fingerprint),
            }
        else:
            # BTC, ETH, ...
            dictionary = {
                'version': version,
                'key': private_key.public_key,
            }
        # new Meta(dict)
        return cls(dictionary)

    #
    #   Runtime
    #
    __meta_classes = {}  # int -> class

    @classmethod
    def register(cls, version: Union[MetaVersion, int], meta_class=None) -> bool:
        """
        Register meta class with version

        :param version:  meta version for different meta algorithms
        :param meta_class: if content class is None, then remove with type
        :return: False on error
        """
        if isinstance(version, MetaVersion):
            version = version.value
        else:
            version = int(version)
        if meta_class is None:
            cls.__meta_classes.pop(version, None)
        elif issubclass(meta_class, Meta):
            cls.__meta_classes[version] = meta_class
        else:
            raise TypeError('%s must be subclass of Meta' % meta_class)
        return True


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

    def __init__(self, meta: dict):
        if self is meta:
            # no need to init again
            return
        super().__init__(meta)
        # id caches
        self.__ids: dict = {}  # int -> ID

    def generate_identifier(self, network: int) -> ID:
        # check cache
        identifier = self.__ids.get(network)
        if identifier is None:
            # generate and cache it
            identifier = super().generate_identifier(network=network)
            assert identifier.valid, 'failed to generate ID with network: %s' % network
            self.__ids[network] = identifier
        return identifier

    def generate_address(self, network: int) -> Address:
        assert self.version == MetaVersion.MKM, 'meta version error: %d' % self.version
        assert self.valid, 'meta not valid: %s' % self
        # check cache
        identifier: ID = self.__ids.get(network)
        if identifier is not None:
            return identifier.address
        # generate
        return DefaultAddress.new(data=self.fingerprint, network=network)


# register meta class with version
Meta.register(version=MetaVersion.MKM, meta_class=DefaultMeta)
