#!/usr/bin/env python
# coding : utf-8

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import time,sys
import os
import pygame
from pygame.locals import *
import random

class Serveur(Server):
	channelClass = ClientChannel

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.clients = []
		print('Server launched')
		self.clock = pygame.time.Clock()
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
		
		# Collisions

	#end Loop
#end MyServer