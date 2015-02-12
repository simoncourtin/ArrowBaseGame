#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pygame

from PodSixNet.Connection import connection, ConnectionListener
import Personnage
import utils
from pygame.locals import *
import os

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.run = False  # Booléen déterminant si ce client est connecté au serveur ou non
        #connexion au serveur
        self.Connect((host, port))
        #initialisation de pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 1)
        #numero d'id sur le serveur
        self.idServeur = 0
        # Chargement du background de la map
        self.background_image, self.background_rect = utils.load_png("/../data/sprite/background.png")

        # Instanciation des personnages et des groupes de sprites
        self.joueur = None
        self.autreJoueur = pygame.sprite.Group()
# end __init__

    def Loop(self):
        while True:
            if(self.run):
                connection.Pump()
                self.Pump()
                self.clock.tick(60)  # max speed is 60 frames per second

                #vitesse du joueur à zéro
                self.joueur.stopHorizontal()

                # Events handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return  # closing the window exits the program
                        # end if
                # end for


                # Gestion des événements de ce client
                touches = pygame.key.get_pressed()
                if (touches[K_DOWN]):
                    connection.Send({"action": "move", "touche": "bas"})
                if (touches[K_LEFT]):
                    connection.Send({"action": "move", "touche": "gauche"})
                if (touches[K_RIGHT]):
                    connection.Send({"action": "move", "touche": "droite"})
                if (touches[K_SPACE]):
                    connection.Send({"action": "move", "touche": "saut"})

                # updates
                self.joueur.update()
                self.autreJoueur.update()

                # drawings
                self.screen.blit(self.background_image, self.background_rect)
                self.joueur.update()
                self.autreJoueur.draw(self.screen)

                # screen refreshing
                pygame.display.flip()
            #end if
        #end while
    #end Loop

    ### Network event/message callbacks ###
    def Network_connected(self, data):
        print('Connexion au serveur !')
        print('attribution de l''id sur le serveur. Id : '+data['id'])
        self.joueur = Personnage.Personnage(1)
        print 'creation du personnage'
        self.run = True


    #end Network_connected

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()
        sys.exit()

    #end Network_error

    def Network_disconnected(self, data):
        print 'Server disconnected'
        sys.exit()

    #end Network_disconnected

    def Network_move(self, data):
        self.neo.rect.center = data['data'][0]
        self.neo.speed = data['data'][1]

    #end Network_move
#end Client

if __name__ == '__main__':
    client = Client(sys.argv[1], int(sys.argv[2]))

    client.Loop()

    sys.exit(0)
