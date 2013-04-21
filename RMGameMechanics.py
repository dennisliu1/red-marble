#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import random
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class TimeThread(QThread):
	Signal_Hour_Update = pyqtSignal(int)
	Signal_Day_Update = pyqtSignal(int)
	Signal_Month_Update = pyqtSignal(int)
	def __init__(self, parent=None):
		super(TimeThread, self).__init__()
		self.parent = parent
		self.isRunning = True
		self.countMiniHour = 0
		self.countFullHour = 60
		self.countHour = 0
		self.countDay = 0
		self.countMonth = 0
		self.countMaxHour = 27
		self.countMaxDay = 31
		self.countMaxMonth = 12

		self.isPause = False
		self.isSpeedUp = False
		
	def run(self):
		print 'start time thread'
		while self.isRunning:
			#print 'time:',self.countMiniHour
			self.countMiniHour = 0
			if self.countHour >= self.countMaxHour:
				self.countHour = 0
				self.countDay += 1
				self.Signal_Day_Update.emit(self.countDay)
			self.Signal_Hour_Update.emit(self.countHour)
			if self.countDay >= self.countMaxDay:
				self.countDay = 0
				self.countMonth += 1
				self.Signal_Month_Update.emit(self.countMonth)
			print 't:',self.countHour,self.countDay,self.countMonth
			if self.isSpeedUp:
				self.countHour = self.countMaxHour
			else:
				self.countHour += 1
			time.sleep(1)
			while self.isPause:
				time.sleep(1)
	def setPause(self):
		self.isPause = not self.isPause

class WeatherControl():
	def __init__(self):
		random.seed(10000)
		self.windSpeed = -1
		self.windDirection = 'N' #N/S/E/W
		self.temperature = 0
		self.temperatureMin = 2
		self.temperatureMax = 20

	def changeWindSpeed(self):
		if random.random() < 0.5:
			self.windSpeed = random.randint(0,70)
		else:
			self.windSpeed = 0
	def changeWindDirection(self):
		num = random.randint(1,4)
		if num == 1:
			self.windDirection = 'N'
		if num == 2:
			self.windDirection = 'E'
		if num == 3:
			self.windDirection = 'S'
		if num == 4:
			self.windDirection = 'W'
	def changeTemperature(self):
		self.temperature = random.randint(self.temperatureMin,self.temperatureMax)
	def changeTemperatureMin(temp):
		self.temperatureMin = temp
	def changeTemperatureMax(temp):
		self.temperatureMax = temp