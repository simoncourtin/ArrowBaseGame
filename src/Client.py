#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import os
from PodSixNet.Connection import connection, ConnectionListener
import thread
import pygame
from pygame.locals import *
import random

class Client(ConnectionListener):
	def __init__(self, host, port):
		self.run = False # Booléen déterminant si ce client est connecté au serveur ou non
		self.Connect((host, port))
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(1,1)

		# Objects creation
		# TODO
	#end __init__

	def Loop(self):
		connection.Pump()
		self.Pump()
		self.clock.tick(60) # max speed is 60 frames per second

		# Events handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit() # closing the window exits the program
			#end if
		#end for
		touches=pygame.key.get_pressed()

		# updates

		# drawings
		
		# screen refreshing
		pygame.display.flip()
	#end Loop

	def Network_(self, data):
		# Blabla
	#end Network_
	
	### Network event/message callbacks ###
	def Network_connected(self, data):
		self.run = True
		print('Connexion au serveur !')
	#end Network_connected

	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
		sys.exit()
	#end Network_error
		
	def Network_disconnected(self, data):
		print 'Server disconnected'
		sys.exit()
	#end Network_disconnected
#end Client