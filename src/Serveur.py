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

class Serveur(Server):
    channelClass = ClientChannel.ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.clients = []
        self.joueur ={}
        print('Server launched')
        self.clock = pygame.time.Clock()
        #definiriton de le la fenetre
        self.screen = pygame.display.set_mode((50, 50))

        #Instanciation des personnages
        self.team1 = pygame.sprite.Group()
        self.team2 = pygame.sprite.Group()

    #end __init_

    def Connected(self, channel, addr):
        print('New connection')
        self.clients.append(channel)
    #end Connected

    def del_client(self,channel):
        print('client deconnecte')
        self.clients.remove(channel)
    #end del_client

    def SendMessageAll(self, message):
        for c in self.clients:
            c.Send(message)
        #end for
    #end SendMessageAll

    def Loop(self):
        for c in self.clients:
            c.neo.stopHorizontal()
        #end for

        # Stuff
        self.Pump()
        self.clock.tick(60) # max speed is 60 frames per second

        # Events



        # Updates
        self.team1.update()
        self.team2.update()

    # Collisions

    #end Loop

if __name__ == '__main__':
    server = Serveur(localaddr = (sys.argv[1], int(sys.argv[2])))

    while True:
        server.Loop()
    sys.exit(0)
    #end MyServer
