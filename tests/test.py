#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ming Ke Ming Test
    ~~~~~~~~~~~~~~~~~

    Unit test for Ming-Ke-Ming
"""

import unittest

from binascii import b2a_hex, a2b_hex

from mkm.utils import *
import mkm

from tests.moki import *
from tests.hulk import *


__author__ = 'Albert Moky'


def hex_encode(data: bytes) -> str:
    """ HEX Encode """
    return b2a_hex(data).decode('utf-8')


def hex_decode(string: str) -> bytes:
    """ HEX Decode """
    return a2b_hex(string)


class CryptoTestCase(unittest.TestCase):

    def test_aes(self):
        print('---------------- test AES begin')

        info = {
            'algorithm': 'AES',
        }
        key = mkm.SymmetricKey.generate(info)
        print(key)
        text = 'Hello world'
        data = text.encode('utf-8')
        ct = key.encrypt(data)
        pt = key.decrypt(ct)
        print(hex_encode(data) + ' -> ' + hex_encode(ct) + ' -> ' + hex_encode(pt))

        self.assertEqual(data, pt)
        print('---------------- test AES end')

    def test_rsa(self):
        print('---------------- test RSA begin')

        info = {
            'algorithm': 'RSA',
        }
        sk = mkm.PrivateKey.generate(info)
        pk = sk.publicKey()
        print(sk)
        print(pk)

        text = 'Hello world!'
        data = text.encode('utf-8')
        ct = pk.encrypt(data)
        pt = sk.decrypt(ct)
        print(text + ' -> ' + base64_encode(ct))
        print(' -> ' + base64_encode(pt) + ' -> ' + pt.decode('utf-8'))

        self.assertEqual(data, pt)

        sig = sk.sign(data)
        print('signature: ' + base64_encode(sig))

        self.assertTrue(pk.verify(data, sig))
        print('---------------- test RSA end')


def print_address(address):
    info = {
        'network': address.network,
        'number': address.number,
    }
    print(address, ':', info)


def print_id(identity):
    info = {
        'name': identity.name,
        'address': identity.address,
        'terminal': identity.terminal,
    }
    print(identity, ':', info)


class BaseTestCase(unittest.TestCase):

    def test_meta(self):
        print('---------------- test Meta begin ')

        id1 = mkm.ID('moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
        seed = 'moki'
        key = {
            'algorithm': 'RSA',
            'data': '-----BEGIN PUBLIC KEY-----'
                    'MIGJAoGBALQOcgxhhV0XiHELKYdG587Tup261qQ3ahAGPuifZvxHXTq+GgulEyXiovwr'
                    'Vjpz7rKXn+16HgspLHpp5agv0WsSn6k2MnQGk5RFXuilbFr/C1rEX2X7uXlUXDMpsriK'
                    'FndoB1lz9P3E8FkM5ycG84hejcHB+R5yzDa4KbGeOc0tAgMBAAE='
                    '-----END PUBLIC KEY-----'
        }
        fingerprint = 'ld68TnzYqzFQMxeJ6N+aZa2jRf9d4zVx4BUiBlmur67ne8YZF08plhCiIhfyYDIwwW' \
                      '7KLaAHvK8gJbp0pPIzLR4bhzu6zRpDLzUQsq6bXgMp+WAiZtFm6IHWNUwUEYcr3iSv' \
                      'Tn5L1HunRt7kBglEjv8RKtbNcK0t1Xto375kMlo='

        meta = {
            'version': 0x01,
            'seed': seed,
            'key': key,
            'fingerprint': fingerprint,
        }

        meta = mkm.Meta(meta)
        print('meta: ', meta)

        ok = meta.match_identifier(id1)
        self.assertTrue(ok)

        id2 = meta.generate_identifier(mkm.NetworkID.Main)
        address2 = meta.generate_address(mkm.NetworkID.Main)
        print_id(id2)
        print_address(address2)

        print('---------------- test Meta end')

    def test_entity(self):
        print('---------------- test Entity begin')

        my_id = 'moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk'
        fingerprint = 'ld68TnzYqzFQMxeJ6N+aZa2jRf9d4zVx4BUiBlmur67ne8YZF08plhCiIhfyYDIwwW7K' \
                      'LaAHvK8gJbp0pPIzLR4bhzu6zRpDLzUQsq6bXgMp+WAiZtFm6IHWNUwUEYcr3iSvTn5L' \
                      '1HunRt7kBglEjv8RKtbNcK0t1Xto375kMlo='

        print('ID: ' + my_id)

        address = mkm.Address('4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
        print_address(address)

        ct = base64_decode(fingerprint)
        address = mkm.Address.generate(fingerprint=ct, network=mkm.NetworkID.Main)
        print_address(address)

        address = '4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk'
        address = mkm.Address(address)
        print_address(address)

        my_id = mkm.ID("moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk")
        print_id(my_id)

        my_id = mkm.ID(name='moky', address=address)
        print_id(my_id)

        entity = mkm.Entity(my_id)
        print(entity)

        entity.name = 'Albert Moky'
        print(entity)

        print('---------------- test Entity end')


class AccountTestCase(unittest.TestCase):

    def test(self):
        print('---------------- test Account begin')

        id1 = mkm.ID(id_moki)
        meta1 = mkm.Meta(meta_moki)
        self.assertTrue(meta1.match_identifier(id1))

        account1 = mkm.Account(id1, meta1.key)
        print('account1: ', account1)

        id2 = mkm.ID(id_hulk)
        sk2 = mkm.PrivateKey(sk_hulk)

        user2 = mkm.User(id2, sk2)
        print('user2: ', user2)

        print('---------------- test Account end')


if __name__ == '__main__':
    unittest.main()
