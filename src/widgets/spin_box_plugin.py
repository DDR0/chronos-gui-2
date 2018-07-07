from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from spin_box import SpinBox


class SpinBoxPlugin(QPyDesignerCustomWidgetPlugin):

	def __init__(self, parent=None):
		super().__init__(parent)

		self.initialized = False

	def initialize(self, core):
		if not self.initialized:
			self.initialized = True

	def isInitialized(self):
		return self.initialized

	def createWidget(self, parent):
		return SpinBox(parent, inEditor=True)

	def name(self):
		return "SpinBox"

	def group(self):
		return "Chronos"

	def icon(self):
		return QIcon(QPixmap("../../assets/qt_creator/spin_box.svg"))

	def toolTip(self):
		return """A spin box with adjustable margins.
		
Margins are displayed in Qt Designer so we can work with them. They
are hidden in the app itself, but they are still clickable. This is
important to maximize touch area, which makes the spin box much
more clickable."""

	def whatsThis(self):
		return self.toolTip() # ¯\_(ツ)_/¯ I have no idea how to trigger this.

	def isContainer(self):
		return False

	def includeFile(self):
		return "spin_box"
