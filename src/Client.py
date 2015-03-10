#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PodSixNet.Connection import connection, ConnectionListener
import sys
import pygame
import GroupJoueur
import Camera
import GroupTir
import Tir
import utils
from pygame.locals import *
import os
from  module_map import Map

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

listeImages = {}


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.run = False  # Booléen déterminant si ce client est connecté au serveur ou non
        #connexion au serveur
        self.Connect((host, port))
        #initialisation de pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        #self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 1)
        #numero d'id sur le serveur
        self.idServeur = 0
        self.carte = None
        self.contolable = None


        self.font_pixel_32 = pygame.font.Font(os.path.dirname(__file__)+"/../data/font/pixelmix.ttf", 32)
        self.font_pixel_20 = pygame.font.Font(os.path.dirname(__file__)+"/../data/font/pixelmix.ttf", 20)
        self.point_vert = utils.load_png(os.path.dirname(__file__)+"/../data/image/point_vert.png")


        # Chargement du background de la map
        self.background_image, self.background_rect = utils.load_png(os.path.dirname(__file__)+"/../data/sprite/background.png")

        # Instanciation des personnages et des groupes de sprites
        self.monGroup =  GroupJoueur.GroupJoueur()

        # Instanciation des tirs et des sprites
        self.groupTir = GroupTir.GroupTir()
    # end __init__

    def Loop(self):
        spaceBarPressed = False
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
                #on regarde si le jeu est démarer ou si le personnage n'est pas en état mort pour activer le tir
                if self.run and self.contolable.mort == False:
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        shootStart = pygame.time.get_ticks()
                        print shootStart
                    if (event.type == pygame.MOUSEBUTTONUP):
                        shootEnd = pygame.time.get_ticks()
                        puissance = shootEnd - shootStart
                        print "Puissance du tir : " + str(puissance)
                        #print str(pygame.mouse.get_pos())+" origine :"+str(self.contolable.rect.x)+","+str(self.contolable.rect.y)
                        mousex, mousey = pygame.mouse.get_pos()
                        mousex += self.cam.state.x
                        mousey += self.cam.state.y

                        connection.Send({"action": "tir","idJoueur":self.contolable.idJoueur,"origine":(self.contolable.rect.x,self.contolable.rect.y), "puissance": puissance, "clic":[mousex, mousey]})

                # end if
            # end for

            if self.run :
                #on regarde si le personnage n'est pas en état mort pour activer les controles
                if self.contolable.mort == False:
                    # Gestion des événements de ce client (les touches sont celles d'un clavier anglais)
                    touches = pygame.key.get_pressed()
                    if (touches[K_DOWN] or touches[K_s]):
                        connection.Send({"action": "move", "touche": "bas"})
                    if (touches[K_LEFT] or touches[K_a]):
                        connection.Send({"action": "move", "touche": "gauche"})
                    if (touches[K_RIGHT] or touches[K_d]):
                        connection.Send({"action": "move", "touche": "droite"})
                    if (touches[K_SPACE] or touches[K_UP] or touches[K_w]):
                        if not spaceBarPressed:
                            connection.Send({"action": "move", "touche": "saut"})
                            spaceBarPressed = True
                        #end if
                    else:
                        spaceBarPressed = False
                    if (touches[K_q]):
                        connection.Send({"action": "attack", "touche": "a"})
                    else:
                        if self.contolable.isAttacking:
                            self.contolable.isAttacking = False
                            connection.Send({"action": "stopAttack"})

                # updates
                self.cam.update(self.contolable,self.screen)
                #print len(self.groupTir)
                self.groupTir.update()
                self.monGroup.update()

                # drawings
                self.screen.fill(0)
                self.carte.afficherCarteCamera(self.cam)
                self.monGroup.draw(self.screen,self.cam)
                self.groupTir.draw(self.screen,self.cam)

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
        self.idServeur = data['id']

    #end Network_identifiaction

    def Network_carteJeu(self,data):
        print 'En Attente de la carte '
        self.carte= Map.Map(self.screen,data['config'],data['carte'])
        print 'la carte à bien été recu '
        #la camera
        #self.cam = Camera.Camera(Camera.complex_camera, (self.carte.largeur_map * self.carte.tile_width), (self.carte.hauteur_map * self.carte.tile_width))
        self.cam = Camera.Camera(Camera.complex_camera, SCREEN_WIDTH, SCREEN_HEIGHT, self.carte.largeur_map*self.carte.tile_width, self.carte.hauteur_map*self.carte.tile_height)
    #end Network_carteJeu

    def Network_game(self,data):
        if data['statut'] == 'start':
            self.screen.fill(0)
            self.contolable = self.monGroup.getPlayerId(self.idServeur)
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



#end Client

if __name__ == '__main__':
    client = Client(sys.argv[1], int(sys.argv[2]))
    client.Loop()

    sys.exit(0)
#end if