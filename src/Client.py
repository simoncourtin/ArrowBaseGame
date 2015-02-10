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
from cPickle import load
from src import Personnage
from src import Animable
from src import load_png

class Client(ConnectionListener):
	def __init__(self, host, port):
		self.run = False # Booléen déterminant si ce client est connecté au serveur ou non
		self.Connect((host, port))
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(1,1)
		
		# Chargement du background de la map
		self.background_image, self.background_rect = load_png.load_png('data/sprite/background.png')
		
		#Instanciation des personnages et des groupes de sprites
		self.neo=Personnage.Personnage(1)
		self.darkVador=Personnage.Personnage(2)
		self.deadpool=Personnage.Personnage(3)
		self.vegeta=Personnage.Personnage(4)
		self.team1 = pygame.sprite.Group()
		self.team2 = pygame.sprite.Group()
		self.team1.add(vegeta)
		self.team1.add(darkVador)
		self.team1.add(deadpool)
		self.team1.add(neo)


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

		if(touches[K_q]):
			return # exit the program    
        if(touches[K_DOWN]):  
           connection.Send({"action":"move", "touche":"bas"})
        if(touches[K_LEFT]):  
           connection.Send({"action":"move", "touche":"gauche"}) 
        if(touches[K_RIGHT]):  
            connection.Send({"action":"move", "touche":"droite"})
        if(touches[K_SPACE]):
            connection.Send({"action":"move", "touche":"saut"})
        
        #if not touches[K_LEFT] and not touches[K_RIGHT]:
	   	
	   	# updates
	   	self.team1.update()
		screen.blit(background_image, background_rect)
		# drawings
		team1.draw(screen)
		# screen refreshing
		pygame.display.flip()
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
		self.neo.rect.center = data['center']
	#end Network_move
#end Client
        
if __name__ == '__main__':
    client = Client()
	while True:
    	client.Loop()
    sys.exit(0)