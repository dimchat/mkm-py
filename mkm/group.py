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

from mkm.entity import ID, Entity


class Group(Entity):

    def __init__(self, identifier: ID):
        """
        Create Group with ID

        :param identifier: Group ID
        """
        if identifier.address.network.is_group():
            super().__init__(identifier)
            self.members = []
        else:
            raise ValueError('Group ID error')

    def addMember(self, member: ID):
        """
        Add group member by ID

        :param member: ID
        """
        if member not in self.members:
            self.members.append(member)

    def removeMember(self, member: ID):
        """
        Remove member by ID

        :param member: ID
        """
        if member in self.members:
            self.members.remove(member)

    def hasMember(self, member: ID) -> bool:
        """
        Check whether contains the member

        :param member: ID
        :return: True/False
        """
        return member in self.members
