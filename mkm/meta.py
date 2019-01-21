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

    DefaultVersion = 0x01

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
            seed = meta['seed']
            key = PublicKey(meta['key'])
            fingerprint = base64_decode(meta['fingerprint'])
        elif version and seed and key and fingerprint:
            # build meta info
            meta = {
                'version': version,
                'seed': seed,
                'key': key,
                'fingerprint': base64_encode(fingerprint),
            }
        else:
            raise AssertionError('Meta parameters error')
        # verify seed and fingerprint
        if version == Meta.DefaultVersion and key.verify(seed.encode('utf-8'), fingerprint):
            # new Meta(dict)
            self = super().__new__(cls, meta)
            self.version = version
            self.seed = seed
            self.key = key
            self.fingerprint = fingerprint
            return self
        else:
            raise ValueError('Meta data not math')

    @classmethod
    def generate(cls, seed: str, private_key: PrivateKey, version: chr=DefaultVersion):
        """ Generate meta info with seed and private key """
        if version == Meta.DefaultVersion:
            # generate fingerprint with private key
            fingerprint = private_key.sign(seed.encode('utf-8'))
            dictionary = {
                'version': version,
                'seed': seed,
                'key': private_key.publicKey,
                'fingerprint': base64_encode(fingerprint),
            }
            return Meta(dictionary)
        else:
            raise AssertionError('Invalid version')

    def match_identifier(self, identifier: ID) -> bool:
        """ Check ID with meta info """
        return identifier.name == self.seed and self.match_address(identifier.address)

    def match_address(self, address: Address) -> bool:
        """ Check address with meta info """
        return self.generate_address(address.network) == address

    def generate_identifier(self, network: NetworkID) -> ID:
        """ Generate ID with meta info and network ID """
        return ID.generate(seed=self.seed, fingerprint=self.fingerprint, network=network, version=self.version)

    def generate_address(self, network: NetworkID) -> Address:
        """ Generate address with meta info and network ID """
        return Address.generate(fingerprint=self.fingerprint, network=network, version=self.version)
