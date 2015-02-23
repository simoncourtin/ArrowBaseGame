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
        self.joueurs = pygame.sprite.Group()
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
        self.joueurs.remove(channel.personnage)
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
        self.joueurs.update()
        # Events
        # Collisions
        listeCollisions = pygame.sprite.groupcollide(self.joueurs,self.carte.getCalqueIndice(1).getGroupeTuiles(),False,False)
        for joueur in listeCollisions.keys():
            for tile in listeCollisions[joueur]:
                if joueur.rect.centerx < tile.rect.centerx and joueur.rect.right > tile.rect.left:
                    #rajouter test pas de tile a gauche de celle-ci
                    print "collision gauche du mur"
                #end if
                if joueur.rect.centerx > tile.rect.centerx and joueur.rect.left < tile.rect.right:
                    #rajouter test pas de tile a droite de celle-ci
                    print "collision droite du mur"
                #end if
                if joueur.rect.centery < tile.rect.centery and joueur.rect.bottom > tile.rect.top:
                    #rajouter test pas de tile au dessus de celle-ci
                    print "collision haut du mur"
                #end if
                if joueur.rect.centery > tile.rect.centery and joueur.rect.top < tile.rect.bottom:
                    #rajouter test pas de tile en dessous de celle-ci
                    print "collision bas du mur"
                #end if
            #end for
        #end for
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)  # closing the window exits the program
            # end if
        # end for
    #end Loop
#end Serveur

if __name__ == '__main__':
    server = Serveur(localaddr = (sys.argv[1], int(sys.argv[2])))
    carte = server.generationMap()
    while True:
        server.Loop()

    sys.exit(0)
    #end MyServer
