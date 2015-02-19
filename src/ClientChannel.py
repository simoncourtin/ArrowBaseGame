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
		
		# Orientation du sprite en fonction de la direction du personnage
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

		message = {"action":"move", "data":(self.neo.rect.center,self.neo.speed, self.neo.orientation)}
		self._server.SendMessageAll(message)
	#end Network_

#end ClientChannel