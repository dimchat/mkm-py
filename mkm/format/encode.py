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

from .helpers import FormatExtensions


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

    # DEFAULT = 'base64'
    # BASE_64 = 'base64'
    # BASE_58 = 'base58'
    # HEX = 'hex'

    @property
    @abstractmethod
    def algorithm(self) -> Optional[str]:
        """
        Get data encode algorithm

        :return: 'base64'
        """
        raise NotImplemented

    @property
    @abstractmethod
    def data(self) -> Optional[bytes]:
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
    def object(self) -> Any:
        """
        to_json()

        :return: str, or dict
        """
        return NotImplemented

    #
    #  Conveniences
    #

    @classmethod
    def encode(cls, data: bytes) -> Any:
        ted = cls.create(data=data)
        # assert isinstance(ted, TransportableData), 'should not happen'
        return ted.object

    @classmethod
    def decode(cls, encoded: Any) -> Optional[bytes]:
        ted = cls.parse(encoded)
        if ted is not None:  # isinstance(ted, TransportableData):
            return ted.data

    #
    #  Factory methods
    #

    @classmethod
    def create(cls, data: bytes, algorithm: str = None):  # -> TransportableData;
        helper = ted_helper()
        return helper.create_transportable_data(data=data, algorithm=algorithm)

    @classmethod
    def parse(cls, ted: Any):  # -> Optional[TransportableData]:
        helper = ted_helper()
        return helper.parse_transportable_data(ted)

    @classmethod
    def get_factory(cls, algorithm: str):  # -> Optional[TransportableDataFactory]:
        helper = ted_helper()
        return helper.get_transportable_data_factory(algorithm=algorithm)

    @classmethod
    def set_factory(cls, algorithm: str, factory):
        helper = ted_helper()
        helper.set_transportable_data_factory(algorithm=algorithm, factory=factory)


def ted_helper():
    helper = FormatExtensions.ted_helper
    assert isinstance(helper, TransportableDataHelper), 'TED helper error: %s' % helper
    return helper


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
    def parse_transportable_data(self, ted: Dict) -> Optional[TransportableData]:
        """
        Parse map object to TED

        :param ted: TED info
        :return: TED object
        """
        raise NotImplemented


########################
#                      #
#   Plugins: Helpers   #
#                      #
########################


class TransportableDataHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_transportable_data_factory(self, algorithm: str, factory: TransportableDataFactory):
        raise NotImplemented

    @abstractmethod
    def get_transportable_data_factory(self, algorithm: str) -> Optional[TransportableDataFactory]:
        raise NotImplemented

    @abstractmethod
    def create_transportable_data(self, data: bytes, algorithm: Optional[str]) -> TransportableData:
        raise NotImplemented

    @abstractmethod
    def parse_transportable_data(self, ted: Any) -> Optional[TransportableData]:
        raise NotImplemented
