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

from typing import Optional, Any, List, Dict

from ..types import URI, Converter
from ..types import Mapper
from ..crypto import DecryptKey

from .object import JSONMap
from .encode import TransportableData, TransportableDataFactory
from .file import PortableNetworkFile, PortableNetworkFileFactory


class FormatGeneralFactory:

    def __init__(self):
        super().__init__()
        self.__pnf_factory: Optional[PortableNetworkFileFactory] = None
        # str(algorithm) => TransportableData.Factory
        self.__ted_factories: Dict[str, TransportableDataFactory] = {}

    # noinspection PyMethodMayBeStatic
    def split(self, text: str) -> List[str]:
        """
        Split text string to array: ["{TEXT}", "{algorithm}", "{content-type}"]

        :param text: '{TEXT}', or
                     'base64,{BASE64_ENCODE}', or
                     'data:image/png;base64,{BASE64_ENCODE}'
        :return: text + algorithm
        """
        pos1 = text.find('://')
        if pos1 > 0:
            # [URL]
            return [text]
        else:
            # skip 'data:'
            pos1 = text.find(':') + 1
        array = []
        # seeking for 'content-type'
        pos2 = text.find(';', pos1)
        if pos2 > pos1:
            array.append(text[pos1:pos2])
            pos1 = pos2 + 1
        # seeking for 'algorithm'
        pos2 = text.find(',', pos1)
        if pos2 > pos1:
            array.insert(0, text[pos1:pos2])
            pos1 = pos2 + 1
        # OK
        if pos1 == 0:
            # [data]
            array.insert(0, text)
        else:
            # [data, algorithm, type]
            array.insert(0, text[pos1:])
        return array

    def decode(self, data: Any, default_key: str) -> Optional[Dict]:
        if isinstance(data, Mapper):
            return data.dictionary
        elif isinstance(data, Dict):
            return data
        text = data if isinstance(data, str) else str(data)
        if len(text) == 0:
            return None
        elif text.startswith('{') and text.endswith('}'):
            return JSONMap.decode(string=text)
        info = {}
        array = self.split(text=text)
        size = len(array)
        if size == 1:
            info[default_key] = array[0]
        else:
            assert size > 1, 'split error: %s => %s' % (text, array)
            info['data'] = array[0]
            info['algorithm'] = array[1]
            if size > 2:
                # 'data:...;...,...'
                info['content-type'] = array[2]
                if text.startswith('data:'):
                    info['URL'] = text
        return info

    #
    #   TED - Transportable Encoded Data
    #

    # noinspection PyMethodMayBeStatic
    def get_data_algorithm(self, ted: Dict[str, Any], default: Optional[str]) -> Optional[str]:
        value = ted.get('algorithm')
        return Converter.get_str(value=value, default=default)

    def set_transportable_data_factory(self, algorithm: str, factory: TransportableDataFactory):
        self.__ted_factories[algorithm] = factory

    def get_transportable_data_factory(self, algorithm: str) -> Optional[TransportableDataFactory]:
        return self.__ted_factories.get(algorithm)

    def create_transportable_data(self, algorithm: str, data: bytes) -> TransportableData:
        factory = self.get_transportable_data_factory(algorithm=algorithm)
        assert factory is not None, 'data algorithm not support: %s' % algorithm
        return factory.create_transportable_data(data=data)

    def parse_transportable_data(self, ted: Any) -> Optional[TransportableData]:
        if ted is None:
            return None
        elif isinstance(ted, TransportableData):
            return ted
        # unwrap
        info = self.decode(data=ted, default_key='data')
        if info is None:
            # assert False, 'TED error: %s' % ted
            return None
        algorithm = self.get_data_algorithm(info, default='*')
        factory = self.get_transportable_data_factory(algorithm=algorithm)
        if factory is None:
            assert algorithm != '*', 'TED factory not ready'
            factory = self.get_transportable_data_factory(algorithm='*')  # unknown
            assert factory is not None, 'default TED factory not found'
        return factory.parse_transportable_data(info)

    #
    #   PNF - Portable Network File
    #

    def set_portable_network_file_factory(self, factory: PortableNetworkFileFactory):
        self.__pnf_factory = factory

    def get_portable_network_file_factory(self) -> Optional[PortableNetworkFileFactory]:
        return self.__pnf_factory

    def create_portable_network_file(self, data: Optional[TransportableData], filename: Optional[str],
                                     url: Optional[URI], password: Optional[DecryptKey]) -> PortableNetworkFile:
        factory = self.get_portable_network_file_factory()
        assert factory is not None, 'PNF factory not ready'
        return factory.create_portable_network_file(data=data, filename=filename, url=url, password=password)

    def parse_portable_network_file(self, pnf: Any) -> Optional[PortableNetworkFile]:
        if pnf is None:
            return None
        elif isinstance(pnf, PortableNetworkFile):
            return pnf
        # unwrap
        info = self.decode(data=pnf, default_key='URL')
        if info is None:
            # assert False, 'PNF error: %s' % pnf
            return None
        factory = self.get_portable_network_file_factory()
        assert factory is not None, 'PNF factory not ready'
        return factory.parse_portable_network_file(info)


# Singleton
class FormatFactoryManager:

    general_factory = FormatGeneralFactory()
