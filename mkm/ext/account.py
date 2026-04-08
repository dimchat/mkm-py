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

from ..protocol import ID
from ..protocol.entity import AccountExtensions


# -----------------------------------------------------------------------------
#  Account Extensions
# -----------------------------------------------------------------------------


# class GeneralAccountHelper(AddressHelper, IDHelper, MetaHelper, DocumentHelper, ABC):
class GeneralAccountHelper(ABC):
    """ Account GeneralFactory """

    @abstractmethod
    def get_meta_type(self, meta: Dict, default: Optional[str] = None) -> Optional[str]:
        raise NotImplemented

    @abstractmethod
    def get_document_type(self, document: Dict, default: Optional[str] = None) -> Optional[str]:
        raise NotImplemented

    @abstractmethod
    def get_document_id(self, document: Dict) -> Optional[ID]:
        raise NotImplemented


class _AccountExt:
    _account_helper: Optional[GeneralAccountHelper] = None

    @property
    def account_helper(self) -> Optional[GeneralAccountHelper]:
        return _AccountExt._account_helper

    @account_helper.setter
    def account_helper(self, helper: GeneralAccountHelper):
        _AccountExt._account_helper = helper


AccountExtensions.helper = _AccountExt.account_helper
