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
from collections.abc import Mapping
from typing import Optional

from ..protocol import ID
from ..protocol.entity import shared_account_extensions


# -----------------------------------------------------------------------------
#  Account Extensions
# -----------------------------------------------------------------------------


# class GeneralAccountHelper(AddressHelper, IDHelper, MetaHelper, DocumentHelper, ABC):
class GeneralAccountHelper(ABC):
    """ Account GeneralFactory """

    @abstractmethod
    def get_meta_type(self, meta: Mapping, default: Optional[str] = None) -> Optional[str]:
        """ Get type from the meta info """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_meta_type()'
        )

    @abstractmethod
    def get_document_type(self, document: Mapping, default: Optional[str] = None) -> Optional[str]:
        """ Get type from the document info """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_document_type()'
        )

    @abstractmethod
    def get_document_id(self, document: Mapping) -> Optional[ID]:
        """ Get did from the document info """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_document_id()'
        )


class GeneralAccountExtension:

    @property
    def helper(self) -> Optional[GeneralAccountHelper]:
        """ Get general account helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.helper getter'
        )

    @helper.setter
    def helper(self, delegate: GeneralAccountHelper):
        """ Set general account helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.helper setter'
        )


shared_account_extensions.helper: Optional[GeneralAccountHelper] = None


# def account_extensions() -> Union[GeneralAccountExtension, AccountExtensions]:
#     return shared_account_extensions
