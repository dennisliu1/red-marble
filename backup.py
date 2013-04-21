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

		
		# self.rover_orientation = "forward"
		# self.collidable = ["y", "s", "w", "r"]
		# self.file_directory = "resources/"
		# self.y_off = 0;
		# self.left_bound = 0;
		# self.bottom_bound = 0;
		# self.isPinned = False;
		# self.x_off = 0;
		# self.rover_X = 5;
		# self.rover_Y = 5;
		# self.mapSize = 60;
		# self.mapRenderSize = 20;
		# self.mapTileDimensions = 64;
		# self.mapMatrix = [[0 for x in xrange(self.mapSize)] for x in xrange(self.mapSize )] 
		# self.fillMapMatrix()
	def initUI(self):
		self.setWindowTitle('Red Marble')

		
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawMapFromMatrix(event, qp)		#draws the map from the mapMatrix
		self.drawRover(event,qp, self.rover_X, self.rover_Y)
		qp.end()

	def fillMapMatrix(self):
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
		horizontal_count = 0; 						#origin x position
		vertical_count = 0;							#origin y position

		#prevent index out of bounds exception for drawing rightmost side. 
		self.left_bound = self.mapRenderSize + self.x_off
		if (self.left_bound) >= self.mapSize:
			self.left_bound = self.mapSize;

		#prevent index from going out of bound for bottom. 
		self.bottom_bound = self.mapRenderSize + self.y_off
		if (self.bottom_bound) >= self.mapSize:
			self.bottom_bound = self.mapSize;

		for i in range(abs(self.y_off), self.bottom_bound):
			for j in range(abs(self.x_off), self.left_bound):
				qp.drawImage(horizontal_count, vertical_count, QImage(self.tileCases(self.mapMatrix[j][i])))
				horizontal_count += self.mapTileDimensions
			horizontal_count = 0
			vertical_count += self.mapTileDimensions

	def tileCases(self, tile):
		if 'x' == tile:
			return self.file_directory + "Ground1.png";
		elif 'y' == tile:
			return self.file_directory + "Block1.png";
		elif 'd' == tile:
			return self.file_directory + "Ground2.png";
		elif 'h' == tile:
			return self.file_directory + "Habitat1.png";
		elif 'w' == tile:
			return self.file_directory + "Wind1.png";
		elif 's' == tile:
			return self.file_directory + "Solar1.png";
		elif 'r' == tile:
			return self.file_directory + "Research1.png";
		else:
			return self.file_directory + "Ground2.png";

	def drawRover(self, event, qp, X, Y):
		qp.drawImage(self.rover_X*64, self.rover_Y*64, QImage(self.file_directory+'rover1_'+self.rover_orientation+'.png'))

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Down:
			# self.rover_orientation = "down"
			# if (self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off + 1] in self.collidable):
			# 	pass;
			# else:
			# 	if (self.y_off + 7) >= self.mapSize :
			# 		pass;
			# 	else:
			# 		if self.rover_Y <= 5:
			# 			self.rover_Y += 1;
			# 		else:
			# 			self.y_off += 1
			# #self.rover_Y +=1;
			# self.repaint()
		elif e.key() == Qt.Key_Up:
			# self.rover_orientation = "forward"
			# #collision detection
			# if (self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off - 1] in self.collidable):
			# 	pass;
			# else:
			# 	if self.rover_Y <= 0:
			# 		self.rover_Y = 1;
			# 	else:
			# 		if self.y_off > 0 and self.rover_Y == 1:
			# 			self.y_off -= 1;
			# 			self.rover_Y = 2;
			# 	self.rover_Y -=1;
			# self.repaint()
		elif e.key() == Qt.Key_Right:
			# self.rover_orientation = "right"
			# if (self.mapMatrix[self.rover_X + self.x_off + 1][self.rover_Y + self.y_off] in self.collidable):
			# 	pass;
			# else:
			# 	if (self.x_off + self.rover_X + 1) >= self.mapSize :
			# 		pass;
			# 	else:
			# 		if self.rover_X <= 10:
			# 			self.rover_X += 1;
			# 		else:
			# 			self.x_off += 1
			# self.repaint()

		elif e.key() == Qt.Key_Left:
			# self.rover_orientation = "left"
			# if (self.mapMatrix[self.rover_X + self.x_off - 1][self.rover_Y + self.y_off] in self.collidable):
			# 	pass;
			# else:
			# 	if self.rover_X >= 3:
			# 		self.rover_X -=1;
			# 	else:
			# 		self.x_off -= 1;
			# 		if self.x_off <= 0:
			# 			if self.rover_X == 2:
			# 				self.rover_X = 1;
			# 			elif self.rover_X == 1:
			# 				self.rover_X = 0;
			# 			self.x_off	= 0;
			# self.repaint()

		############## BUILDING KEY PRESSES ############
		elif e.key() == Qt.Key_1:  #habitat
			print "Habitat was planted!"
			self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] = 'h';
			self.repaint()
		elif e.key() == Qt.Key_2:
			print "Solar panel was planted!"
			self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] = 's';
			self.repaint()
		elif e.key() == Qt.Key_3:
			print "Wind mill was planted!"
			self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] = 'w';
			self.repaint()			
		elif e.key() == Qt.Key_4:
			print "Research center mill was planted!"
			self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] = 'r';
			self.repaint()		

		######## DEBUGGING #############
		print "ROVER CO-ORDS: (", self.rover_X, ", ", self.rover_Y, ")" ;
		print "OFFSET CO-ORDS: (", self.x_off, ", ",  self.y_off, ")";

def main():
	app = QApplication(sys.argv)	# application object for PyQT
	gui = RedMarbleMain(1000,600)
	gui.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()