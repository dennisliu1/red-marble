#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class StartMenu(QWidget):
	def __init__(self, width,height, parent=None):
		super(StartMenu, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.resize(self.width,self.height)

		self.picSun = QImage('resources/RM_Start_Screen-01.png')
		self.picTitle = QImage('resources/RM_Start_Screen-02.png')
		self.picGround = QImage('resources/RM_Start_Screen-03.png')
		self.picSunFinalHeight = 122
		self.picTitleFinalHeight = 20
		self.picSunHeight = self.height
		self.picTitleHeight = 300
		#img_rect = QRect(0,0, self.img.width(),self.img.height())
		#qp.drawImage(event.rect(), self.img, img_rect)
		self.thread = StartMenu.StartThread(self)
		self.thread.Signal_Update.connect(self.moveTitle)
		self.thread.Signal_Flash_Update.connect(self.flashTitle)
		self.thread.start()
		self.flashColor = QColor(255,255,0)
	
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawStartMenu(event, qp)
		qp.end()

	def drawStartMenu(self, event, qp):
		qp.setPen(QColor(255,255,255))
		qp.setBrush(QColor(255,255,255))
		qp.drawRect(0,0, self.width-1,self.height-1)
		# qp.drawText(50,50, 'THIS IS THE START MENU')
		img_rect = QRect(0,0, self.picSun.width()-1,self.picSun.height()-1)
		qp.drawImage(QRect(620,self.picSunHeight,(self.picSun.width()-1)/2,(self.picSun.height()-1)/2), self.picSun, img_rect)
		img_rect = QRect(0,0, self.picGround.width()-1,self.picGround.height()-1)
		qp.drawImage(QRect(0,self.height*0.42,self.width/1,self.height*(1-0.3865)), self.picGround, img_rect)
		img_rect = QRect(0,0, self.picTitle.width()-1,self.picTitle.height()-1)
		qp.drawImage(QRect(105,self.picTitleHeight,(self.picTitle.width()-1)/2,(self.picTitle.height()-1)/2), self.picTitle, img_rect)

		if not (self.picSunHeight > self.picSunFinalHeight or self.picTitleHeight > self.picTitleFinalHeight):
			qp.setPen(self.flashColor)
			qp.setFont(QFont('Decorative',25, 75))
			qp.drawText(350,500, 'PRESS ANY BUTTON')
	
	def moveTitle(self):
		if self.picSunHeight > self.picSunFinalHeight:
			self.picSunHeight -= 1
		if self.picTitleHeight > self.picTitleFinalHeight:
			self.picTitleHeight -= 1
		#print 'move:',self.picSunHeight,self.picTitleHeight
		self.repaint()
		pass

	def flashTitle(self):
		if self.flashColor == QColor(255,255,0):
			self.flashColor = QColor(0,0,0)
		else:
			self.flashColor = QColor(255,255,0)
		self.repaint()

	class StartThread(QThread):
		Signal_Update = pyqtSignal()
		Signal_Flash_Update = pyqtSignal()
		def __init__(self, parent=None):
			super(StartMenu.StartThread, self).__init__()
			self.parent = parent
			self.isRunning = True
			self.flash_time = 0
			
		def run(self):
			#print 'start thread'
			while self.isRunning:
				#print 'loop'
				self.Signal_Update.emit()
				if self.flash_time >= 100:
					self.Signal_Flash_Update.emit()
					self.flash_time = 0
				time.sleep(0.01)
				self.flash_time += 1


