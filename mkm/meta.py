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

    version: chr = 1
    seed: str = ''
    key: PublicKey = None
    fingerprint: bytes = None

    valid: bool = False

    def __new__(cls, dictionary: dict=None,
                seed: str='', public_key: PublicKey=None, private_key: PrivateKey=None,
                fingerprint: bytes=None, version: chr=0x01):
        valid = False
        if dictionary:
            # return Meta object directory
            if isinstance(dictionary, Meta):
                return dictionary
            # get fields from dictionary
            version = dictionary['version']
            seed = dictionary['seed']
            key = dictionary['key']
            fingerprint = dictionary['fingerprint']
            # verify fingerprint with public key
            public_key = PublicKey(key)
            fingerprint = base64_decode(fingerprint)
            valid = public_key.verify(seed.encode('utf-8'), fingerprint)
        elif private_key:
            if version == 0x01:
                # generate fingerprint with private key
                public_key = private_key.publicKey()
                fingerprint = private_key.sign(seed.encode('utf-8'))
                valid = True
                dictionary = {
                    'version': version,
                    'seed': seed,
                    'key': public_key,
                    'fingerprint': base64_encode(fingerprint),
                }
        elif fingerprint:
            # verify fingerprint with public key
            valid = public_key.verify(seed.encode('utf-8'), fingerprint)
            if valid:
                dictionary = {
                    'version': version,
                    'seed': seed,
                    'key': public_key,
                    'fingerprint': base64_encode(fingerprint),
                }

        # new dict
        self = super(Meta, cls).__new__(cls, dictionary)
        self.version = version
        self.seed = seed
        self.key = public_key
        self.fingerprint = fingerprint
        self.valid = valid
        return self

    def match_id(self, identity: ID) -> bool:
        return identity.name == self.seed and self.match_address(identity.address)

    def match_address(self, address: Address) -> bool:
        return self.build_address(address.network) == address

    def build_id(self, network: NetworkID) -> ID:
        address = self.build_address(network)
        return ID(name=self.seed, address=address)

    def build_address(self, network: NetworkID) -> Address:
        if self.valid:
            return Address(fingerprint=self.fingerprint, network=network, version=self.version)
