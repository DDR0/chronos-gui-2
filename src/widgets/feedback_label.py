# -*- coding: future_fstrings -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize, pyqtProperty

from debugger import *; dbg


class FeedbackLabel(QLabel):
	"""A flashy little error label. 
		
		Text is usually set by calling showMsg(…).
	"""
	
	#I'd like to make the error message flash, but that's a bit of a "stretch goal" right now.
	
	def __init__(self, parent=None, showHitRects=False):
		super().__init__(parent)
		
		self._customStyleSheet = ''
		
		# Set some default text, so we can see the widget.
		if not self.text():
			self.showError('«error message will go here»')
		
		if not showHitRects:
			self.hide()
			
		self._hideMessageTimer = QtCore.QTimer()
		self._hideMessageTimer.timeout.connect(self.hide)
	
	
	def sizeHint(self):
		return QSize(141, 21)
	
	
	def refreshStyle(self):
		self.setStyleSheet(f"""
			font-size: 14px;
			background: transparent;
			color: #c80000;
		""" + self._customStyleSheet)
	
	
	def showError(self, message: str='', *, timeout: int=0) -> None:
		"""Show a highlighted error message.
			
			Use .hide() when the condition has passed, or specify a
			timeout=x in seconds if the error is transient."""
		
		self.setStyleSheet(f"""
			font-size: 14px;
			background: transparent;
			color: #c80000;
		""" + self._customStyleSheet)
		
		message and self.setText(message)
		self.show()
		timeout and self._hideMessageTimer.start(timeout*1000)
	
	
	def showMessage(self, message: str='', *, timeout: int=30) -> None:
		"""Show a non-highlighted feedback message.
			
			Hides itself after 30 seconds. Can be overridden by
			setting timeout = x seconds. If x is 0 (or None), don't
			auto-hide."""
		
		self.setStyleSheet(f"""
			font-size: 14px;
			background: transparent;
			color: #000000;
		""" + self._customStyleSheet)
		
		message and self.setText(message)
		self.show()
		timeout and self._hideMessageTimer.start(timeout*1000)
	
	
	@pyqtProperty(str)
	def customStyleSheet(self):
		return self._customStyleSheet
	
	@customStyleSheet.setter
	def customStyleSheet(self, styleSheet):
		self._customStyleSheet = styleSheet
		self.refreshStyle()