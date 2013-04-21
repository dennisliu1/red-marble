#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class GameModel():
	def __init__(self):
		self.buildingList = []
		self.roverModel = RoverModel(0,0)

class RoverModel():
	def __init__(self, x,y):
		self.location = [x,y]
		self.direction = 'N'
		self.hp = 10
		self.energy = 100
	def moveUp(self):
		self.location[1] += 1
	def moveDown(self):
		self.location[1] -= 1
	def moveRight(self):
		self.location[0] += 1
	def moveLeft(self):
		self.location[0] -= 1

class BuildingAbstract():
	def __init__(self, x,y):
		self.location = [x,y]
		self.direction = ''
		self.hp = -1
		self.energy = -1

class BuildingHabitat(BuildingAbstract):
	def __init__(self):
		super(BuildingHabitat, self).__init__()

class BuildingSolarPanel(BuildingAbstract):
	def __init__(self):
		super(BuildingSolarPanel, self).__init__()

class BuildingWindmill(BuildingAbstract):
	def __init__(self):
		super(BuildingWindmill, self).__init__()

class BuildingResearchCenter(BuildingAbstract):
	def __init__(self):
		super(BuildingResearchCenter, self).__init__()

