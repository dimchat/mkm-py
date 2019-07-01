#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ming Ke Ming Test
    ~~~~~~~~~~~~~~~~~

    Unit test for Ming-Ke-Ming
"""

import unittest

from binascii import b2a_hex, a2b_hex
import json

from mkm import *
from mkm.crypto.utils import *
from mkm.identifier import ANYONE, EVERYONE

from tests.immortals import moki_id, moki_meta, moki_sk
from tests.immortals import hulk_id, hulk_meta, hulk_sk
from tests.facebook import facebook


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
        key = SymmetricKey(info)
        print(key)
        text = 'Hello world'
        data = text.encode('utf-8')
        ct = key.encrypt(data)
        pt = key.decrypt(ct)
        print(hex_encode(data) + ' -> ' + hex_encode(ct) + ' -> ' + hex_encode(pt))

        self.assertEqual(data, pt, 'AES error')

    def test_rsa(self):
        print('\n---------------- %s' % self)

        info = {
            'algorithm': 'RSA',
        }
        sk = PrivateKey(info)
        pk = sk.public_key
        print(sk)
        print(pk)

        text = 'Hello world!'
        data = text.encode('utf-8')
        ct = pk.encrypt(data)
        pt = sk.decrypt(ct)
        print(text + ' -> ' + base64_encode(ct))
        print(' -> ' + base64_encode(pt) + ' -> ' + pt.decode('utf-8'))

        self.assertEqual(data, pt, 'RSA error')

        sig = sk.sign(data)
        print('signature: ' + base64_encode(sig))

        self.assertTrue(pk.verify(data, sig), 'signature not match')


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
        'type': identity.type,
    }
    print(identity, ':', info)


class BaseTestCase(unittest.TestCase):

    def test_keys(self):
        print('\n---------------- %s' % self)
        key = {'algorithm': 'RSA', 'data': '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDr2zVbMu4zFOdimKVD4DlW0Uol\nEtUocA9QESbKVdv8sjFY29JROrXNGHW0uD1cyGSLJyKVuDu7PnvgcUILeSpV+TEn\nNrMN5KSSTeWyOmh5n8NI5WqT3qpCk5vNMa4e/4/Yuh/Hy4d3KOmFO0cVa29e0GmV\nDHkGqw6f7uykdGVnNwIDAQAB\n-----END PUBLIC KEY-----'}
        pk = PublicKey(key)
        print('pk:', json.dumps(pk))
        data = base64_encode(pk.data)
        print('pk.data:', data)
        exp = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDr2zVbMu4zFOdimKVD4DlW0UolEtUocA9QESbKVdv8sjFY29JROrXNGHW0uD1cyGSLJyKVuDu7PnvgcUILeSpV+TEnNrMN5KSSTeWyOmh5n8NI5WqT3qpCk5vNMa4e/4/Yuh/Hy4d3KOmFO0cVa29e0GmVDHkGqw6f7uykdGVnNwIDAQAB'
        self.assertEqual(exp, data, 'RSA keys error')

    def test_meta(self):
        print('\n---------------- %s' % self)

        print('meta: ', moki_meta)

        ok = moki_meta.match_identifier(moki_id)
        self.assertTrue(ok, 'meta algorithm error')

        identifier = moki_meta.generate_identifier(NetworkID.Main)
        address = moki_meta.generate_address(NetworkID.Main)
        print_id(identifier)
        print_address(address)

    def test_id(self):
        print('\n---------------- %s' % self)

        moki = "moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk"
        id1 = ID(moki)
        id2 = ID(moki + "/home")

        print_id(id1)
        print_id(id2)
        self.assertTrue(id1 == id2, 'ID error with terminal')

        satoshi = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        id1 = ID(satoshi)
        id2 = ID(satoshi + '/btc')

        print_id(id1)
        print_id(id2)
        self.assertTrue(id1 == id2, 'ID error with terminal')

        print_id(ANYONE)
        id3 = ID('ANYONE@ANYWHERE')
        print_id(id3)
        self.assertIs(ANYONE, id3)

        print_id(EVERYONE)
        id4 = ID('EVERYONE@EVERYWHERE')
        print_id(id4)
        self.assertIs(EVERYONE, id4)

        info = {
            'func': 'test_id',
            'anyone': ANYONE,
            'everyone': EVERYONE,
            'id3': id3,
            'id4': id4,
        }
        print('info: ', info)

    def test_entity(self):
        print('\n---------------- %s' % self)

        id1 = ID("moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk")
        id2 = ID("moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk/home")
        print_id(id1)
        print_id(id2)

        e1 = Entity(id1)
        e2 = Entity(id2)

        e1.delegate = facebook
        e2.delegate = facebook

        print(e1)
        print(e2)
        self.assertTrue(e1 == e2, 'entity error with terminal')

        e2 = None
        self.assertTrue(e1 != e2, 'entity error')


class AccountTestCase(unittest.TestCase):

    def test_register(self):
        print('\n---------------- %s' % self)

        name = 'moky'

        for x in range(0, 10):
            sk = PrivateKey({'algorithm': 'RSA'})
            meta = Meta.generate(seed=name, private_key=sk)
            print(x, 'meta: ', meta)
            self.assertTrue(meta.key.match(sk), 'meta key not match private key')

            id1 = meta.generate_identifier(NetworkID.Main)
            print_id(id1)
            self.assertTrue(meta.match_identifier(id1), 'meta not match ID')

            if id1.number % 10000 == 9527:
                print('Got it!')
                break

    def test_account(self):
        print('\n---------------- %s' % self)

        id1 = ID(moki_id)
        meta1 = Meta(moki_meta)
        print('ID: ', id1, ', meta: ', meta1)
        self.assertTrue(meta1.match_identifier(id1), 'meta not match ID')

        sk1 = PrivateKey(moki_sk)
        print('private key: ', sk1)
        self.assertTrue(meta1.key.match(sk1), 'meta key not match private key')

        account1 = Account(id1)
        account1.delegate = facebook

        print('account1: ', account1)

        id2 = ID(hulk_id)
        sk2 = PrivateKey(hulk_sk)

        user2 = User(id2)
        user2.delegate = facebook

        print('user2: ', user2)
        # print('number: ', user2.number())
        print('number: ', user2.number)
        print('number: ', user2.number)
        print('number: ', user2.number)

        data = 'moky'.encode('utf-8')
        ct = user2.encrypt(data)
        pt = user2.decrypt(ct)
        self.assertEqual(data, pt, 'decryption error')

        sig = user2.sign(data)
        ok = user2.verify(data, sig)
        self.assertTrue(ok, 'signature error')


if __name__ == '__main__':
    unittest.main()
