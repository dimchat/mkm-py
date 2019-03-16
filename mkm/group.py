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
    Group for assembly
    ~~~~~~~~~~~~~~~~~~

    Group with members
"""

from abc import abstractmethod, ABCMeta, ABC

from .identifier import ID
from .entity import Entity, IEntityDataSource


class Group(Entity):

    @property
    def founder(self) -> ID:
        return self.delegate.group_founder(group=self)

    @property
    def owner(self) -> ID:
        return self.delegate.group_owner(group=self)

    @property
    def members(self) -> list:
        return self.delegate.group_members(group=self)


#
#  Delegates
#


class IGroupDelegate(metaclass=ABCMeta):
    """
        Group Delegate
        ~~~~~~~~~~~~~~
    """

    @abstractmethod
    def group_create(self, identifier: ID) -> Group:
        """ Create group with ID """
        pass

    @abstractmethod
    def group_add_member(self, group: Group, member: ID) -> bool:
        """ Add member to group """
        pass

    @abstractmethod
    def group_remove_member(self, group: Group, member: ID) -> bool:
        """ Remove member from group """
        pass


class IGroupDataSource(IEntityDataSource, ABC):
    """
        User Data Source
        ~~~~~~~~~~~~~~~~
    """

    @abstractmethod
    def group_founder(self, group: Group) -> ID:
        """ Get founder of the group """
        pass

    @abstractmethod
    def group_owner(self, group: Group) -> ID:
        """ Get current owner of the group """
        pass

    @abstractmethod
    def group_members(self, group: Group) -> list:
        """ Get all members in the group """
        pass
