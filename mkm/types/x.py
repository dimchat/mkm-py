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

import time


URI = str


class DateTime:

    def __init__(self, timestamp: float):
        super().__init__()
        self.__timestamp = timestamp  # seconds since the Epoch.
        self.__localtime = None

    @property
    def timestamp(self) -> float:
        """ seconds from 1970-01-01 00:00:00 """
        return self.__timestamp

    # Override
    def __str__(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', self.localtime)

    # Override
    def __repr__(self) -> str:
        return time.strftime('%a %b %d %H:%M:%S %Y', self.localtime)

    @property
    def localtime(self) -> time.struct_time:
        if self.__localtime is None:
            self.__localtime = time.localtime(self.__timestamp)
        return self.__localtime

    @property
    def year(self) -> int:
        """ year, for example, 1993 """
        return self.localtime.tm_year

    @property
    def month(self) -> int:
        """ month of year, range [1, 12] """
        return self.localtime.tm_mon

    @property
    def day(self) -> int:
        """ day of month, range [1, 31] """
        return self.localtime.tm_mday

    @property
    def weak_day(self) -> int:
        """ day of week, range [0, 6], Monday is 0 """
        return self.localtime.tm_wday

    @property
    def year_day(self) -> int:
        """ day of year, range [1, 366] """
        return self.localtime.tm_yday

    @property
    def hours(self) -> int:
        """ hours, range [0, 23] """
        return self.localtime.tm_hour

    @property
    def minutes(self) -> int:
        """ minutes, range [0, 59] """
        return self.localtime.tm_min

    @property
    def seconds(self) -> int:
        """ seconds, range [0, 61]) """
        return self.localtime.tm_sec

    #
    #  Factory
    #

    @classmethod
    def now(cls):
        seconds = time.time()
        return DateTime(timestamp=seconds)

    @classmethod
    def current_timestamp(cls) -> float:
        """ Return the current time in seconds since the Epoch. """
        return time.time()
