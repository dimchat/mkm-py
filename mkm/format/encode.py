# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2023 Albert Moky
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

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict

from ..types import Mapper


class TransportableData(Mapper, ABC):
    """
        Transportable Data
        ~~~~~~~~~~~~~~~~~~
        TED - Transportable Encoded Data

            0. "{BASE64_ENCODE}"
            1. "base64,{BASE64_ENCODE}"
            2. "data:image/png;base64,{BASE64_ENCODE}"
            3. {
                algorithm : "base64",
                data      : "...",      // base64_encode(data)
                ...
            }
    """

    #
    #   encode algorithm
    #
    DEFAULT = 'base64'
    BASE_64 = 'base64'
    BASE_58 = 'base58'
    HEX = 'hex'

    @property
    @abstractmethod
    def algorithm(self) -> str:
        """
        Get data encode algorithm

        :return: 'base64'
        """
        raise NotImplemented

    @property
    @abstractmethod
    def data(self) -> bytes:
        """
        Get original data

        :return: plaintext
        """
        raise NotImplemented

    @abstractmethod
    def __str__(self) -> str:
        """
        Get encoded string

        :return: '{BASE64_ENCODE}', or
                 'base64,{BASE64_ENCODE}', or
                 'data:image/png;base64,{BASE64_ENCODE}', or
                 '{...}'
        """
        raise NotImplemented

    @property
    @abstractmethod
    def object(self) -> object:
        """
        to_json()

        :return: str, or dict
        """
        return NotImplemented

    #
    #  Conveniences
    #

    @classmethod
    def encode(cls, data: bytes) -> object:
        ted = cls.create(data=data)
        # assert isinstance(ted, TransportableData), 'should not happen'
        return ted.object

    @classmethod
    def decode(cls, ted: Any) -> Optional[bytes]:
        ted = cls.parse(ted)
        if ted is not None:  # isinstance(ted, TransportableData):
            return ted.data

    #
    #  Factory methods
    #

    @classmethod
    def create(cls, data: bytes, algorithm: str = None):  # -> TransportableData;
        if algorithm is None:
            algorithm = cls.DEFAULT
        gf = general_factory()
        return gf.create_transportable_data(data=data, algorithm=algorithm)

    @classmethod
    def parse(cls, ted: Any):  # -> Optional[TransportableData]:
        gf = general_factory()
        return gf.parse_transportable_data(ted)

    @classmethod
    def factory(cls, algorithm: str):  # -> Optional[TransportableDataFactory]:
        gf = general_factory()
        return gf.get_transportable_data_factory(algorithm=algorithm)

    @classmethod
    def register(cls, algorithm: str, factory):
        gf = general_factory()
        gf.set_transportable_data_factory(algorithm=algorithm, factory=factory)


def general_factory():
    from .factory import FormatFactoryManager
    return FormatFactoryManager.general_factory


class TransportableDataFactory(ABC):
    """ TED factory """

    @abstractmethod
    def create_transportable_data(self, data: bytes) -> TransportableData:
        """
        Create TED

        :param data: original data
        :return: TED object
        """
        raise NotImplemented

    @abstractmethod
    def parse_transportable_data(self, ted: Dict[str, Any]) -> Optional[TransportableData]:
        """
        Parse map object to TED

        :param ted: TED info
        :return: TED object
        """
        raise NotImplemented
