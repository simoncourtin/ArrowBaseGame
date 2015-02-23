#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PodSixNet.Connection import connection, ConnectionListener
import sys
import pygame
import GroupJoueur
import Personnage
import utils
from pygame.locals import *
import os
from  module_map import Map

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


listeImages = {}


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
        self.carte = None
        self.font_pixel_32 = pygame.font.Font("../data/font/pixelmix.ttf", 32)
        self.font_pixel_20 = pygame.font.Font("../data/font/pixelmix.ttf", 20)

        # Chargement du background de la map
        self.background_image, self.background_rect = utils.load_png(os.path.dirname(__file__)+"/../data/sprite/background.png")

        # Instanciation des personnages et des groupes de sprites
        self.monGroup =  GroupJoueur.GroupJoueur()
    # end __init__

    def Loop(self):
        while True:
            connection.Pump()
            self.monGroup.Pump()
            self.Pump()
            self.clock.tick(60)  # max speed is 60 frames per second
            # Events handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # closing the window exits the program
                # end if
            # end for
            if self.run:
                # Vitesse horizontale du joueur à zéro
                self.monGroup.stopHorizontal()

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
                self.monGroup.update()

                # drawings
                self.carte.afficherCarte()
                self.monGroup.draw(self.screen)


            #end if
            else:
                #ecran d'attente
                self.screen.fill(0)
                self.screen.blit(self.font_pixel_32.render("Veuillez patienter...", False, (255, 255, 255)),
                         (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 100))
                i=0
                for p in self.monGroup:
                    texte =self.font_pixel_20.render("Player " + str(p.idJoueur) , False, (255, 255, 255))
                    self.screen.blit(texte,(SCREEN_WIDTH / 2 - 100 , SCREEN_HEIGHT / 2 + i))
                    i+=50

            #end else
            # screen refreshing
            pygame.display.flip()
        #end while
    #end Loop

    ### Network event/message callbacks ###
    def Network_connected(self, data):
        print('Connexion au serveur !')
        print('En attente de l''identifcation ......')
    #end Network_connected

    def Network_identification(self,data):
        print 'attribution id sur le serveur. Id : '+ str(data['id'])
        #self.monGroup.add(Personnage.Personnage(1,data['id']))
        print 'creation du personnage'

    #end Network_identifiaction

    def Network_carteJeu(self,data):
        print 'En Attente de la carte '
        self.carte= Map.Map(self.screen,data['carte'])
        print 'la carte à bien été recu '
    #end Network_carteJeu

    def Network_game(self,data):
        if data['statut'] == 'start':
            self.screen.fill(0)
            self.run = True
    #end Network_startGame

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()
        sys.exit()

    #end Network_error

    def Network_disconnected(self, data):
        print 'Server disconnected'
        sys.exit()

    #end Network_disconnected

#end Client

if __name__ == '__main__':
    client = Client(sys.argv[1], int(sys.argv[2]))

    client.Loop()

    sys.exit(0)
#end if