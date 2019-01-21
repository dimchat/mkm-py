#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ming Ke Ming Test
    ~~~~~~~~~~~~~~~~~

    Unit test for Ming-Ke-Ming
"""

import unittest

from binascii import b2a_hex, a2b_hex

import mkm
from mkm.utils import *
from mkm.immortals import *


__author__ = 'Albert Moky'


def hex_encode(data: bytes) -> str:
    """ HEX Encode """
    return b2a_hex(data).decode('utf-8')


def hex_decode(string: str) -> bytes:
    """ HEX Decode """
    return a2b_hex(string)


class CryptoTestCase(unittest.TestCase):

    def test_aes(self):
        print('\n---------------- %s' % self)

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

    def test_rsa(self):
        print('\n---------------- %s' % self)

        info = {
            'algorithm': 'RSA',
        }
        sk = mkm.PrivateKey.generate(info)
        pk = sk.publicKey
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
        'number': identity.number,
    }
    print(identity, ':', info)


class BaseTestCase(unittest.TestCase):

    def test_meta(self):
        print('\n---------------- %s' % self)

        id1 = mkm.ID(moki_id)

        meta = mkm.Meta(moki_meta)
        print('meta: ', meta)

        ok = meta.match_identifier(id1)
        self.assertTrue(ok)

        id2 = meta.generate_identifier(mkm.NetworkID.Main)
        address2 = meta.generate_address(mkm.NetworkID.Main)
        print_id(id2)
        print_address(address2)

    def test_entity(self):
        print('\n---------------- %s' % self)

        my_id = mkm.ID("moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk")
        print_id(my_id)

        entity = mkm.Entity(my_id)
        print(entity)

        entity.name = 'Albert Moky'
        print(entity)


class AccountTestCase(unittest.TestCase):

    def test_register(self):
        print('\n---------------- %s' % self)

        name = 'moky'

        for x in range(0, 10):
            sk = mkm.PrivateKey.generate({'algorithm': 'RSA'})
            meta = mkm.Meta.generate(name, sk)
            print(x, 'meta: ', meta)
            self.assertTrue(meta.key.match(sk))

            id1 = meta.generate_identifier(mkm.NetworkID.Main)
            print_id(id1)
            self.assertTrue(meta.match_identifier(id1))

    def test_account(self):
        print('\n---------------- %s' % self)

        id1 = mkm.ID(moki_id)
        meta1 = mkm.Meta(moki_meta)
        print('ID: ', id1, ', meta: ', meta1)
        self.assertTrue(meta1.match_identifier(id1))

        sk1 = mkm.PrivateKey(moki_sk)
        print('private key: ', sk1)
        self.assertTrue(meta1.key.match(sk1))

        account1 = mkm.Account(id1, meta1.key)
        print('account1: ', account1)

        id2 = mkm.ID(hulk_id)
        sk2 = mkm.PrivateKey(hulk_sk)

        user2 = mkm.User(id2, sk2)
        print('user2: ', user2)
        # print('number: ', user2.number())
        print('number: ', user2.number)
        print('number: ', user2.number)
        print('number: ', user2.number)
        self.assertTrue(user2.publicKey.match(user2.privateKey))


if __name__ == '__main__':
    unittest.main()
