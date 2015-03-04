#!/usr/bin/env python
# coding : utf-8

from PodSixNet.Channel import Channel
import time, sys
import os
import pygame
from pygame.locals import *

import Personnage
from posix import wait
import Tir

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.identifiant = 0
        self.personnage = Personnage.Personnage(1,self.identifiant)
        self._server.joueurs.add(self.personnage)
    # end __init__


    def sendMove(self):
        message = {"action":"move", "data":(self.personnage.rect.center,self.personnage.speed, self.personnage.orientation, self.personnage.isAttacking),'id':self.identifiant}
        print message
        self._server.SendMessageAll(message)
    #end sendMove

    def sendTir(self):
        print "Tir sent (depuis sendTir)"
        message = {"action":"tir", "data":(self.personnage.rect.center, self.personnage.orientation)}
        self._server.SendMessageAll(message)
    #end sendTir



    def Close(self):
        self._server.del_client(self)
        print 'Client parti'
    #end Close

    #def Network_(self, data):

    #end Network_


    def Network_move(self, data):
        mouvement=data['touche']
        if(mouvement == "bas"):
            if self.personnage.orientation == "droite" or self.personnage.orientation == "gauche":
                self.personnage.orienter("bas")
            #end if

            self.personnage.down()
        elif(mouvement == "haut"):
            if self.personnage.orientation == "bas":
                self.personnage.orienter("haut")
            #end if

            self.personnage.sauter()
        elif(mouvement == "gauche"):
            if self.personnage.orientation == "droite" or self.personnage.orientation == "bas" :
                self.personnage.orienter("gauche")
            self.personnage.left()
        elif(mouvement == "droite"):
            if self.personnage.orientation == "gauche" or self.personnage.orientation == "bas":
                self.personnage.orienter("droite")
            self.personnage.right()
        elif(mouvement == "saut"):
            self.personnage.sauter()
        elif(mouvement=="a"):
        	self.personnage.attaquer()

        self.sendMove()



    def Network_tir(self, data):
        print "Network tir (depuis Network_tir)"
        self.sendTir()

#end ClientChannel
