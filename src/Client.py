#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pygame

from PodSixNet.Connection import connection, ConnectionListener
import Personnage
import load_png
from pygame.locals import *
import os

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768


class Client(ConnectionListener):
	def __init__(self, host, port):
		self.run = False  # Booléen déterminant si ce client est connecté au serveur ou non
		self.Connect((host, port))
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(1, 1)

		# Chargement du background de la map
		self.background_image, self.background_rect = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/background.png")

		# Instanciation des personnages et des groupes de sprites
		self.neo = Personnage.Personnage(1)
		self.darkVador = Personnage.Personnage(2)
		self.deadpool = Personnage.Personnage(3)
		self.vegeta = Personnage.Personnage(4)
		self.team1 = pygame.sprite.Group()
		self.team2 = pygame.sprite.Group()
		self.team1.add(self.vegeta)
		self.team1.add(self.darkVador)
		self.team1.add(self.deadpool)
		self.team1.add(self.neo)
	# end __init__

	def Loop(self):
		while True:
			self.neo.stopHorizontal()
			
			connection.Pump()
			self.Pump()
			self.clock.tick(60)  # max speed is 60 frames per second
	
			# Events handling
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return  # closing the window exits the program
				# end if
			# end for


			
			# Gestion des événements de ce client
			touches = pygame.key.get_pressed()
			if (touches[K_q]):
				sys.exit(0)
				# exit the program
			if (touches[K_DOWN]):
				connection.Send({"action": "move", "touche": "bas"})
			if (touches[K_LEFT]):
				connection.Send({"action": "move", "touche": "gauche", "orientation":"gauche"})
			if (touches[K_RIGHT]):
				connection.Send({"action": "move", "touche": "droite"})
			if (touches[K_SPACE]):
				connection.Send({"action": "move", "touche": "saut"})
		
			# updates
			self.team1.update()

			# drawings
			self.screen.blit(self.background_image, self.background_rect)
			self.team1.draw(self.screen)

			# screen refreshing
			pygame.display.flip()
		#end while
	#end Loop

	#def Network_(self, data):
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

	def Network_move(self, data):
		self.neo.rect.center = data['data'][0]
		self.neo.speed = data['data'][1]
		self.neo.orienter(data['data'][2])

	 #end Network_move

# end Client

if __name__ == '__main__':
	client = Client(sys.argv[1], int(sys.argv[2]))
   
	client.Loop()
	
	sys.exit(0)