#!/usr/bin/env python
# coding : utf-8

from PodSixNet.Channel import Channel
import time,sys
import os
import pygame
from pygame.locals import *
import Personnage

class ClientChannel(Channel):
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)
		self.neo=Personnage.Personnage(1)
		self._server.team1.add(self.neo)
	#end __init__

	def Close(self):
		self._server.del_client(self)
		print 'Client parti'
	#end Close

	#def Network_(self, data):
		
	#end Network_
	
	def Network_move(self, data):
		mouvement=data['touche']
		if(mouvement == "bas"):
			if self.neo.orientation == "droite" or self.neo.orientation == "gauche":
				self.neo.orienter("bas")
			self.neo.down()
		elif(mouvement == "haut"):
			if self.neo.orientation == "bas":
				self.neo.orienter("haut")
		elif(mouvement == "gauche"):
			if self.neo.orientation == "droite":
				self.neo.orienter("gauche")
			self.neo.left()
		elif(mouvement == "droite"):
			if self.neo.orientation == "gauche":
				self.neo.orienter("droite")
			self.neo.right()
		elif(mouvement == "saut"):
			self.neo.sauter()
		
		self._server.SendMessageAll("move", "data", (self.neo.rect.center,self.neo.speed, self.neo.orientation))
	#end Network_

#end ClientChannel