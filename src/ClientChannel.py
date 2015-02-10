#!/usr/bin/env python
# coding : utf-8

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import time,sys
import os
import pygame
from pygame.locals import *
import random

class ClientChannel(Channel):
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)
	#end __init__

	def Close(self):
		self._server.del_client(self)
	#end Close

	def Network_(self, data):
		
	#end Network_
#end ClientChannel