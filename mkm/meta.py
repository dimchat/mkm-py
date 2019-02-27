# -*- coding: utf-8 -*-
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

"""
    Account/Group Meta data
    ~~~~~~~~~~~~~~~~~~~~~~~

    data format: {
        version: 1,          // algorithm version
        seed: "moKy",        // user/group name
        key: "{public key}", // PK = secp256k1(SK);
        fingerprint: "..."   // CT = sign(seed, SK);
    }

    algorithm:
        fingerprint = sign(seed, SK);

        CT      = fingerprint; // or key.data for BTC address
        hash    = ripemd160(sha256(CT));
        code    = sha256(sha256(network + hash)).prefix(4);
        address = base58_encode(network + hash + code);
        number  = uint(code);
"""

from .utils import base64_encode, base64_decode
from .crypto import PublicKey, PrivateKey

from .address import NetworkID, Address
from .entity import ID


class Meta(dict):
    """
        Meta for Identifier
        ~~~~~~~~~~~~~~~~~~~

        @enum MKMMetaVersion

        @abstract Defined for algorithm that generating address.

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
    DefaultVersion = Version_MKM

    def __new__(cls, meta: dict=None,
                seed: str='', key: PublicKey=None, fingerprint: bytes=None, version: chr=DefaultVersion):
        """
        Create meta object with meta info

        :param meta:        A dictionary as meta info
        :param seed:        A string as seed (name)
        :param key:         A public key
        :param fingerprint: A data signed by private keys with seed
        :param version:     Algorithm version
        :return: Meta object
        """
        if meta:
            # return Meta object directly
            if isinstance(meta, Meta):
                return meta
            # get fields from dictionary
            version = int(meta['version'])
            if version == cls.Version_MKM or version == cls.Version_ExBTC:
                seed = meta['seed']
                fingerprint = base64_decode(meta['fingerprint'])
            elif version == cls.Version_BTC:
                seed = ''
                fingerprint = None
            else:
                raise ValueError('unsupported version:', version)
            # public key
            key = PublicKey(meta['key'])
        elif version and key:
            # build meta info
            if version == cls.Version_MKM or version == cls.Version_ExBTC:
                meta = {
                    'version': version,
                    'seed': seed,
                    'key': key,
                    'fingerprint': base64_encode(fingerprint),
                }
            elif version == cls.Version_BTC:
                meta = {
                    'version': version,
                    'key': key,
                }
            else:
                raise ValueError('unsupported version:', version)
        else:
            raise AssertionError('Meta parameters error')
        # check meta version
        if version == cls.Version_MKM or version == cls.Version_ExBTC:
            # verify seed and fingerprint
            if not key.verify(seed.encode('utf-8'), fingerprint):
                raise ValueError('Meta data not math')
        # new Meta(dict)
        self = super().__new__(cls, meta)
        self.version = version
        self.seed = seed
        self.key = key
        self.fingerprint = fingerprint
        return self

    @classmethod
    def generate(cls, private_key: PrivateKey, seed: str='', version: chr=DefaultVersion):
        """ Generate meta info with seed and private key """
        if version == cls.Version_MKM or version == cls.Version_ExBTC:
            # generate fingerprint with private key
            fingerprint = private_key.sign(seed.encode('utf-8'))
            dictionary = {
                'version': version,
                'seed': seed,
                'key': private_key.publicKey,
                'fingerprint': base64_encode(fingerprint),
            }
            return Meta(dictionary)
        elif version == cls.Version_BTC:
            dictionary = {
                'version': version,
                'key': private_key.publicKey,
            }
            return Meta(dictionary)
        else:
            raise AssertionError('Invalid version')

    def match_identifier(self, identifier: ID) -> bool:
        """ Check ID(name+address) with meta info """
        return identifier.name == self.seed and self.match_address(address=identifier.address)

    def match_address(self, address: Address) -> bool:
        """ Check address with meta info """
        return self.generate_address(network=address.network, algorithm=address.algorithm) == address

    def generate_identifier(self, network: NetworkID, algorithm=Address.DefaultAlgorithm) -> ID:
        """ Generate ID with meta info and network ID """
        address = self.generate_address(network=network, algorithm=algorithm)
        return ID(name=self.seed, address=address)

    def generate_address(self, network: NetworkID, algorithm: int=Address.DefaultAlgorithm) -> Address:
        """ Generate address with meta info and network ID """
        if self.version == Meta.Version_MKM:
            # generate MKM address
            return Address(fingerprint=self.fingerprint, network=network, algorithm=algorithm)
        elif self.version == Meta.Version_BTC or self.version == Meta.Version_ExBTC:
            # generate BTC address
            return Address(fingerprint=self.key.data, network=network, algorithm=algorithm)

    def __eq__(self, other) -> bool:
        """ Check whether they can generate same IDs """
        if other:
            other = Meta(other)
        else:
            return False
        id1 = self.generate_identifier(network=NetworkID.Main)
        id2 = other.generate_identifier(network=NetworkID.Main)
        return id1 == id2
