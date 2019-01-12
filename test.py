#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ming Ke Ming Test
    ~~~~~~~~~~~~~~~~~

    Unit test for Ming-Ke-Ming
"""
from Crypto.Hash import SHA256

import mkm

__author__ = 'Albert Moky'


def test_aes():
    print('---------------- test AES begin')

    info = {
        'algorithm': 'AES',
    }
    key = mkm.SymmetricKey.new(info)
    print(key)
    text = 'Hello world'
    data = text.encode('utf-8')
    ct = key.encrypt(data)
    pt = key.decrypt(ct)
    print(mkm.hex_encode(data) + ' -> ' + mkm.hex_encode(ct) + ' -> ' + mkm.hex_encode(pt))

    print('---------------- test AES end')


def test_rsa():
    print('---------------- test RSA begin')

    info = {
        'algorithm': 'RSA',
    }
    sk = mkm.PrivateKey.new(info)
    pk = sk.publicKey()
    print(sk)
    print(pk)

    text = 'Hello world!'
    data = text.encode('utf-8')
    ct = pk.encrypt(data)
    pt = sk.decrypt(ct)
    print(text + ' -> ' + mkm.base64_encode(ct))
    print(' -> ' + mkm.base64_encode(pt) + ' -> ' + pt.decode('utf-8'))
    SHA256.new(data)

    sig = sk.sign(data)
    print('signature: ' + mkm.base64_encode(sig))
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


def test_entity():
    print('---------------- test Entity begin')

    my_id = 'moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk'
    fingerprint = 'ld68TnzYqzFQMxeJ6N+aZa2jRf9d4zVx4BUiBlmur67ne8YZF08plhCiIhfyYDIwwW7K' \
                  'LaAHvK8gJbp0pPIzLR4bhzu6zRpDLzUQsq6bXgMp+WAiZtFm6IHWNUwUEYcr3iSvTn5L' \
                  '1HunRt7kBglEjv8RKtbNcK0t1Xto375kMlo='

    print('ID: ' + my_id)

    address = mkm.Address(string='4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
    print_address(address)

    ct = mkm.base64_decode(fingerprint)
    address = mkm.Address(fingerprint=ct, network=0x08, version=0x01)
    print_address(address)

    address = '4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk'
    address = mkm.Address(address)

    my_id = mkm.ID(string="moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk")
    print_id(my_id)

    my_id = mkm.ID(name='moky', address=address)
    print_id(my_id)

    print('---------------- test Entity end')


if __name__ == '__main__':

    test_aes()
    test_rsa()
    test_entity()
