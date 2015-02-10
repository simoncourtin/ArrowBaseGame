#!/usr/bin/env python
# coding : utf-8

from PodSixNet.Channel import Channel
import ClientChannel
from PodSixNet.Server import Server
import time,sys
import os
import pygame
from pygame.locals import *
import random
import Personnage

class Serveur(Server):
	channelClass = ClientChannel

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.clients = []
		print('Server launched')
		self.clock = pygame.time.Clock()
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(1,1)

		#Instanciation des personnages
		self.darkVador=Personnage.Personnage(2)
		self.deadpool=Personnage.Personnage(3)
		self.vegeta=Personnage.Personnage(4)
		self.team1 = pygame.sprite.Group()
		self.team2 = pygame.sprite.Group()
		self.team1.add(self.vegeta)
		self.team1.add(self.darkVador)
		self.team1.add(self.deadpool)
		self.team1.add(self.neo)
		#end __init__

	def Connected(self, channel, addr):
		print('New connection')
		self.clients.append(channel)
	#end Connected

	def del_client(self,channel):
		print('client deconnecte')
		self.clients.remove(channel)
	#end del_client

	def SendMessageAll(self, action, key, value):
		for c in self.clients:
			c.Send({"action":action, key:value})
		#end for
	#end SendMessageAll

	def Loop(self):
		# Stuff
		self.Pump()
		self.clock.tick(60) # max speed is 60 frames per second
		self.compteur += 1

		# Events



		# Updates
		self.team1.update()
		self.team2.update()

		# Collisions

	#end Loop

if __name__ == '__main__':
    server = Server()

    while True:
    	server.Loop()
    sys.exit(0)
#end MyServer