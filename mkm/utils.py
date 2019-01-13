#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Utilities
    ~~~~~~~~~

    Crypto utilities
"""

import hashlib
import base58
import base64


def sha256(data: bytes) -> bytes:
    """ SHA-256 """
    # return SHA256.new(data).digest()
    return hashlib.sha256(data).digest()


def ripemd160(data: bytes) -> bytes:
    """ RIPEMD-160 """
    hash_obj = hashlib.new('ripemd160')
    hash_obj.update(data)
    return hash_obj.digest()


def base58_encode(data: bytes) -> str:
    """ BASE-58 Encode """
    return base58.b58encode(data).decode('utf-8')


def base58_decode(string: str) -> bytes:
    """ BASE-58 Decode """
    return base58.b58decode(string)


def base64_encode(data: bytes) -> str:
    """ BASE-64 Encode """
    return base64.b64encode(data).decode('utf-8')


def base64_decode(string: str) -> bytes:
    """ BASE-64 Decode """
    return base64.b64decode(string)
