#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ming Ke Ming Test
    ~~~~~~~~~~~~~~~~~

    Unit test for Ming-Ke-Ming
"""

from mkm.utils import *
import mkm

__author__ = 'Albert Moky'


def test_aes():
    print('---------------- test AES begin')

    info = {
        'algorithm': 'AES',
    }
    key = mkm.SymmetricKey(info)
    print(key)
    text = 'Hello world'
    data = text.encode('utf-8')
    ct = key.encrypt(data)
    pt = key.decrypt(ct)
    print(hex_encode(data) + ' -> ' + hex_encode(ct) + ' -> ' + hex_encode(pt))

    print('---------------- test AES end')


def test_rsa():
    print('---------------- test RSA begin')

    info = {
        'algorithm': 'RSA',
    }
    sk = mkm.PrivateKey(info)
    pk = sk.publicKey()
    print(sk)
    print(pk)

    text = 'Hello world!'
    data = text.encode('utf-8')
    ct = pk.encrypt(data)
    pt = sk.decrypt(ct)
    print(text + ' -> ' + base64_encode(ct))
    print(' -> ' + base64_encode(pt) + ' -> ' + pt.decode('utf-8'))

    sig = sk.sign(data)
    print('signature: ' + base64_encode(sig))
    if pk.verify(data, sig):
        print('signature verify OK!')
    else:
        print('signature error!')

    print('---------------- test RSA end')


def print_address(obj):
    info = {
        'network': obj.network,
        'number': obj.number,
        'valid': obj.valid,
    }
    print(obj + ':' + info.__str__())


def print_id(obj):
    info = {
        'name': obj.name,
        'address': obj.address,
        'terminal': obj.terminal,
    }
    print(obj + ':' + info.__str__())


def test_meta():
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
    print(meta)

    if meta.match_id(id1):
        print('meta match ID')
    else:
        print('meta NOT match ID')

    id2 = meta.build_id(0x08)
    address2 = meta.build_address(0x08)
    print_id(id2)
    print_address(address2)


def test_entity():
    print('---------------- test Entity begin')

    my_id = 'moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk'
    fingerprint = 'ld68TnzYqzFQMxeJ6N+aZa2jRf9d4zVx4BUiBlmur67ne8YZF08plhCiIhfyYDIwwW7K' \
                  'LaAHvK8gJbp0pPIzLR4bhzu6zRpDLzUQsq6bXgMp+WAiZtFm6IHWNUwUEYcr3iSvTn5L' \
                  '1HunRt7kBglEjv8RKtbNcK0t1Xto375kMlo='

    print('ID: ' + my_id)

    address = mkm.Address('4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
    print_address(address)

    ct = base64_decode(fingerprint)
    address = mkm.Address(fingerprint=ct, network=0x08, version=0x01)
    print_address(address)

    address = '4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk'
    address = mkm.Address(address)
    print_address(address)

    my_id = mkm.ID(string="moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk")
    print_id(my_id)

    my_id = mkm.ID(name='moky', address=address)
    print_id(my_id)

    print('---------------- test Entity end')


if __name__ == '__main__':

    test_aes()
    test_rsa()
    test_meta()
    test_entity()
