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

from lisp.backends.base.media_element import ElementType, MediaType
from lisp.backends.gst.gst_element import GstMediaElement
from lisp.backends.gst.gi_repository import Gst


class UriInput(GstMediaElement):
    ElementType = ElementType.Input
    MediaType = MediaType.Audio
    Name = "URIInput"

    _properties_ = ('uri', 'download', 'buffer_size', 'use_buffering')

    def __init__(self, pipe):
        super().__init__()

        self._decoder = Gst.ElementFactory.make("uridecodebin", None)
        self._convert = Gst.ElementFactory.make("audioconvert", None)
        self._handler = self._decoder.connect("pad-added", self.__on_pad_added)

        pipe.add(self._decoder)
        pipe.add(self._convert)

        self.uri = ""
        self.download = False
        self.buffer_size = -1
        self.use_buffering = False

        self.property_changed.connect(self.__property_changed)

    def input_uri(self):
        return self.uri

    def dispose(self):
        self._decoder.disconnect(self._handler)

    def src(self):
        return self._convert

    def __on_pad_added(self, *args):
        self._decoder.link(self._convert)

    def __property_changed(self, name, value):
        name.replace('_', '-')
        self._decoder.set_property(name, value)
