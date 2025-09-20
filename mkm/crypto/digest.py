# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
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
    Message Digest
    ~~~~~~~~~~~

    MD5, SHA1, SHA-256, Keccak256, RipeMD-160, ...
"""

from abc import ABC, abstractmethod


class MessageDigester(ABC):

    @abstractmethod
    def digest(self, data: bytes) -> bytes:
        raise NotImplemented


class SHA256:
    digester: MessageDigester = None

    @classmethod
    def digest(cls, data: bytes) -> bytes:
        # assert SHA256.digester is not None, 'SHA256 coder not set yet'
        return cls.digester.digest(data=data)


class KECCAK256:
    digester: MessageDigester = None

    @classmethod
    def digest(cls, data: bytes) -> bytes:
        # assert KECCAK256.digester is not None, 'KECCAK256 coder not set yet'
        return cls.digester.digest(data=data)


class RIPEMD160:
    digester: MessageDigester = None

    @classmethod
    def digest(cls, data: bytes) -> bytes:
        # assert RIPEMD160.digester is not None, 'RIPEMD160 coder not set yet'
        return cls.digester.digest(data=data)


#
#   Interfaces
#


def sha256(data: bytes) -> bytes:
    return SHA256.digest(data=data)


def keccak256(data: bytes) -> bytes:
    return KECCAK256.digest(data=data)


def ripemd160(data: bytes) -> bytes:
    return RIPEMD160.digest(data=data)
