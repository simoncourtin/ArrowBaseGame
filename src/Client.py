#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PodSixNet.Connection import connection, ConnectionListener
import sys
import pygame
import GroupJoueur
import Camera
import GroupTir
import Button
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
        self.controlable = None
        self.isPaused = False
        self.fin_du_jeu = 0
        self.shootStart = 0


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

    def pause(self):
        self.isPaused = True
        self.screen.fill(0)
        self.screen.blit(self.font_pixel_32.render("Pause", False, (255, 255, 255)),
                     (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 50))


    def tir_detection(self, event,shootStart):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            shootStart = pygame.time.get_ticks()
        if (event.type == pygame.MOUSEBUTTONUP):
            shootEnd = pygame.time.get_ticks()
            puissance = shootEnd - shootStart
            print "Puissance du tir : " + str(puissance)
            # print str(pygame.mouse.get_pos())+" origine :"+str(self.contolable.rect.x)+","+str(self.contolable.rect.y)
            mousex, mousey = pygame.mouse.get_pos()
            mousex += self.cam.state.x
            mousey += self.cam.state.y

            connection.Send({"action": "tir", "idJoueur": self.controlable.idJoueur,
                             "origine": (self.controlable.rect.x, self.controlable.rect.y), "puissance": puissance,
                             "clic": [mousex, mousey]})
        return shootStart

    def mouvment_and_attack(self, spaceBarPressed, touches):
        if self.isPaused == False:
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
                    # end if
            else:
                spaceBarPressed = False
            if (touches[K_q]):
                connection.Send({"action": "attack", "touche": "a"})
            else:
                if self.controlable.isAttacking:
                    self.controlable.isAttacking = False
                    connection.Send({"action": "stopAttack"})
            return spaceBarPressed

    def menu_pause(self, escapePressed, touches):
        # Menu pause et la touche escape
        if (touches[K_ESCAPE]):
            if not escapePressed:
                print "Escape"
                escapePressed = True
                if self.isPaused == False:
                    self.isPaused = True
                else:
                    self.isPaused = False
                    # end if
        else:
            escapePressed = False
        return escapePressed

    def touches_attaques(self, attackKeyPressed, touches):
        if (touches[K_q]):
            if not attackKeyPressed:
                connection.Send({"action": "attack", "touche": "a"})
                attackKeyPressed = True
        else:
            if self.controlable.isAttacking:
                self.controlable.isAttacking = False
                connection.Send({"action": "stopAttack"})
            attackKeyPressed = False

    def Loop(self):
        spaceBarPressed = False
        escapePressed = False
        attackKeyPressed = False
        shootStart = 0
        while True:
            connection.Pump()
            self.monGroup.Pump()
            self.groupTir.Pump()
            self.Pump()
            self.clock.tick(60)  # max speed is 60 frames per second
            # Events handling

            #evenement pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # closing the window exits the program
                # end if
                #on regarde si le jeu est démarer ou si le personnage n'est pas en état mort pour activer le tir
                if self.run and self.controlable.mort == False:
                    shootStart = self.tir_detection(event, shootStart)

                #end if
                #ecran de fin du jeu
                if self.fin_du_jeu > 0:
                    myButton = Button.Button((200,200,200),"Recommencer",180,40,(SCREEN_WIDTH / 2-50, SCREEN_HEIGHT / 2+100 ),10,2,(70,70,70))
                    if (event.type == pygame.MOUSEBUTTONUP):
                        myButton.pressed(pygame.mouse.get_pos())
                    #end if

                # end if
            # end for

            # Gestion des événements (les touches sont celles d'un clavier anglais)
            touches = pygame.key.get_pressed()
            #on regarde si le personnage n'est pas en état mort  et le jeu commence
            if self.run and not self.controlable.mort :
                spaceBarPressed = self.mouvment_and_attack(spaceBarPressed, touches)
                #escape et menu pause
                escapePressed = self.menu_pause(escapePressed, touches)
                #l action d attaque
                attackKeyPressed = self.touches_attaques(attackKeyPressed, touches)

            # updates
                self.cam.update(self.controlable,self.screen)
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


            if self.fin_du_jeu > 0:
                print self.fin_du_jeu
                if self.fin_du_jeu == 1:
                    image_victoire = pygame.image.load(os.path.dirname(__file__)+"/../data/image/coupe_victoire.png")
                    self.screen.blit(image_victoire,(SCREEN_WIDTH / 2-50 , SCREEN_HEIGHT / 2 -75 ))
                    self.screen.blit(self.font_pixel_32.render("Victoire", False, (170, 170, 170)),
                                   (SCREEN_WIDTH / 2-50, SCREEN_HEIGHT / 2 ))
                elif self.fin_du_jeu == 2:
                    #image_victoire = pygame.image.load(os.path.dirname(__file__)+"/../data/image/coupe_victoire.png")
                    #self.screen.blit(image_victoire,(SCREEN_WIDTH / 2-50 , SCREEN_HEIGHT / 2 -75 ))
                    self.screen.blit(self.font_pixel_32.render("Defaite", False, (170, 170, 170)),
                                     (SCREEN_WIDTH / 2-50, SCREEN_HEIGHT / 2 ))
                myButton.afficher(self.screen)


            #la pause
            if self.isPaused == True:
                self.pause()


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
            self.controlable = self.monGroup.getPlayerId(self.idServeur)
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
    #end Network_disconnected
    
    def Network_victoire(self, data):
        if data["idGagnant"] ==  self.idServeur :
            self.fin_du_jeu =1 #victoire
        else:
            self.fin_du_jeu = 2 #defaite


#end Client

if __name__ == '__main__':
    client = Client(sys.argv[1], int(sys.argv[2]))
    client.Loop()

    sys.exit(0)
#end if