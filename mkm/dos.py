# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
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
    Disk Operating System
    ~~~~~~~~~~~~~~~~~~~~~

    File access
"""

import json
import os
from typing import Union, Optional


class File:

    def __init__(self, path: str):
        super().__init__()
        self.__path = path
        self.__data: Union[bytes, str, None] = None

    @classmethod
    def exists(cls, path: str) -> bool:
        return os.path.exists(path)

    @classmethod
    def make_dirs(cls, directory: str) -> bool:
        if cls.exists(directory):
            # directory exists
            return os.path.isdir(directory)
        try:
            os.makedirs(directory)
            return True
        except IOError:
            return False

    def read(self, mode: str='rb') -> Union[bytes, str, None]:
        if self.__data is not None:
            # get data from cache
            return self.__data
        if not self.exists(self.__path):
            # file not found
            return None
        if not os.path.isfile(self.__path):
            # the path is not a file
            raise IOError('%s is not a file' % self.__path)
        with open(self.__path, mode) as file:
            self.__data = file.read()
        return self.__data

    def write(self, data: Union[bytes, str], mode: str='wb') -> bool:
        directory = os.path.dirname(self.__path)
        if not self.make_dirs(directory):
            return False
        with open(self.__path, mode) as file:
            if len(data) == file.write(data):
                # OK, update cache
                self.__data = data
                return True

    def append(self, data: Union[bytes, str], mode: str='ab') -> bool:
        if not self.exists(self.__path):
            # new file
            return self.write(data=data, mode=mode)
        # append to exists file
        with open(self.__path, mode) as file:
            if len(data) == file.write(data):
                # OK, erase cache
                self.__data = None
                return True

    def remove(self, path: str=None) -> bool:
        if path is None:
            path = self.__path
        if self.exists(path):
            os.remove(path)
            return True


class TextFile(File):

    def read(self, mode: str='r') -> Optional[str]:
        return super().read(mode=mode)

    def write(self, text: str, mode: str='w') -> bool:
        return super().write(data=text, mode=mode)

    def append(self, text: str, mode: str='a') -> bool:
        return super().append(data=text, mode=mode)


class JSONFile(TextFile):

    def __init__(self, path: str):
        super().__init__(path=path)
        self.__container: Union[dict, list, None] = None

    def read(self, **kwargs) -> Union[dict, list, None]:
        if self.__container is not None:
            # get content from cache
            return self.__container
        # read as text file
        text = super().read()
        if text is not None:
            # convert text string to JsON object
            self.__container = json.loads(text)
        return self.__container

    def write(self, container: Union[dict, list], **kwargs) -> bool:
        # convert JsON object to text string
        text = json.dumps(container)
        if text is None:
            raise ValueError('cannot convert to JsON: %s' % container)
        if super().write(text=text):
            # OK, update cache
            self.__container = container
            return True

    def append(self, text: str, mode: str='a') -> bool:
        raise AssertionError('JsON file cannot append')
