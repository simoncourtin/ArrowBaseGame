#!/usr/bin/env python
# coding : utf-8

from PodSixNet.Channel import Channel
import time, sys
import os
import pygame
from pygame.locals import *
import Personnage


class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.identifiant = 0
        self.personnage = Personnage.Personnage(1,0)
        self._server.joueur.add(self.personnage)
    # end __init__

    def Close(self):
        self._server.del_client(self)
        print 'Client parti'

    #end Close

    #def Network_(self, data):

    #end Network_

    def Network_move(self, data):
        mouvement = data['touche']
        if (mouvement == "bas"):
            self.personnage.down()
        elif (mouvement == "gauche"):
            self.personnage.left()
            self.personnage.orienter("gauche")
        elif (mouvement == "droite"):
            self.personnage.right()
            self.personnage.orienter("droite")
        elif (mouvement == "saut"):
            self.personnage.sauter()

        message = {"action": "move", "data": (self.personnage.rect.center, self.personnage.speed, self.personnage.orientation),"id":self.identifiant}
        self._server.SendMessageAll(message)
        #end Network_move

        #end ClientChannel