#!/usr/bin/env python
# coding : utf-8

from PodSixNet.Channel import Channel
import time, sys
import os
import pygame
from pygame.locals import *
import Tir
import Personnage
#from posix import wait
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
        #print message
        self._server.SendMessageAll(message)
    #end sendMove
    def set_identifiant(self,id):
        self.identifiant = id
        self.personnage.idJoueur = id
    def sendTir(self,id, puissance):
        message = {"action":"tirs", "data":(self.personnage.rect.center, self.personnage.orientation,id, puissance)}
        self._server.SendMessageAll(message)
    #end sendTir


    def Close(self):
        self._server.del_client(self)
        print 'Client parti'
    #end Close



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

        self.sendMove()

    def Network_tir(self, data):
        id_tir= len(self._server.tirs)
        if self.personnage.orientation=="gauche":
            xtir= self.personnage.rect.left
        elif self.personnage.orientation =="droite":
            xtir = self.personnage.rect.right
        self._server.tirs.add(Tir.Tir(self.identifiant,id_tir,[xtir,self.personnage.rect.centery],self.personnage.orientation, data['puissance']))
        message = {"action":"tirs", "data":([xtir,self.personnage.rect.centery],self.personnage.orientation,id_tir,data['puissance'])}
        self._server.SendMessageAll(message)
        
    def Network_attack(self, data):
        self.personnage.attaquer()
        self.sendMove()
        
    def Network_stopAttack(self, data):
        self.personnage.isAttacking = False
        self.sendMove()

#end ClientChannel
