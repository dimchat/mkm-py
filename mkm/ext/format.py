# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2024 Albert Moky
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
from typing import Optional, Dict

from ..types import Singleton

from ..format.encode import TransportableDataHelper
from ..format.file import PortableNetworkFileHelper
from ..format.helpers import FormatExtensions


# class GeneralFormatHelper(TransportableDataHelper, PortableNetworkFileHelper, ABC):
class GeneralFormatHelper(ABC):
    """ Format GeneralFactory """

    #
    #   Algorithm
    #

    @abstractmethod
    def get_format_algorithm(self, ted: Dict, default: Optional[str] = None) -> Optional[str]:
        raise NotImplemented


@Singleton
class SharedFormatExtensions:
    """ Format FactoryManager """

    def __init__(self):
        super().__init__()
        self.__helper: Optional[GeneralFormatHelper] = None

    @property
    def helper(self) -> Optional[GeneralFormatHelper]:
        return self.__helper

    @helper.setter
    def helper(self, helper: GeneralFormatHelper):
        self.__helper = helper

    #
    #   TED
    #

    @property
    def ted_helper(self) -> Optional[TransportableDataHelper]:
        return FormatExtensions.ted_helper

    @ted_helper.setter
    def ted_helper(self, helper: TransportableDataHelper):
        FormatExtensions.ted_helper = helper

    #
    #   PNF
    #

    @property
    def pnf_helper(self) -> Optional[PortableNetworkFileHelper]:
        return FormatExtensions.pnf_helper

    @pnf_helper.setter
    def pnf_helper(self, helper: PortableNetworkFileHelper):
        FormatExtensions.pnf_helper = helper
