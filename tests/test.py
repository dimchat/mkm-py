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
from mkm.immortals import Immortals


immortals = Immortals()
moki_id = immortals.identifier(string='moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
hulk_id = immortals.identifier(string='hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj')


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

    def test_meta(self):
        username = 'moky'
        sk = PrivateKey({'algorithm': 'RSA'})
        meta = Meta.generate(seed=username, private_key=sk)
        print('meta: %s' % json.dumps(meta))
        print('SK: %s' % json.dumps(sk))

    def check_x(self, meta_json: str, sk_json: str):
        dict1 = json.loads(meta_json)
        meta = Meta(dict1)
        identifier = meta.generate_identifier(network=NetworkID.Main)
        print("meta: %s" % meta)
        print("ID: %s" % identifier)

        dict2 = json.loads(sk_json)
        sk = PrivateKey(dict2)
        print("SK: %s" % sk)
        self.assertTrue(meta.key.match(sk))

        name = "moky"
        data = name.encode("UTF-8")
        CT = meta.key.encrypt(data)
        PT = sk.decrypt(CT)
        hex = hex_encode(CT)
        res = PT.decode("UTF-8")
        print("encryption: %s -> %s -> %s" % (name, hex, res))

    def test_java_meta(self):
        print("checking data from Java ...")
        s1 = "{\"seed\":\"moky\",\"fingerprint\":\"m76nBPhABBTG4LmLlxzp4s3o2n4EdEsjDE60EHDtQme8gY9mPf7sr41eDbbpmzH2QnNlulh2Jh8ryr99rYnjBFe7o0HtWpOP1ea/kTCZb1qRHKgg0/JvDghYoHAElAdMHWtJMTwxCJIW+ei9HjQ4MZ10oCLmxFwtIN+qokcAcH4=\",\"version\":1,\"key\":{\"mode\":\"ECB\",\"padding\":\"PKCS1\",\"data\":\"-----BEGIN PUBLIC KEY-----\\r\\nMIGJAoGBAMOJODxrdcYaVtEvTMW3KmG3X4xhEor9+LWN03X4WyCk+PHncC4UtvYgMdfHXaL5JZXu\\r\\nPf52UOv5pNM21eo3SnRC2TN+DzwNKnLV83LxMuGMl/CPPmstdQVwg8Ru5NNNnEvtH3TxgmzfDRDm\\r\\ncfFEJp9PF27WfVpr4niWCy7NAHMTAgMBAAE=\\r\\n-----END PUBLIC KEY-----\",\"digest\":\"SHA256\",\"algorithm\":\"RSA\"}}\n"
        s2 = "{\"mode\":\"ECB\",\"padding\":\"PKCS1\",\"data\":\"-----BEGIN PUBLIC KEY-----\\r\\nMIGJAoGBAMOJODxrdcYaVtEvTMW3KmG3X4xhEor9+LWN03X4WyCk+PHncC4UtvYgMdfHXaL5JZXu\\r\\nPf52UOv5pNM21eo3SnRC2TN+DzwNKnLV83LxMuGMl/CPPmstdQVwg8Ru5NNNnEvtH3TxgmzfDRDm\\r\\ncfFEJp9PF27WfVpr4niWCy7NAHMTAgMBAAE=\\r\\n-----END PUBLIC KEY-----\\n-----BEGIN RSA PRIVATE KEY-----\\r\\nMIICXgIBAAKBgQDDiTg8a3XGGlbRL0zFtypht1+MYRKK/fi1jdN1+FsgpPjx53AuFLb2IDHXx12i\\r\\n+SWV7j3+dlDr+aTTNtXqN0p0Qtkzfg88DSpy1fNy8TLhjJfwjz5rLXUFcIPEbuTTTZxL7R908YJs\\r\\n3w0Q5nHxRCafTxdu1n1aa+J4lgsuzQBzEwIDAQABAoGATsOUeooS2+S6OfMiqrX4hXoXK/XiQUjC\\r\\niWeC2Y9cLc8mVFMU1gsUFBqt2Sx+pGpV4IoiQMEqIZPi+A2rp3f0LiH3oYpap4rBEJKpHO8dvNAy\\r\\n2yZjAAuwnVBw5Eahdh+vjxVAeblckPP1ktpl9KNJpnLFeT4wToJm7e2o4VZABokCQQDyZfFYiY0O\\r\\nqJQEtf2gAwCQDF/zk2r7HebW0lwhSkD+xup5akaGW5PJArIF2YMMs494DL/ACSlEDME2KhW+69uH\\r\\nAkEAzoIZnx1/E16+UwDQp3UtPL6oIaeVRtz4yjdq7RHBESvVrSi3M3n9artgv8qLyAstRuuw7Hz4\\r\\nlYvWuuGGS1NHFQJBAJ8xhlSwWZxz6GpDn6MT9a2lAus0OQFc/Pq+wtT2MENjHiDJRDH/OMq9427m\\r\\nECQqVSHxtYkIOzq+6bGJ6CgwPEcCQQCD6GqBTpALSWt9DXo6XQjGUmqHBMq/dwqb8IYmZD7UvxFA\\r\\nCE/tW7DZ6lLEb5aV8z26nXZnuPP4YliJCuGDX/B5AkEAyhXbQ2V1Vtf0ouuIEJoUvxlvqVMgKl9k\\r\\npydPVhWIoW4bj2NBnMgkptbt3GuK55NxvUCDfAgVD02VsObeW67L+Q==\\r\\n-----END RSA PRIVATE KEY-----\",\"digest\":\"SHA256\",\"algorithm\":\"RSA\"}\n"
        self.check_x(s1, s2)

    def test_oc_meta(self):
        print("checking data from Obj-C ...")
        s1 = "{\"fingerprint\":\"HLpTHlWIr\\/Hzd7l9\\/+8iAYgeOQI2gezR4TLs\\/WYR0sJZYKnVJeHeTijbwtze0t7Ak\\/K7U8TVnnlubRXE7N\\/Dio0\\/1PZmhoW95j40zVOjlxc13n54S4ZKVH7laZUmGtNLEkKsj+4Vr\\/RybJJhGQMwHO2h3q0ueIQj6nrI6fWCX9I=\",\"key\":{\"algorithm\":\"RSA\",\"data\":\"-----BEGIN PUBLIC KEY-----\\nMIGJAoGBANHKUezJ7gH1RTnYhnRZrMrONd3\\/RKV+UthgU4uwVsA7jJz\\/JwJWhsLY\\nX1BsSJRcQRnpWYSUxkzjU34FhUW28oFPvTrtzFM41AhLhE8MYP8vy9\\/\\/TK0OAFwY\\nwY1pqEJJKdbbOVCHLI1Ddu1CbHmLdQ2NF+10nszrJGxJLDnNadZnAgMBAAE=\\n-----END PUBLIC KEY-----\\n\",\"digest\":\"SHA256\",\"mode\":\"ECB\",\"padding\":\"PKCS1\"},\"seed\":\"moky\",\"version\":1}"
        s2 = "{\"algorithm\":\"RSA\",\"data\":\"-----BEGIN RSA PRIVATE KEY-----\\nMIICXAIBAAKBgQDRylHsye4B9UU52IZ0WazKzjXd\\/0SlflLYYFOLsFbAO4yc\\/ycC\\nVobC2F9QbEiUXEEZ6VmElMZM41N+BYVFtvKBT7067cxTONQIS4RPDGD\\/L8vf\\/0yt\\nDgBcGMGNaahCSSnW2zlQhyyNQ3btQmx5i3UNjRftdJ7M6yRsSSw5zWnWZwIDAQAB\\nAoGAKeT00kwK9yIjVmdqhk6oJoHimPgSndfptGMcG\\/+1e0MJFAsSH7HmzH9IHXfa\\nUKJRr9p9MXBCX3VgJYD1udPMfnCxCnL9CLnqxjPWJ+SISumV2g8PYVEPCVnN+zBp\\njBLpoeQS43c4heyF3DM41x6QrSGXtofUJ1W4U0VejnvlosECQQDvqp\\/6rkT4mjqj\\nMAGHWnIr2cbnt2UqQH85viSx3pLyPXn5FnDI1EiEU\\/Pi+XuxoTCtxWd+gx9aWRpY\\n+mXcK\\/YnAkEA4BZ0ukPDr8e5KmQN7x5x\\/CfHhqPRGVk4VH9z+icJ0\\/DvH9+7Nj30\\n5i8T6kAyGWdYoxkhQydmwi6Fpx6SxGWFwQJAQxkV6OzZSnCDciSCiQ59YGF8Gmtx\\n2z5rYBMn2tRhd4hWmbH6qX8lPkbyxNzsEHL8Weoma3jyUi0X\\/0k7M0TriQJBALv6\\nGnEl50HNiMbGp+mu4G9l7zpCsWVSMq6vO9rcZKIlunJCfAlEb+uoEkyvDVfCGdi3\\ne++ZXdoGrJdETlnx0AECQDQEW7kuBhHQ4cZ9v+qY7PfM87qM7EdsCm1QTNJ48n9I\\nJWeoVaoTQkKb+vB\\/JOjuNx9FHmqySKkNMkTqPNlFCFI=\\n-----END RSA PRIVATE KEY-----\\n\",\"digest\":\"SHA256\",\"mode\":\"ECB\",\"padding\":\"PKCS1\"}"
        self.check_x(s1, s2)


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

        moki_meta = immortals.meta(identifier=moki_id)

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
        # self.assertTrue(is_broadcast(id2))

        print_id(ANYONE)
        id3 = ID('anyone@anywhere')
        print_id(id3)
        self.assertEqual(ANYONE, id3)
        self.assertIsNot(ANYONE, id3)
        self.assertTrue(id3.is_broadcast)

        print_id(EVERYONE)
        id4 = ID('everyone@everywhere')
        print_id(id4)
        self.assertEqual(EVERYONE, id4)
        self.assertIsNot(EVERYONE, id4)
        self.assertTrue(id4.is_broadcast)

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

        e1.delegate = immortals
        e2.delegate = immortals

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

        address = Address('4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
        address = Address(address)
        print('address: %s' % address)

        id1 = moki_id
        meta1 = immortals.meta(identifier=id1)
        print('ID: ', id1, ', meta: ', meta1)
        self.assertTrue(meta1.match_identifier(id1), 'meta not match ID')

        sk1 = immortals.private_key_for_signature(identifier=id1)
        print('private key: ', sk1)
        self.assertTrue(meta1.key.match(sk1), 'meta key not match private key')

        account1 = User(id1)
        account1.delegate = immortals

        print('account1: ', account1)

        id2 = ID(hulk_id)
        sk2 = immortals.private_key_for_signature(identifier=id2)

        user2 = User(id2)
        user2.delegate = immortals

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

    def test_profile(self):
        print('\n---------------- %s' % self)

        id1 = ID(moki_id)
        profile = immortals.profile(identifier=id1)
        print('profile: ', profile)

        profile2 = Profile.new(identifier=id1)
        print('profile2: ' , profile2)


if __name__ == '__main__':
    unittest.main()
