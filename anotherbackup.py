#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import socket
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class RedMarbleMain(QMainWindow):
	def __init__(self, width,height):
		super(RedMarbleMain, self).__init__()
		self.setWindowTitle('Red Marble')
		self.width = width
		self.height = height
		self.resize(self.width,self.height)
		self.initUI()

		self.rover_X = 0;
		self.rover_Y = 0;
		self.mapSize = 90;
		self.mapTileDimensions = 64;
		self.mapMatrix = [[0 for x in xrange(self.mapSize)] for x in xrange(self.mapSize )] 

	def initUI(self):
		self.setWindowTitle('Red Marble')
		

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawMapFromMatrix(event, qp)		#draws the map from the mapMatrix
		self.drawRover(event,qp, self.rover_X, self.rover_Y)
		qp.end()

	def fillMapMatix(self):
															#converts the map.txt file into a matrix of numbers portraying different depth and structures.
		lineCount = 0; 								#known number of lines in the map file.
		with open('map.txt', 'rU') as f:			#opens the map.txt file
			for line in f:								#for every line in map.txt
				for i in range(0,len(line)): 		
					tile_select = str(line[i])
					self.mapMatrix[i][lineCount] = tile_select				
				if '\n' in line:
					lineCount += 1

	def drawMapFromMatrix(self, event, qp):
															#takes the mapMatrix and draw it. 
		self.fillMapMatix() 							#fill dat map
		horizontal_count = 0; 						#origin x position
		vertical_count = 0;							#origin y position
		for i in range(0, self.mapSize):
			for j in range(0, self.mapSize):
				qp.drawImage(horizontal_count, vertical_count, QImage(self.tileCases(self.mapMatrix[j][i])))
				horizontal_count += self.mapTileDimensions
			horizontal_count = 0
			vertical_count += self.mapTileDimensions

	def tileCases(self, tile):
		if 'x' == tile:
			return "marstile_5.png";
		elif 'y' == tile:
			return "marstile_4.png";
		else:
			return "marstile_3.png"

	def drawRover(self, event, qp, X, Y):
		qp.drawImage(self.rover_X*64, self.rover_Y*64, QImage('rover1_forward.png'))

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Down:
			self.rover_Y +=1;
			self.repaint()
		elif e.key() == Qt.Key_Up:
			self.rover_Y -=1;
			self.repaint()
		elif e.key() == Qt.Key_Right:
			self.rover_X +=1;
			self.repaint()
		elif e.key() == Qt.Key_Left:
			self.rover_X -=1;
			self.repaint()

	def drawTiles(self, event, qp):
															#OBSOLETE BUT LEFT FOR LEGACY SUPPORT!
															#draws the file without making it into a matrix first
		horizontal_count = 0; 						#origin x position
		vertical_count = 0;							#origin y position
		horizontal_offset = 0;
		with open('map.txt', 'rU') as f:
			for line in f:
				for i in range(0,len(line)): 
					tile_select = str(line[i])
					if (tile_select == 'x'):
						qp.drawImage(horizontal_count, vertical_count, QImage('marstile_1.png'))
			
						horizontal_count += self.mapTileDimensions
				if '\n' in line:
					horizontal_count = 0
					vertical_count += self.mapTileDimensions







def main():
	app = QApplication(sys.argv)	# application object for PyQT
	gui = RedMarbleMain(1000,600)
	gui.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()