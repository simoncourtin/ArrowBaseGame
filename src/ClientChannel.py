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
			self.neo.down()
		elif(mouvement == "gauche"):
			self.neo.left()
			self.neo.orienter("gauche")
		elif(mouvement == "droite"):
			self.neo.right()
			self.neo.orienter("droite")
		elif(mouvement == "saut"):
			self.neo.sauter()

		message = {"action":"move", "data":(self.neo.rect.center,self.neo.speed, self.neo.orientation)}
		self._server.SendMessageAll(message)
	#end Network_

#end ClientChannel