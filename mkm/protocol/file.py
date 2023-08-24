# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2023 by Moky <albert.moky@gmail.com>
#
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
from typing import Optional

from ..crypto import SymmetricKey


class PortableNetworkFile(ABC):
    """
        Transportable File
        ~~~~~~~~~~~~~~~~~~

        data format: {
            URL      : "http://...", // download from CDN
            data     : "...",        // base64_encode(fileContent)
            filename : "...",

            password : {             // symmetric key to decrypt file content
                algorithm : "AES",   // "DES", ...
                data      : "{BASE64_ENCODE}",
                ...
            }
        }
    """

    @property
    @abstractmethod
    def url(self) -> Optional[str]:
        # download URL from CDN
        raise NotImplemented

    @url.setter
    @abstractmethod
    def url(self, string: Optional[str]):
        raise NotImplemented

    @property
    @abstractmethod
    def data(self) -> Optional[bytes]:
        # when file data is too big, don't set it in this dictionary,
        # but upload it to a CDN and set the download URL instead.
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

    @property
    @abstractmethod
    def password(self) -> SymmetricKey:
        # password for decrypting the downloaded data from CDN,
        # default is a plain key, which just return the same data when decrypting.
        raise NotImplemented

    @password.setter
    @abstractmethod
    def password(self, key: SymmetricKey):
        raise NotImplemented
