#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PodSixNet.Connection import connection, ConnectionListener
import sys
import pygame
import GroupJoueur
import Personnage
import GroupTir
import Tir
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
        self.point_vert = utils.load_png(os.path.dirname(__file__)+"/../data/image/point_vert.png")


        # Chargement du background de la map
        self.background_image, self.background_rect = utils.load_png(os.path.dirname(__file__)+"/../data/sprite/background.png")

        # Instanciation des personnages et des groupes de sprites
        self.monGroup =  GroupJoueur.GroupJoueur()

        # Instanciation des tirs et des sprites
        self.groupTir = GroupTir.GroupTir()
    # end __init__

    def Loop(self):
        while True:
            connection.Pump()
            self.monGroup.Pump()
            self.groupTir.Pump()
            self.Pump()
            self.clock.tick(60)  # max speed is 60 frames per second
            # Events handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # closing the window exits the program
                # end if
                if (event.type == pygame.MOUSEBUTTONUP):
                    print 'Tir'
                    connection.Send({"action": "tir"})
                # end if
            # end for
            if self.run:
                # Vitesse horizontale du joueur à zéro
                #self.monGroup.stopHorizontal()

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
                self.groupTir.update()

                # drawings
                self.carte.afficherCarte()
                self.monGroup.draw(self.screen)

                self.groupTir.draw(self.screen)


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
            #end if

            # screen refreshing
            pygame.display.flip()
        #end while
    #end Loop

    ### Network event/message callbacks ###
    def Network_connected(self, data):
        print('Connexion au serveur !')
        print('En attente de l identifcation ......')
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

    def Network_refused(self,data):
        print data['message']
        sys.exit()
    #end network_refused

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()
        sys.exit()

    #end Network_error

    def Network_disconnected(self, data):
        print 'Server disconnected'
        sys.exit()
    #end Network_disconnected*

    def Network_collision(self, data):
        for joueur in self.monGroup:
            if joueur.idJoueur == data['id']:
                joueur.collision(data['cote'])
            #end if
        #end for
    #end Network_collision

#end Client

if __name__ == '__main__':
    client = Client(sys.argv[1], int(sys.argv[2]))
    client.Loop()

    sys.exit(0)
#end if