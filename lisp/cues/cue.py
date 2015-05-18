# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2015 Francesco Ceruti <ceppofrancy@gmail.com>
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

from abc import abstractmethod
from enum import Enum
from uuid import uuid4

from lisp.core.has_properties import HasProperties
from lisp.core.signal import Signal


class Cue(HasProperties):
    """Cue(s) are the base component for implement any kind of live-controllable
    element (live = during a show).

    A cue implement his behavior(s) via the execute method, a cue can be
    executed trying to force a specific behavior. Any cue must provide the
    available "actions" via an enumeration named "CueAction".

    .. note::
        The execute implementation is can ignore the specified action if
        some condition is not matched (e.g. trying to pause a stopped track).

    Cue provide **(and any subclass should do the same)** properties via
    HasProperties/Property interfaces specifications.
    """

    class CueAction(Enum):
        """Actions supported by the cue.

        A subclass should override this, if implements more then one action.
        """
        Default = 0

    _properties_ = ['id', 'index', 'groups', 'name']

    def __init__(self, id_=None):
        super().__init__()

        #: Emitted before execution (object, action)
        self.on_execute = Signal()
        #: Emitted after execution (object, action)
        self.executed = Signal()

        self.id = str(uuid4()) if id_ is None else id_
        self.index = -1
        self.groups = []
        self.name = 'Untitled'

    @abstractmethod
    def execute(self, action=CueAction.Default):
        """Execute the specified action, if possible.

        :param action: the action to be performed
        """

    # TODO: are finalize/finalized really needed ??
    @abstractmethod
    def finalize(self):
        """Finalize the cue"""

    @abstractmethod
    def finalized(self):
        """
        :return: True if the cue is finalized, False otherwise
        :rtype: bool
        """
