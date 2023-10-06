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

from abc import ABC, abstractmethod
from typing import Optional, Union, Any, Dict, List


class ObjectCoder(ABC):
    """
        Object Coder
        ~~~~~~~~~~~~
        JsON, XML, ...

        1. encode object to string;
        2. decode string to object.
    """

    @abstractmethod
    def encode(self, obj: Any) -> str:
        """
        Encode Map/List object to str

        :param obj: Map or List
        :return: serialized string
        """
        raise NotImplemented

    @abstractmethod
    def decode(self, string: str) -> Optional[Any]:
        """
        Decode str to Map/List object

        :param string: serialized string
        :return: Map or List
        """
        raise NotImplemented


class JSON:
    coder: ObjectCoder = None

    @staticmethod
    def encode(obj: Any) -> str:
        # assert JSON.coder is not None, 'JSON parser not set yet'
        return JSON.coder.encode(obj=obj)

    @staticmethod
    def decode(string: str) -> Optional[Any]:
        # assert JSON.coder is not None, 'JSON parser not set yet'
        return JSON.coder.decode(string=string)


class MapCoder(ObjectCoder, ABC):
    """ coder for json <=> map """

    # Override
    def encode(self, obj: Dict) -> str:
        return JSON.encode(obj=obj)

    # Override
    def decode(self, string: str) -> Optional[Dict]:
        return JSON.decode(string=string)


class ListCoder(ObjectCoder, ABC):
    """ coder for json <=> list """

    # Override
    def encode(self, obj: List) -> str:
        return JSON.encode(obj=obj)

    # Override
    def decode(self, string: str) -> Optional[List]:
        return JSON.decode(string=string)


class JSONMap:
    coder = MapCoder()

    @staticmethod
    def encode(obj: Any) -> str:
        # assert JSONMap.coder is not None, 'JSONMap parser not set yet'
        return JSONMap.coder.encode(obj=obj)

    @staticmethod
    def decode(string: str) -> Optional[Any]:
        # assert JSONMap.coder is not None, 'JSONMap parser not set yet'
        return JSONMap.coder.decode(string=string)


class JSONList:
    coder = ListCoder()

    @staticmethod
    def encode(obj: Any) -> str:
        # assert JSONList.coder is not None, 'JSONList parser not set yet'
        return JSONList.coder.encode(obj=obj)

    @staticmethod
    def decode(string: str) -> Optional[Any]:
        # assert JSONList.coder is not None, 'JSONList parser not set yet'
        return JSONList.coder.decode(string=string)


#
#   Interfaces
#


def json_encode(obj: Union[Dict, List]) -> str:
    return JSON.encode(obj=obj)


def json_decode(string: str) -> Union[Dict, List, None]:
    return JSON.decode(string=string)
