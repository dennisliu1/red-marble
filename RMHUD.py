#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import time
import random

class ShowWindWidget(QWidget):
	def __init__(self, width,height, parent):
		super(ShowWindWidget, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.resize(self.width,self.height)
		self.i = 0
		self.x = 0
		self.y = 0
		self.thread = ShowWindWidget.TimerThread(self)
		self.thread.Signal_Update.connect(self.triggerWind)

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawWind(event, qp)
		qp.end()

	def drawWind(self, event, qp):
		qp.drawImage(self.i*64,0,QImage('resources/Wind.png'))
	
	def triggerWind(self):
		self.i += 1
		self.repaint()

	def createWind(self):
		self.i = 0
		self.thread.start()

	class TimerThread(QThread):
		Signal_Update = pyqtSignal()
		def __init__(self, parent=None):
			super(ShowWindWidget.TimerThread, self).__init__()
			self.parent = parent
			
		def run(self):
			print 'start time thread'
			for h in range(4):
				time.sleep(1)
				self.Signal_Update.emit()
			self.parent.hide()

class RoverHPBar(QWidget):
	def __init__(self, width,height, parent):
		super(RoverHPBar, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.resize(self.width,self.height)
		self.roverHP = 0

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawBar(event, qp)
		qp.end()

	def drawBar(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setBrush(QColor(255,0,0))
		qp.drawRect(0,0, self.width-1,self.height-1)
		qp.setPen(QColor(0,0,0))
		qp.setFont(QFont('Times',10,75))
		qp.drawText(0,20, ' HP:'+str(self.roverHP))
		
	def setHP(self, hp):
		self.roverHP = hp

class BaseTimeBar(QWidget):
	def __init__(self, width,height, parent):
		super(BaseTimeBar, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.resize(self.width,self.height)
		self.hour = 0
		self.day = 0
		self.month = 0
	
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawBar(event, qp)
		qp.end()

	def drawBar(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setBrush(QColor(255,255,0))
		qp.drawRect(0,0, self.width-1,self.height-1)
		qp.setPen(QColor(0,0,0))
		qp.setFont(QFont('Times',10,75))
		qp.drawText(0,20, 'H:'+str(self.hour)+'D:'+str(self.day)+'M:'+str(self.month))
		
	def setHour(self, energy):
		self.hour = energy
	def setDay(self, energy):
		self.day = energy
	def setMonth(self, energy):
		self.month = energy

class BaseEnergyBar(QWidget):
	def __init__(self, width,height, parent):
		super(BaseEnergyBar, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.resize(self.width,self.height)
		self.baseUseEnergy = 0
		self.baseEnergy = 100
	
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawBar(event, qp)
		qp.end()

	def drawBar(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setBrush(QColor(255,255,0))
		qp.drawRect(0,0, self.width-1,self.height-1)
		qp.setPen(QColor(0,0,0))
		qp.setFont(QFont('Times',10,75))
		qp.drawText(0,20, ' Pwr:'+str(self.baseEnergy))
		#qp.drawText(45,20, 'Used:'+str(self.baseUseEnergy))
		
	def setEnergy(self, energy):
		self.baseEnergy = energy
	def setUseEnergy(self, energy):
		self.baseUseEnergy = energy

class BaseMetalBar(QWidget):
	def __init__(self, width,height, parent):
		super(BaseMetalBar, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.resize(self.width,self.height)
		self.baseMetal = 6000
	
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawBar(event, qp)
		qp.end()

	def drawBar(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setBrush(QColor(178,178,178))
		qp.drawRect(0,0, self.width-1,self.height-1)
		qp.setPen(QColor(0,0,0))
		qp.setFont(QFont('Times',10,75))
		qp.drawText(0,20, ' Metal:'+str(self.baseMetal))
		
	def setMetal(self, metal):
		self.baseMetal = metal

class RoverPIBar(QWidget):
	def __init__(self, width,height, parent):
		super(RoverPIBar, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.resize(self.width,self.height)
		self.pi = 0

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawBar(event, qp)
		qp.end()

	def drawBar(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setBrush(QColor(255,0,255))
		qp.drawRect(0,0, self.width-1,self.height-1)
		qp.setPen(QColor(0,0,0))
		qp.setFont(QFont('Times',10,75))
		qp.drawText(0,20, ' PI:'+str(self.pi))
		
	def setPI(self, pi):
		self.pi = pi
	
class BaseWeatherWidget(QWidget):
	def __init__(self, width,height, parent):
		super(BaseWeatherWidget, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.resize(self.width,self.height)
		self.windSpeed = 0
		self.windDirection = 'N'
		self.temperatureMin = -80
		self.temperatureMax = 20
		self.temperature = 0
	
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawBar(event, qp)
		qp.end()

	def drawBar(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setBrush(QColor(0,0,255))
		qp.drawRect(0,0, self.width-1,self.height-1)
		qp.setPen(QColor(0,0,0))
		qp.setFont(QFont('Times',10,75))
		qp.drawText(0,20, 'Wind:'+str(self.windSpeed)+'km/h '+self.windDirection)
		qp.drawText(0,40, 'Temp:'+str(self.temperature)+'\'C')
	
	def changeWindSpeed(self,wind):
		self.windSpeed = wind
	def changeWindDirection(self,direction):
		self.windDirection = direction
	def changeTemperature(self,temp):
		self.temperature = temp
	def changeTemperatureMin(temp):
		self.temperatureMin = temp
	def changeTemperatureMax(temp):
		self.temperatureMax = temp
