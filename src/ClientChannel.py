#!/usr/bin/env python
# coding : utf-8

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import time,sys
import os
import pygame
from pygame.locals import *
import random
from dns.rdatatype import NULL

class ClientChannel(Channel):
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)
		self.neo=Personnage.Personnage(1)
		self._server.team1.add(self.neo)
	#end __init__

	def Close(self):
		self._server.del_client(self)
	#end Close

	#def Network_(self, data):
		
	#end Network_
	
	def Network_move(self, data):
		mouvement=data['touche']
		if(mouvement == "bas"):
			self.neo.down()
        if(mouvement == "gauche"):  
            self.neo.left()
        if(mouvement == "droite"):  
            self.neo.right()
        if(mouvement == "saut"):  
            self.neo.sauter()
        
        self._server.sendMessageAll("move", "center", self.neo.rect.center)
	#end Network_

#end ClientChannel