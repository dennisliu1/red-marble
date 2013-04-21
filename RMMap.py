#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MapDisplay(QWidget):
	def __init__(self, width,height, parent):
		super(MapDisplay, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.resize(self.width,self.height)
		self.initMap()
		self.isFlipped = False
	
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawMap(event, qp)
		qp.end()

	def drawMap(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setBrush(QColor(168, 100,100, 100))
		qp.drawRect(0,0, self.width-1,self.height-1)

		qp.setPen(QColor(168, 34, 3))
		qp.setFont(QFont('Times',20,75))
		qp.drawText(50,50, 'DRAW MAP')

	def initMap(self):
		self.known_mining_areas = [[6,2,10], [9,8,8], [20,10,8], [30,18,8], [12,24,20], [15, 32, 15], [16, 32, 15], [15, 33, 15], [10, 10, 15], [12, 10, 15], [12, 17, 15], [1, 12, 18], [30, 12, 18], [22, 12, 18]];
		self.solar_locations = [];
		self.research_locations = [];
		self.wind_locations = [];
		self.mineral_count = 6000;
		self.power_count = 100;
		self.public_interest = 0;
		self.habitat_locations = [];
		self.rover_orientation = "forward"
		self.collidable = ["y", "s", "w", "r", "h"]
		self.file_directory = "resources/"
		self.y_off = 0;
		self.left_bound = 0;
		self.bottom_bound = 0;
		self.isPinned = False;
		self.x_off = 0;
		self.rover_X = 5;
		self.rover_Y = 5;
		self.mapSize = 60;
		self.mapRenderSize = 20;
		self.mapTileDimensions = 64;
		self.mapMatrix = [[0 for x in xrange(self.mapSize)] for x in xrange(self.mapSize )] 
		self.fillMapMatrix()
		self.repaint()
		

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

	def decrease_building(self):
		for t in self.solar_locations:
			t[2] -= 3;

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
				for t in self.known_mining_areas:
					self.mapMatrix[t[0]][t[1]] = "m"
			horizontal_count = 0
			vertical_count += self.mapTileDimensions

		for t in self.solar_locations:
			qp.setPen(QColor(255,255,255))
			qp.setBrush(QColor(100,100,100))
			qp.setFont(QFont('Times',13,75))
			if self.mapMatrix[t[0]][t[1]] != 'g':
				qp.drawText((t[0]-self.x_off)*64,(t[1]-self.y_off)*64,(str(t[2])+"%"))

		for t in self.wind_locations:
			qp.setPen(QColor(255,255,255))
			qp.setBrush(QColor(100,100,100))
			qp.setFont(QFont('Times',13,75))
			if self.mapMatrix[t[0]][t[1]] != 'g':
				qp.drawText((t[0]-self.x_off)*64,(t[1]-self.y_off)*64,(str(t[2])+"%"))

		for t in self.research_locations:
			qp.setPen(QColor(255,255,255))
			qp.setBrush(QColor(100,100,100))
			qp.setFont(QFont('Times',13,75))
			if self.mapMatrix[t[0]][t[1]] != 'g':
				qp.drawText((t[0]-self.x_off)*64,(t[1]-self.y_off)*64,(str(t[2])+"%"))

###########################################################
		for t in self.habitat_locations:
			qp.setPen(QColor(255,255,255))
			qp.setBrush(QColor(100,100,100))
			qp.setFont(QFont('Times',13,75))
			if self.mapMatrix[t[0]][t[1]] != 'g':
				qp.drawText((t[0]-self.x_off)*64,(t[1]-self.y_off)*64,(str(t[2])+"%"))
############################################################
	def tileCases(self, tile):
		if 'x' == tile:
			return self.file_directory + "Ground1.png";
		elif 'y' == tile:
			return self.file_directory + "Block1.png";
		elif 'd' == tile:
			return self.file_directory + "Ground2.png";
		elif 'h' == tile:
			if not self.isFlipped:
				return self.file_directory + "Habitat1.png";
			else:
				return self.file_directory + "Habitat2.png";
		elif 'w' == tile:
			if not self.isFlipped:
				return self.file_directory + "Wind1.png";
			else:
				return self.file_directory + "Wind2.png";
		elif 's' == tile:
			if not self.isFlipped:
				return self.file_directory + "Solar1.png";
			else:
				return self.file_directory + "Solar2.png";
		elif 'r' == tile:
			if not self.isFlipped:
				return self.file_directory + "Research1.png";
			else:
				return self.file_directory + "Research2.png";
		elif 'm' == tile:
			return self.file_directory + "Mineral.png";
		elif 'g' == tile:
			return self.file_directory + "Wreck.png";
		else:
			return self.file_directory + "Ground2.png";

	def drawRover(self, event, qp, X, Y):
		qp.drawImage(self.rover_X*64, self.rover_Y*64, QImage(self.file_directory+'rover_'+self.rover_orientation+'.png'))

	def moveDown(self):
		self.rover_orientation = "down"
		if (self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off + 1] in self.collidable):
			self.check_repair((self.rover_X + self.x_off), (self.y_off + self.rover_Y + 1))
			pass;
		else:
			if (self.y_off + 7) >= self.mapSize :
				pass;
			else:
				if self.rover_Y <= 5:
					self.rover_Y += 1;
				else:
					self.y_off += 1
		#self.rover_Y +=1;
		self.repaint()
		print "ROVER CO-ORDS: (", self.rover_X, ", ", self.rover_Y, ")" ;
		print "OFFSET CO-ORDS: (", self.x_off, ", ",  self.y_off, ")";

	def moveUp(self):
		self.rover_orientation = "forward"
		#collision detection
		if (self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off - 1] in self.collidable):
			self.check_repair((self.rover_X + self.x_off), (self.y_off + self.rover_Y - 1))
			pass;
		else:
			if self.rover_Y <= 0:
				self.rover_Y = 1;
			else:
				if self.y_off > 0 and self.rover_Y == 1:
					self.y_off -= 1;
					self.rover_Y = 2;
			self.rover_Y -=1;
		self.repaint()
		print "ROVER CO-ORDS: (", self.rover_X, ", ", self.rover_Y, ")" ;
		print "OFFSET CO-ORDS: (", self.x_off, ", ",  self.y_off, ")";


	def moveRight(self):
		self.rover_orientation = "right"
		if (self.mapMatrix[self.rover_X + self.x_off + 1][self.rover_Y + self.y_off] in self.collidable):
			self.check_repair((self.rover_X + self.x_off + 1), (self.y_off + self.rover_Y))
			pass;
		else:
			if (self.x_off + self.rover_X + 1) >= self.mapSize :
				pass;
			else:
				if self.rover_X <= 10:
					self.rover_X += 1;
				else:
					self.x_off += 1
		self.repaint()
		print "ROVER CO-ORDS: (", self.rover_X, ", ", self.rover_Y, ")" ;
		print "OFFSET CO-ORDS: (", self.x_off, ", ",  self.y_off, ")";


	def moveLeft(self):
		self.rover_orientation = "left"
		if (self.mapMatrix[self.rover_X + self.x_off - 1][self.rover_Y + self.y_off] in self.collidable):
			self.check_repair((self.rover_X + self.x_off - 1), (self.y_off + self.rover_Y))
			pass;
		else:
			if self.rover_X >= 3:
				self.rover_X -=1;
			else:
				self.x_off -= 1;
				if self.x_off <= 0:
					if self.rover_X == 2:
						self.rover_X = 1;
					elif self.rover_X == 1:
						self.rover_X = 0;
					self.x_off	= 0;
			self.repaint()
		print "ROVER CO-ORDS: (", self.rover_X, ", ", self.rover_Y, ")" ;
		print "OFFSET CO-ORDS: (", self.x_off, ", ",  self.y_off, ")";


	def check_repair(self, X, Y):
		print X, " ", Y
		for t in self.solar_locations:
			if (t[0] == X and t[1] == Y and t[2] < 100):
				t[2] += 10;
				self.mineral_count -= 5;
				print self.mineral_count;
				if (t[2] > 100):
					t[2] = 100
		for t in self.research_locations:
			if (t[0] == X and t[1] == Y and t[2] < 100):
				t[2] += 10;
				self.mineral_count -= 5;
				print self.mineral_count;
				if (t[2] > 100):
					t[2] = 100
		for t in self.wind_locations:
			if (t[0] == X and t[1] == Y and t[2] < 100):
				t[2] += 10;
				self.mineral_count -= 5;
				print self.mineral_count;
				if (t[2] > 100):
					t[2] = 100
		for t in self.habitat_locations:
			if (t[0] == X and t[1] == Y and t[2] < 100):
				t[2] += 10;
				self.mineral_count -= 5;
				print self.mineral_count;
				if (t[2] > 100):
					t[2] = 100
		self.parent.metalWidget.setMetal(self.mineral_count)
		self.parent.metalWidget.repaint()
		self.repaint();

	def power_down(self):
		self.power_count -= 10

	def power_up(self):
		self.power_count += 10

	def decrease_building(self):
		for t in self.solar_locations:
			t[2] -= 3;
			if (t[2] < 0):
				self.mapMatrix[t[0]][t[1]] = "g"
				self.solar_locations.remove(t)
		for t in self.research_locations:
			t[2] -= 3;
			if (t[2] < 0):
				self.mapMatrix[t[0]][t[1]] = "g"
				self.research_locations.remove(t)
		for t in self.wind_locations:
			t[2] -= 3;
			if (t[2] < 0):
				self.mapMatrix[t[0]][t[1]] = "g"
				self.wind_locations.remove(t)
		for t in self.habitat_locations:
			t[2] -= 3;
			if (t[2] < 0):
				self.mapMatrix[t[0]][t[1]] = "g"
				self.habitat_locations.remove(t)
		self.repaint()
	def createHabitat(self):
		print "Habitat was planted!"
		self.mineral_count -= 200
		self.public_interest += 1;
		self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] = 'h';
		self.habitat_locations.append([self.rover_X + self.x_off, self.rover_Y + self.y_off, 100])
		self.repaint()
	def createSolarPanel(self):
		print "Solar panel was planted!"
		self.mineral_count -= 200
		self.public_interest += 1;
		self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] = 's';
		self.solar_locations.append([self.rover_X + self.x_off, self.rover_Y + self.y_off, 100])
		print self.solar_locations
		self.repaint()
	def createWindMill(self):
		print "Wind mill was planted!"
		self.mineral_count -= 200
		self.public_interest += 1;
		self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] = 'w';
		self.wind_locations.append([self.rover_X + self.x_off, self.rover_Y + self.y_off, 100])
		self.repaint()
	def createResearchCenter(self):
		print "Research center was planted!"
		self.mineral_count -= 200
		self.public_interest += 1;
		self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] = 'r';
		self.research_locations.append([self.rover_X + self.x_off, self.rover_Y + self.y_off, 100])
		self.repaint()
	def mine(self):
		print "Mining"
		if self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] == 'm':
			print "Mining! current minerals: ", self.mineral_count
			for tup in self.known_mining_areas:
				print tup
				if tup[0] == (self.rover_X + self.x_off) and tup[1] == (self.rover_Y + self.y_off):
					currentminerals = tup[2];
					currentminerals -= 1;
					tup[2] = currentminerals;

					if currentminerals <= 0:
						self.mapMatrix[self.rover_X + self.x_off][self.rover_Y + self.y_off] = 'x'
						self.known_mining_areas.remove(tup)
						self.repaint()

					self.mineral_count += 5
					print currentminerals
			self.repaint()
		else:
			print "nothing to mine here!"	

