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

from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QWidget

from lisp.core.signal import Connection
from lisp.ui.qclicklabel import QClickLabel
from lisp.utils.configuration import config


class CueWidget(QWidget):

    focus_changed = pyqtSignal(object)
    context_menu_request = pyqtSignal(object, QPoint)
    edit_request = pyqtSignal(object)

    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.cue = None
        self.selected = False

        if config['Theme']['current'] == 'LiSP':
            self.bg = 'rgba(70,70,70,255)'
            self.fg = 'rgba(177,177,177,255)'
        else:
            pal = QWidget().palette()
            self.bg = 'rgb' + str(pal.color(pal.Background).getRgb())
            self.fg = 'rgb' + str(pal.color(pal.Foreground).getRgb())

        self.setStyleSheet('background: rgba(0,0,0,0)')

        self.nameButton = QClickLabel(self)
        self.nameButton.setWordWrap(True)
        self.nameButton.setAlignment(Qt.AlignCenter)
        self.nameButton.setFocusPolicy(Qt.NoFocus)
        self.nameButton.clicked.connect(self.on_click)

    def contextMenuEvent(self, event):
        self.context_menu_request.emit(self, event.globalPos())

    def mouseMoveEvent(self, e):
        if(e.buttons() == Qt.LeftButton and
                (e.modifiers() == Qt.ControlModifier or
                 e.modifiers() == Qt.ShiftModifier)):
            mimeData = QMimeData()
            mimeData.setText('GridLayout_Drag&Drop')

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(self.grab(self.rect()))

            if e.modifiers() == Qt.ControlModifier:
                drag.exec_(Qt.MoveAction)
            else:
                drag.exec_(Qt.CopyAction)
        else:
            e.ignore()

    def select(self):
        self.selected = not self.selected
        self.update_style()

    def set_cue(self, cue):
        if self.cue is not None:
            raise Exception('Media already assigned')

        self.cue = cue

        # TODO: not properties
        if not hasattr(cue, 'background'):
            cue.background = self.bg
        if not hasattr(cue, 'color'):
            cue.color = self.fg
        if not hasattr(cue, 'font_size'):
            cue.font_size = 11

        self.cue_updated()

        # Cue updated
        #self.cue.updated.connect(self.cue_updated, Connection.QtQueued)

    def cue_updated(self):
        self.nameButton.setText(self.cue.name)
        self.update_style()

    def on_click(self, e):
        if e.button() != Qt.RightButton:
            if e.modifiers() == Qt.ShiftModifier:
                self.edit_request.emit(self.cue)
            elif e.modifiers() == Qt.ControlModifier:
                self.select()
            else:
                self.cue.execute()

    def update_style(self, style={}):
        stylesheet = 'background: '
        if 'background' in style:
            stylesheet += style['background'] + ';'
        else:
            stylesheet += self.cue.background + ';'

        stylesheet += 'color: '
        if 'color' in style:
            stylesheet += style['color'] + ';'
        else:
            stylesheet += self.cue.color + ';'

        stylesheet += 'font-size: '
        if 'font-size' in style:
            stylesheet += style['font-size'] + ';'
        else:
            stylesheet += str(self.cue.font_size) + 'pt;'

        stylesheet += 'border: 1 solid rgb(0,0,0);'
        stylesheet += 'border-radius: 6px;'

        if self.selected:
            stylesheet += 'text-decoration: underline;'

        self.nameButton.setStyleSheet(stylesheet)
        self.update()

    def resizeEvent(self, *args, **kwargs):
        self.update()

    def update(self):
        self.nameButton.setGeometry(self.rect())
