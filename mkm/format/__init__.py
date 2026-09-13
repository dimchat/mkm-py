# -*- coding: utf-8 -*-
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
    Data Format
    ~~~~~~~~~~~

    UTF-8, JsON, Hex, Base58, Base64, ...
    TED, PNF
"""

from .data import DataCoder, Hex, Base58, Base64

from .object import ObjectCoder, JSON
from .object import MapCoder, JSONMap

from .string import StringCoder, UTF8


from .ted import TransportableResource
from .ted import TransportableData, TransportableDataFactory

# from .ted import TransportableDataHelper
# from .ted import FormatExtensions, shared_format_extensions


__all__ = [

    #
    #   Format
    #

    'DataCoder', 'Hex', 'Base58', 'Base64',
    'ObjectCoder', 'JSON',
    'MapCoder', 'JSONMap',
    'StringCoder', 'UTF8',

    'TransportableResource',
    'TransportableData',

    #
    #   Factories
    #

    'TransportableDataFactory',

    #
    #   Extensions
    #

    # 'TransportableDataHelper',
    # 'FormatExtensions', 'shared_format_extensions',

]
