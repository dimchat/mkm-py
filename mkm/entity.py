#! /usr/bin/env python
# -*- coding: utf-8 -*-

from mkm.crypto import *


class Meta(dict):
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
            version = dictionary['version']
            seed = dictionary['seed']
            key = dictionary['key']
            public_key = PublicKey(key)
            fingerprint = dictionary['fingerprint']
            fingerprint = base64_decode(fingerprint)
            valid = public_key.verify(seed.encode('utf-8'), fingerprint)
        elif private_key:
            if version == 0x01:
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
            valid = public_key.verify(seed.encode('utf-8'), fingerprint)
            if valid:
                dictionary = {
                    'version': version,
                    'seed': seed,
                    'key': public_key,
                    'fingerprint': base64_encode(fingerprint),
                }

        # new dict
        self = super(Meta, cls).__new__(dictionary)
        self.version = version
        self.seed = seed
        self.key = public_key
        self.fingerprint = fingerprint
        self.valid = valid
        return self


def user_number(code: bytes) -> int:
    """ Get user number, which for remembering and searching user """
    return int.from_bytes(code, byteorder='little')


class Address(str):
    """
        Address like BitCoin
        ~~~~~~~~~~~~~~~~~~~~

        data format: "network+digest+check_code"
            network    --  1 byte
            digest     -- 20 bytes
            check_code --  4 bytes

        algorithm:
            fingerprint = sign(seed, SK);
            digest      = ripemd160(sha256(fingerprint));
            check_code  = sha256(sha256(network + digest)).prefix(4);
            address     = base58_encode(network + digest + check_code);
    """

    network: chr = 0x00
    number: int = 0
    valid: bool = False

    def __new__(cls, string: str='',
                fingerprint: bytes=None, network: chr=0x00, version: chr=0x01):
        number = 0
        valid = False
        if string:
            data = base58_decode(string)
            prefix = data[:1]
            digest = data[1:-4]
            code = data[-4:]
            network = ord(prefix)
            number = user_number(code)
            valid = (sha256(sha256(prefix + digest))[:4] == code)
        elif fingerprint:
            if version == 0x01:
                prefix = chr(network).encode('utf-8')
                digest = ripemd160(sha256(fingerprint))
                code = sha256(sha256(prefix + digest))[:4]
                string = base58_encode(prefix + digest + code)
                number = user_number(code)
                valid = True

        # new str
        self = super(Address, cls).__new__(cls, string)
        self.network = network
        self.number = number
        self.valid = valid
        return self


class ID(str):
    """
        ID for entity (Account/Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: "name@address[/terminal]"

        filed(s):
            name     - entity name, the seed of fingerprint to build address
            address  - a string to identify an entity
            terminal - entity login resource(device), OPTIONAL
    """

    name: str = ''
    address: Address = None
    terminal: str = ''

    def __new__(cls, string: str='',
                name: str='', address: Address=None, terminal: str=''):
        if string:
            pair = string.split('@', 1)
            name = pair[0]
            pair = pair[1].split('/', 1)
            address = Address(string=pair[0])
            if pair.__len__() > 1:
                terminal = pair[1]
            else:
                terminal = ''
        elif terminal:
            string = name + '@' + address + '/' + terminal
            address = Address(string=address)
        else:
            string = name + '@' + address
            address = Address(string=address)

        # new str
        self = super(ID, cls).__new__(cls, string)
        self.name = name
        self.address = address
        self.terminal = terminal
        return self

    def number(self) -> int:
        return self.address.number


class Entity:
    """
        Entity (Account / Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~


    """

    ID: ID = None
    name: str = ''

    def __init__(self, entity_id):
        super(Entity, self).__init__()
        self.ID = entity_id
        self.name = ''

    def number(self) -> int:
        return self.ID.address.number
