#!/usr/bin/env python
# coding : utf-8

import ClientChannel
from PodSixNet.Server import Server
import time,sys
import os
import pygame
from pygame.locals import *
import random
import Personnage
from  module_map import Map

listeImages = {}
TAB_MAP = [("Image","../../data/map/map02/background.png",True),
            ("","../../data/map/map02/plateforme.txt",'../../data/map/map02/terre.png',32,32)]

class Serveur(Server):
    channelClass = ClientChannel.ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.nb_joueur = 0
        self.ids=[]
        self.clients = []
        self.joueur = pygame.sprite.Group()
        print('Server launched')
        self.clock = pygame.time.Clock()
        #definiriton de le la fenetre
        self.screen = pygame.display.set_mode((50, 50))
        self.carte = None


    #end __init_

    def Connected(self, channel, addr):
        print 'New connection'
        print 'Nouveau client'
        self.nb_joueur += 1
        print 'Client avec id : ' + str(self.nb_joueur)
        channel.identifiant = self.nb_joueur
        self.ids.append(self.nb_joueur)
        self.clients.append(channel)
        channel.Send({'action':'identification','id':self.nb_joueur})
        #envoi de la map generer par le serveur
        channel.Send({'action':'carteJeu','carte':TAB_MAP})
        #on envoie les position de tous les personnage a tous le monde
        self.SendMessageAll({'action':'players','ids':self.ids})

        for c in self.clients:
            c.sendMove()
    #end Connected

    def del_client(self,channel):
        print('client deconnecte')
        self.ids.remove(channel.identifiant)
        self.joueur.remove(channel.personnage)
        self.SendMessageAll({'action':'playerQuit','id':channel.identifiant})
        self.clients.remove(channel)
    #end del_client

    def SendMessageAll(self, message):
        for c in self.clients:
            c.Send(message)
        #end for
    #end SendMessageAll

    def generationMap(self):
        #fichiers de tileset
        tileset = '../data/map/map01/terre.png'
        #creation de la carte
        carte = Map.Map(self.screen,TAB_MAP)
        self.carte=carte
        return carte
    #end generationMap

    def Loop(self):
        for c in self.clients:
            c.personnage.stopHorizontal()
        #end for

        # Stuff
        self.Pump()
        self.clock.tick(60) # max speed is 60 frames per second

        # Updates
        self.carte.afficherCarte()
        self.joueur.update()
        # Events
        wall = pygame.sprite.groupcollide(self.joueur,self.carte.getCalqueIndice(1).getGroupeTuiles(),False,False)
        for j in wall:
            print "collision"

    # Collisions

    #end Loop

if __name__ == '__main__':
    server = Serveur(localaddr = (sys.argv[1], int(sys.argv[2])))
    carte = server.generationMap()
    cooldown_attack = 30
    while True:
        server.Loop()

    sys.exit(0)
    #end MyServer
