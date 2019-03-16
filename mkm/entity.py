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

from abc import abstractmethod, ABCMeta

from .address import NetworkID
from .identifier import ID
from .meta import Meta


class Entity:
    """
        Entity (Account/Group)
        ~~~~~~~~~~~~~~~~~~~~~~

        Base class of Account and Group, ...
    """

    def __init__(self, identifier: ID):
        """
        Create Entity with ID

        :param identifier: User/Group ID
        """
        super().__init__()
        self.identifier = identifier
        self.delegate = None  # IEntityDataSource

    def __str__(self):
        clazz = self.__class__.__name__
        identifier = self.identifier
        network = identifier.address.network
        number = identifier.address.number
        name = self.name
        return '<%s: %s(%d|%d) "%s" />' % (clazz, identifier, network, number, name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.identifier == other.identifier

    @property
    def type(self) -> NetworkID:
        """ Entity type """
        return self.identifier.address.network

    @property
    def number(self) -> int:
        """ Search number of this entity """
        return self.identifier.address.number

    @property
    def name(self) -> str:
        nick = self.delegate.entity_name(entity=self)
        if nick:
            return nick
        nick = self.identifier.name
        if nick:
            return nick
        # BTC address
        return self.identifier.address

    @property
    def meta(self) -> Meta:
        return self.delegate.entity_meta(entity=self)


#
#  Delegate
#


class IEntityDataSource(metaclass=ABCMeta):
    """
        Entity Data Source
        ~~~~~~~~~~~~~~~~~~
    """

    @abstractmethod
    def entity_meta(self, entity: Entity) -> Meta:
        """ Get meta for this entity ID """
        pass

    @abstractmethod
    def entity_name(self, entity: Entity) ->str:
        """ Get name in this entity's profile """
        pass
