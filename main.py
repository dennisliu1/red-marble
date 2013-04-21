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

	def initUI(self):
		pass

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawRover(event, qp)
		qp.end()

	def drawRover(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setBrush(QColor(168, 100,100, 100))

def main():
	app = QApplication(sys.argv)	# application object for PyQT
	gui = RedMarbleMain(1000,600)
	gui.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()