# -*- coding: future_fstrings -*-

from random import randint

from PyQt5.QtCore import Q_ENUMS, QSize, Qt, pyqtProperty
from PyQt5.QtWidgets import QSpinBox

from debugger import *; dbg
from touch_margin_plugin import TouchMarginPlugin, MarginWidth
from direct_api_link_plugin import DirectAPILinkPlugin
from focusable_plugin import FocusablePlugin


class SpinBox(QSpinBox, TouchMarginPlugin, DirectAPILinkPlugin, FocusablePlugin):
	Q_ENUMS(MarginWidth) #This is needed here. I don't know why the definition in the TouchMarginPlugin doesn't work.
	
	def __init__(self, parent=None, showHitRects=False):
		super().__init__(parent, showHitRects=showHitRects)
		self.clickMarginColor = f"rgba({randint(0, 32)}, {randint(128, 255)}, {randint(128, 255)}, {randint(32,96)})"
		self._units = ''
		
		self.isFocused = False
		self.jogWheelClick.connect(self.toggleFocussed)
		self.jogWheelLowResolutionRotation.connect(self.onLowResRotate)
	
	
	def sizeHint(self):
		return QSize(201, 81)
	
	
	def refreshStyle(self):
		if self.showHitRects:
			self.setStyleSheet(f"""
				SpinBox {{
					/* Editor style. Use border to show were click margin is, so we don't mess it up during layout. */
					font-size: 16px;
					border: 1px solid black;
					padding-right: 0px;
					padding-left: 10px;
					background: rgba(255,255,255,127); /* The background is drawn under the button borders, so they are opaque if the background is opaque. */
					
					/* use borders instead of margins so we can see what we're doing */
					border-left:   {self.clickMarginLeft   * 10 + 1}px solid {self.clickMarginColor};
					border-right:  {self.clickMarginRight  * 10 + 1}px solid {self.clickMarginColor};
					border-top:    {self.clickMarginTop    * 10 + 1}px solid {self.clickMarginColor};
					border-bottom: {self.clickMarginBottom * 10 + 1}px solid {self.clickMarginColor};
				}}
				SpinBox:disabled {{ 
					color: #969696;
				}}
				SpinBox::up-button, SpinBox::down-button {{
					width: 0px; /*These buttons just take up room. We have a jog wheel for them.*/
				}}
			""" + self.originalStyleSheet())
		else:
			self.setStyleSheet(f"""
				SpinBox {{ 
					border: 1px solid black;
					padding-right: 0px;
					padding-left: 10px;
					font-size: 16px;
					background: white;
					
					/* Add some touch space so this widget is easier to press. */
					margin-left: {self.clickMarginLeft*10}px;
					margin-right: {self.clickMarginRight*10}px;
					margin-top: {self.clickMarginTop*10}px;
					margin-bottom: {self.clickMarginBottom*10}px;
				}}
				SpinBox:disabled {{ 
					color: #969696;
				}}
				SpinBox::up-button, SpinBox::down-button {{
					width: 0px; /*These buttons just take up room. We have a jog wheel for them.*/
				}}
			""" + self.originalStyleSheet())
	
	
	@pyqtProperty(str)
	def units(self):
		return self._units
	@units.setter
	def units(self, newUnitCSVList):
		self._units = newUnitCSVList
	
	
	def onLowResRotate(self, delta, pressed):
		if self.isFocused:
			if pressed:
				self.injectKeystrokes(
					Qt.Key_PageUp if delta > 0 else Qt.Key_PageDown,
					count=abs(delta) )
			else:
				self.injectKeystrokes(
					Qt.Key_Up if delta > 0 else Qt.Key_Down,
					count=abs(delta) )
		else:
			if pressed:
				self.injectKeystrokes(
					Qt.Key_PageUp if delta > 0 else Qt.Key_PageDown,
					count=abs(delta) )
			else:
				self.selectWidget(delta)
	
	
	def toggleFocussed(self):
		self.isFocused = not self.isFocused
		if self.isFocused:
			self.window().focusRing.focusIn()
		else:
			self.window().focusRing.focusOut()