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
from typing import Optional, Union, Any

from ..types import Singleton
from ..types import Stringer


class TransportableResource(ABC):
    """
        Transportable Resource
        ~~~~~~~~~~~~~~~~~~~~~~

        TED - TransportableData
            0. "{BASE64_ENCODE}"
            1. "data:image/png;base64,{BASE64_ENCODE}"

        PNF - TransportableFile
            2. "https://..."
            3. {
                data     : "...",        // base64_encode(fileContent)
                filename : "avatar.png",

                URL      : "http://...", // download from CDN
                // before fileContent uploaded to a public CDN,
                // it can be encrypted by a symmetric key
                key      : {             // symmetric key to decrypt file content
                    algorithm : "AES",   // "DES", ...
                    data      : "{BASE64_ENCODE}",
                    ...
                }
            }
    """

    @abstractmethod
    def serialize(self) -> Union[str, dict]:
        """
        Serializes the resource into a transportable format.

        :return: str for formats 0, 1, 2 (Base64 string, Data URI, or URL)
                 dict for format 3 (structured JSON object as map)
        """
        raise NotImplemented


class TransportableData(Stringer, TransportableResource, ABC):
    """
        Transportable Data
        ~~~~~~~~~~~~~~~~~~
        TED - Transportable Encoded Data

            0. "{BASE64_ENCODE}"
            1. "data:image/png;base64,{BASE64_ENCODE}"
    """

    # DEFAULT = 'base64'
    # BASE_64 = 'base64'
    # BASE_58 = 'base58'
    # HEX = 'hex'

    @property
    @abstractmethod
    def encoding(self) -> Optional[str]:
        """
        Get data encode algorithm

        :return: 'base64'
        """
        raise NotImplemented

    @abstractmethod
    def to_bytes(self) -> Optional[bytes]:
        """
        Get original data

        :return: plaintext
        """
        raise NotImplemented

    # Override
    @abstractmethod
    def __len__(self) -> int:
        """
        Get the size of the raw binary data in bytes.

        :return: size in bytes
        """
        raise NotImplemented

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """
        Check whether this data is empty.

        :return: True or False
        """
        raise NotImplemented

    # Override
    @abstractmethod
    def __str__(self) -> str:
        """
        Get encoded string

        :return: '{BASE64_ENCODE}', or
                 'data:image/png;base64,{BASE64_ENCODE}'
        """
        raise NotImplemented

    # Override
    @abstractmethod
    def serialize(self) -> str:
        """
        Serializes this TED to a transportable string (same as [__str__]).

        :return: Encoded string representation (format 0 or 1)
        """
        return NotImplemented

    #
    #  Factory methods
    #

    @classmethod
    def parse(cls, ted: Any):  # -> Optional[TransportableData]:
        helper = ted_helper()
        return helper.parse_transportable_data(ted)

    @classmethod
    def get_factory(cls):  # -> Optional[TransportableDataFactory]:
        helper = ted_helper()
        return helper.get_transportable_data_factory()

    @classmethod
    def set_factory(cls, factory):
        helper = ted_helper()
        helper.set_transportable_data_factory(factory=factory)


def ted_helper():
    helper = shared_format_extensions.ted_helper
    assert isinstance(helper, TransportableDataHelper), 'TED helper error: %s' % helper
    return helper


class TransportableDataFactory(ABC):
    """ TED factory """

    @abstractmethod
    def parse_transportable_data(self, ted: str) -> Optional[TransportableData]:
        """
        Parse an encoded string to TED

        :param ted: Encoded string in TED format (0 or 1)
        :return: TED object
        """
        raise NotImplemented


# -----------------------------------------------------------------------------
#  Format Extensions
# -----------------------------------------------------------------------------


class TransportableDataHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_transportable_data_factory(self, factory: TransportableDataFactory):
        raise NotImplemented

    @abstractmethod
    def get_transportable_data_factory(self) -> Optional[TransportableDataFactory]:
        raise NotImplemented

    @abstractmethod
    def parse_transportable_data(self, ted: Any) -> Optional[TransportableData]:
        raise NotImplemented


@Singleton
class FormatExtensions:

    @property
    def ted_helper(self) -> Optional[TransportableDataHelper]:
        return _TedExt.ted_helper

    @ted_helper.setter
    def ted_helper(self, helper: Optional[TransportableDataHelper]):
        _TedExt.ted_helper = helper


class _TedExt:
    ted_helper: Optional[TransportableDataHelper] = None


# global
shared_format_extensions = FormatExtensions()
