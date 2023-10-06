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
from ..types import URI
from ..crypto import DecryptKey


class PortableNetworkFile(Mapper, ABC):
    """
        Transportable File
        ~~~~~~~~~~~~~~~~~~
        PNF - Portable Network File

            0. "{URL}"
            1. "base64,{BASE64_ENCODE}"
            2. "data:image/png;base64,{BASE64_ENCODE}"
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

    #
    #   When file data is too big, don't set it in this dictionary,
    #   but upload it to a CDN and set the download URL instead.
    #
    @property
    @abstractmethod
    def data(self) -> Optional[bytes]:
        raise NotImplemented

    @data.setter
    @abstractmethod
    def data(self, content: Optional[bytes]):
        raise NotImplemented

    @property
    @abstractmethod
    def filename(self) -> Optional[str]:
        raise NotImplemented

    @filename.setter
    @abstractmethod
    def filename(self, string: str):
        raise NotImplemented

    #
    #   Download URL
    #
    @property
    @abstractmethod
    def url(self) -> Optional[URI]:
        # download URL from CDN
        raise NotImplemented

    @url.setter
    @abstractmethod
    def url(self, string: Optional[URI]):
        raise NotImplemented

    #
    #   Password for decrypting the downloaded data from CDN,
    #   default is a plain key, which just return the same data when decrypting.
    #
    @property
    @abstractmethod
    def password(self) -> DecryptKey:
        raise NotImplemented

    @password.setter
    @abstractmethod
    def password(self, key: DecryptKey):
        raise NotImplemented

    @abstractmethod
    def __str__(self) -> str:
        """
        Get encoded string

        :return: 'URL', or
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
    #  Factory methods
    #

    @classmethod
    def create_from_url(cls, url: URI, password: Optional[DecryptKey]):
        return cls.create(url=url, password=password)

    @classmethod
    def create_from_data(cls, data: bytes, filename: Optional[str]):
        return cls.create(data=data, filename=filename)

    @classmethod
    def create(cls, data: bytes = None, filename: Optional[str] = None,
               url: URI = None, password: Optional[DecryptKey] = None):  # -> PortableNetworkFile:
        gf = general_factory()
        return gf.create_portable_network_file(data=data, filename=filename, url=url, password=password)

    @classmethod
    def parse(cls, pnf: Any):  # -> Optional[PortableNetworkFile]:
        gf = general_factory()
        return gf.parse_portable_network_file(pnf)

    @classmethod
    def factory(cls, algorithm: str):  # -> Optional[PortableNetworkFileFactory]:
        gf = general_factory()
        return gf.get_portable_network_file_factory(algorithm=algorithm)

    @classmethod
    def register(cls, algorithm: str, factory):
        gf = general_factory()
        gf.set_portable_network_file_factory(algorithm=algorithm, factory=factory)


def general_factory():
    from .factory import FormatFactoryManager
    return FormatFactoryManager.general_factory


class PortableNetworkFileFactory(ABC):
    """ PNF factory """

    @abstractmethod
    def create_portable_network_file(self, data: Optional[bytes], filename: Optional[str],
                                     url: Optional[URI], password: Optional[DecryptKey]) -> PortableNetworkFile:
        """
        Create PNF

        :param data:     file data (not encrypted)
        :param filename: file name
        :param url:      download URL
        :param password: decrypt key for downloaded data
        :return: PNF object
        """
        raise NotImplemented

    @abstractmethod
    def parse_portable_network_file(self, pnf: Dict[str, Any]) -> Optional[PortableNetworkFile]:
        """
        Parse map object to PNF

        :param pnf: PNF info
        :return: PNF object
        """
        raise NotImplemented
