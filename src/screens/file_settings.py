# -*- coding: future_fstrings -*-

import logging; log = logging.getLogger('Chronos.gui')

from PyQt5 import uic, QtWidgets, QtCore
# from PyQt5.QtCore import pyqtSlot

from debugger import *; dbg
import api2 as api
import settings
from animate import delay


class FileSettings(QtWidgets.QDialog):
	def __init__(self, window):
		super().__init__()
		uic.loadUi("src/screens/file_settings.ui", self)
		
		# Panel init.
		self.move(0, 0)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		
		# Button binding.
		#The preferred external partition is the one set in settings' preferredFileSavingUUID, OR the most recent partition.
		settings.observe('preferredFileSavingUUID', '', self.setPreferredSavingDevice)
		api.externalPartitions.observe(lambda *_: self.setPreferredSavingDevice(
			settings.value('preferredFileSavingUUID', '') ))
		self.uiSavedVideoLocation.currentIndexChanged.connect(lambda *_: 
			self.uiSavedVideoLocation.hasFocus() and settings.setValue(
				'preferredFileSavingUUID',
				(self.uiSavedVideoLocation.currentData() or {}).get('uuid') ) )
		
		
		self.uiSavedVideoName.setText(
			settings.value('savedVideoName', self.uiSavedVideoName.text()) )
		self.uiSavedVideoName.textChanged.connect(lambda value:
			settings.setText('savedVideoName', value) )
		
		self.uiSavedVideoFileExtention.setCurrentText(
			settings.value('savedVideoFileExtention', self.uiSavedVideoFileExtention.currentText()) )
		self.uiSavedVideoFileExtention.currentTextChanged.connect(lambda value:
			settings.setValue('savedVideoFileExtention', value) )
		
		
		self.uiSavedFileFramerate.setValue(
			settings.value('savedFileFramerate', self.uiSavedFileFramerate.value()) )
		self.uiSavedFileFramerate.valueChanged.connect(lambda value:
			settings.setValue('savedFileFramerate', value) )
		
		self.uiSavedFileBPP.setValue(
			settings.value('savedFileBPP', self.uiSavedFileBPP.value()) )
		self.uiSavedFileBPP.valueChanged.connect(lambda value:
			settings.setValue('savedFileBPP', value) )
		
		self.uiSavedFileMaxBitrate.setValue(
			settings.value('savedFileMaxBitrate', self.uiSavedFileMaxBitrate.value()) )
		self.uiSavedFileMaxBitrate.valueChanged.connect(lambda value:
			settings.setValue('savedFileMaxBitrate', value) )
		
		
		self.uiAutoSaveVideo.setCheckState( #[autosave]
			bool(settings.value('autoSaveVideo', self.uiAutoSaveVideo.checkState())) * 2 )
		self.uiAutoSaveVideo.stateChanged.connect(lambda value:
			settings.setValue('autoSaveVideo', bool(value)) )
		
		self.uiResumeRecordingAfterSave.setCheckState( #[autosave]
			bool(settings.value('resumeRecordingAfterSave', self.uiResumeRecordingAfterSave.checkState())) * 2 )
		self.uiResumeRecordingAfterSave.stateChanged.connect(lambda value:
			settings.setValue('resumeRecordingAfterSave', bool(value)) )
		
		
		self.uiStampData.clicked.connect(lambda: window.show('stamp'))
		self.uiDone.clicked.connect(window.back)
	
	
	
	def onShow(self):
		#Try, _again_, to set the drop-down to the correct value. Since this widget is
		#repopulated when the partitions change and on show, this is really hard. >_<
		api.externalPartitions.observe(lambda *_: self.setPreferredSavingDevice(
			settings.value('preferredFileSavingUUID', '') ))
		delay(self, 16, lambda:
			api.externalPartitions.observe(lambda *_: self.setPreferredSavingDevice(
				settings.value('preferredFileSavingUUID', '') )) )
	
	def setPreferredSavingDevice(self, device):
		try:
			self.uiSavedVideoLocation.setCurrentIndex(
				[partition['uuid'] for partition in api.externalPartitions.list()].index(device) )
		except ValueError: #Not found. Do nothing.
			pass