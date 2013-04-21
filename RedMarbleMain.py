#!/usr/bin/python
# -*- coding: utf-8 -*-
# temperatue -90 to 20 celcius

import sys
import socket
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from RMUnitInfo import *
from RMMap import *
from RMHUD import *
from RMStartMenu import *
from RMGameMechanics import *

class RedMarbleMain(QMainWindow):
	def __init__(self, width,height):
		super(RedMarbleMain, self).__init__()
		self.setWindowTitle('Red Marble')
		self.width = width
		self.height = height
		self.resize(self.width,self.height)
		self.initUI()

	def initUI(self):
		self.isInGame = False
		self.startMenu = StartMenu(self.width,self.height, self)


		self.rover = RoverModel(0,0)
		self.mapDisplay = MapDisplay(self.width,self.height, self)
		self.hpWidget = RoverHPBar(100,30, self)
		self.hpWidget.move(self.width-100,0)
		self.energyWidget = BaseEnergyBar(100,30,self)
		self.energyWidget.move(self.width-100,30)
		self.metalWidget = BaseMetalBar(100,30,self)
		self.metalWidget.move(self.width-100,60)
		self.weatherWidget = BaseWeatherWidget(100,60,self)
		self.weatherWidget.move(self.width-100,90)
		self.piWidget = RoverPIBar(100,30,self)
		self.piWidget.move(self.width-100,90+60)
		self.timeWidget = BaseTimeBar(100,30,self)
		self.timeWidget.move(self.width-100,90+60+30)
		self.windWidgets = []
		for iter in range(10):
			self.windWidgets.append(ShowWindWidget(300,30,self))
			self.windWidgets[iter].hide()
		self.mapDisplay.hide()
		self.hpWidget.hide()
		self.energyWidget.hide()
		self.metalWidget.hide()
		self.weatherWidget.hide()
		self.piWidget.hide()
		self.timeWidget.hide()

		self.weatherControl = WeatherControl()
		self.timeThread = TimeThread(self)
		self.timeThread.Signal_Hour_Update.connect(self.updateHour)
		self.timeThread.Signal_Day_Update.connect(self.updateDay)
		self.timeThread.Signal_Month_Update.connect(self.updateMonth)
		pass

	def showGame(self):
		self.mapDisplay.show()
		self.hpWidget.show()
		self.energyWidget.show()
		self.metalWidget.show()
		self.weatherWidget.show()
		self.piWidget.show()
		self.timeWidget.show()
		self.timeThread.start()

	def keyPressEvent(self, e):
		if self.isInGame == False:
			self.startMenu.hide()
			self.startMenu.thread.isRunning = False
			self.showGame()
			self.isInGame = True
		else:
			if e.key() == Qt.Key_X: # pause game
				self.timeThread.setPause()
			elif e.key() == Qt.Key_Down:
				self.mapDisplay.moveDown()
			elif e.key() == Qt.Key_Up:
				self.mapDisplay.moveUp()
			elif e.key() == Qt.Key_Right:
				self.mapDisplay.moveRight()
			elif e.key() == Qt.Key_Left:
				self.mapDisplay.moveLeft()
			############## BUILDING KEY PRESSES ############
			elif e.key() == Qt.Key_1:  #habitat
				self.mapDisplay.createHabitat()
				self.metalWidget.setMetal(self.mapDisplay.mineral_count)
				self.metalWidget.repaint()
			elif e.key() == Qt.Key_2:
				self.mapDisplay.createSolarPanel()
				self.metalWidget.setMetal(self.mapDisplay.mineral_count)
				self.metalWidget.repaint()
			elif e.key() == Qt.Key_3:
				self.mapDisplay.createWindMill()
				self.metalWidget.setMetal(self.mapDisplay.mineral_count)
				self.metalWidget.repaint()
			elif e.key() == Qt.Key_4:
				self.mapDisplay.createResearchCenter()
				self.metalWidget.setMetal(self.mapDisplay.mineral_count)
				self.metalWidget.repaint()
			elif e.key() == Qt.Key_D:
				self.mapDisplay.decrease_building()
			elif e.key() == Qt.Key_M:
				self.mapDisplay.mine()
				self.metalWidget.setMetal(self.mapDisplay.mineral_count)
				self.metalWidget.repaint()
			elif e.key() == Qt.Key_L:
				self.mapDisplay.power_down()
				self.energyWidget.setEnergy(self.mapDisplay.power_count)
				self.energyWidget.repaint()
			elif e.key() == Qt.Key_K:
				self.mapDisplay.power_up()
				self.energyWidget.setEnergy(self.mapDisplay.power_count)
				self.energyWidget.repaint()
	def updateHour(self):
		self.weatherControl.changeTemperature()
		self.weatherWidget.changeTemperature(self.weatherControl.temperature)
		self.weatherWidget.repaint()

		number = self.weatherControl.windSpeed/10
		for iter in range(int(number)):
			x = random.randint(0,10)*64
			y = random.randint(0,5)*64
			self.windWidgets[iter].show()
			self.windWidgets[iter].move(x,y)
			self.windWidgets[iter].createWind()

		self.timeWidget.setHour(self.timeThread.countHour)
		print 'update hour'
		pass
	def updateDay(self):
		self.weatherControl.changeWindDirection()
		self.weatherControl.changeWindSpeed()
		self.weatherWidget.changeWindDirection(self.weatherControl.windDirection)
		self.weatherWidget.changeWindSpeed(self.weatherControl.windSpeed)
		self.weatherWidget.repaint()
		self.timeWidget.setDay(self.timeThread.countDay)
		print 'update day'
		pass
	def updateMonth(self):
		print 'update month'
		self.timeWidget.setMonth(self.timeThread.countMonth)
		pass

	# def mouseDoubleClickEvent(self, event):
	# 	print 'double click',event.x(),' ',event.y()
	# 	pass
	# def mouseMoveEvent(self, event):
	# 	print 'move ',event.x(),' ',event.y()
	# 	pass
	# def mousePressEvent(self, event):
	# 	print 'press',event.x(),' ',event.y()
	# 	if event.button() == Qt.LeftButton:
	# 		pass
	# def mouseReleaseEvent(self, event):
	# 	print 'release ',event.x(),' ',event.y()
	# 	if event.button() == Qt.LeftButton:
	# 		pass
	# 	if event.button() == Qt.RightButton:
	# 		pass

def main():
	app = QApplication(sys.argv)	# application object for PyQT
	gui = RedMarbleMain(1000,600)
	gui.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()