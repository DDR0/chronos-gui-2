# -*- coding: future_fstrings -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize

from debugger import *; dbg


class Subheader(QLabel):
	def __init__(self, parent=None, showHitRects=False):
		super().__init__(parent)
		
		self.setStyleSheet(f"""
			font-size: 18px;
			background: transparent; /*Don't mess with this, it affects font width.*/
		""" + self.styleSheet())
		
		# Set some default text, so we can see the widget.
		if not self.text():
			self.setText('Subheader')


	def sizeHint(self):
		return QSize(241, 21)