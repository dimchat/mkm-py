#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
        CT      = sign(seed, SK);
        hash    = ripemd160(sha256(CT));
        code    = sha256(sha256(network + hash)).prefix(4);
        address = base58_encode(network + hash + code);
        number  = uint(code);
"""

from mkm.utils import base64_encode, base64_decode
from mkm.crypto import PublicKey, PrivateKey

from mkm.address import NetworkID, Address
from mkm.entity import ID


class Meta(dict):

    version: chr = 0x01
    seed: str = ''
    key: PublicKey = None
    fingerprint: bytes = None

    def __new__(cls, dictionary: dict=None,
                seed: str='', key: PublicKey=None, fingerprint: bytes=None, version: chr=0x01):
        """ Create meta object with meta info """
        if dictionary:
            # return Meta object directory
            if isinstance(dictionary, Meta):
                return dictionary
            # get fields from dictionary
            version = int(dictionary['version'])
            seed = dictionary['seed']
            key = PublicKey(dictionary['key'])
            fingerprint = base64_decode(dictionary['fingerprint'])
        elif seed and key and fingerprint:
            # build meta info
            dictionary = {
                'version': version,
                'seed': seed,
                'key': key,
                'fingerprint': base64_encode(fingerprint),
            }
        else:
            raise AssertionError('Parameters error')
        # verify seed and fingerprint
        if version == 0x01 and key.verify(seed.encode('utf-8'), fingerprint):
            # new dict
            self = super(Meta, cls).__new__(cls, dictionary)
            self.version = version
            self.seed = seed
            self.key = key
            self.fingerprint = fingerprint
            return self
        else:
            raise ValueError('Meta data not math')

    @classmethod
    def new(cls, seed: str, private_key: PrivateKey, version: chr=0x01):
        """ Create meta info with seed and private key """
        if version == 0x01:
            # generate fingerprint with private key
            fingerprint = private_key.sign(seed.encode('utf-8'))
            dictionary = {
                'version': version,
                'seed': seed,
                'key': private_key.publicKey(),
                'fingerprint': base64_encode(fingerprint),
            }
            return Meta(dictionary)
        else:
            raise AssertionError('Invalid version')

    def match_identity(self, identity: ID) -> bool:
        """ Check ID with meta info """
        return identity.name == self.seed and self.match_address(identity.address)

    def match_address(self, address: Address) -> bool:
        """ Check address with meta info """
        return self.build_address(address.network) == address

    def build_identity(self, network: NetworkID) -> ID:
        """ Build ID with meta info and network ID """
        address = self.build_address(network)
        return ID(name=self.seed, address=address)

    def build_address(self, network: NetworkID) -> Address:
        """ Build address with meta info and network ID """
        return Address.new(fingerprint=self.fingerprint, network=network, version=self.version)
