#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PodSixNet.Connection import connection, ConnectionListener
import sys
import pygame
import GroupJoueur
import Camera
import GroupTir
import Button
import utils
from pygame.locals import *
import os
from  module_map import Map

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

listeImages = {}


class Client(ConnectionListener):
    def __init__(self, host, port,pseudo=None):
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
        self.pseudo = pseudo
        self.carte = None
        self.controlable = None
        self.isPaused = False
        self.fin_du_jeu = 0
        self.controles_actif = False


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

    def pause(self, liste_event):
        self.isPaused = True
        self.screen.fill(0)
        self.screen.blit(self.font_pixel_32.render("Pause", False, (255, 255, 255)),
                     (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 50))

        btn_reprendre_pause = Button.Button((56,142,60), "Reprendre", 160, 48, (SCREEN_WIDTH / 2 - 64, SCREEN_HEIGHT / 2 + 100 ), 12, 4, (56,142,60))
        btn_quitter_pause = Button.Button((244,67,54), "Quitter", 160, 48, (SCREEN_WIDTH / 2 - 64, SCREEN_HEIGHT / 2 + 164 ), 12, 4, (244,67,54))
        btn_reprendre_pause.afficher(self.screen)
        btn_quitter_pause.afficher(self.screen)

        for event in liste_event:
            if (event.type == pygame.MOUSEBUTTONUP):
                if (btn_reprendre_pause.pressed(pygame.mouse.get_pos())):
                    connection.Send({"action": "pause", "idJoueur": self.idServeur})
                if (btn_quitter_pause.pressed(pygame.mouse.get_pos())):
                    sys.exit()


    def chargement_musique(self):
        # chargement du fond sonore
        pygame.mixer.music.load(os.path.dirname(__file__) + "/../data/music/Celtic_Impulse.ogg")
        # chargement des bruitages
        self.hit = pygame.mixer.Sound(os.path.dirname(__file__) + "/../data/music/hit.ogg")
        self.arrow = pygame.mixer.Sound(os.path.dirname(__file__) + "/../data/music/23185.ogg")


    def tir_detection(self, event,shootStart):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            shootStart = pygame.time.get_ticks()
        if (event.type == pygame.MOUSEBUTTONUP):
            shootEnd = pygame.time.get_ticks()
            puissance = shootEnd - shootStart
            mousex, mousey = pygame.mouse.get_pos()
            mousex += self.cam.state.x
            mousey += self.cam.state.y
            self.arrow.play()
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
            return spaceBarPressed

    def menu_pause(self, escapePressed, touches):
        # Menu pause et la touche escape
        if (touches[K_ESCAPE]):
            if not escapePressed:
                escapePressed = True
                connection.Send({"action": "pause", "idJoueur": self.idServeur})
        else:
            escapePressed = False
        return escapePressed

    def ecran_attente(self):
        # ecran d'attente
        self.screen.fill(0)
        self.screen.blit(self.font_pixel_32.render("Veuillez patienter...", False, (255, 255, 255)),
                         (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 100))
        i = 0
        for p in self.monGroup:
            texte = self.font_pixel_20.render(str(p.pseudo), False, (255, 255, 255))
            self.screen.blit(texte, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + i))
            i += 50

    def fin_partie_message(self):
        #on desactive les controle
        self.controles_actif = False
        #le joueur a gagne
        if self.fin_du_jeu == 1:
            image_victoire = pygame.image.load(os.path.dirname(__file__) + "/../data/image/fleche_victoire.png")
            self.screen.blit(image_victoire, (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 150 ))
            self.screen.blit(self.font_pixel_32.render("Victoire", False, (255, 255, 255)),
                             (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 + 20))
        #le joueur a perdu
        elif self.fin_du_jeu == 2:
            image_victoire = pygame.image.load(os.path.dirname(__file__) + "/../data/image/fleche_cassee.png")

            self.screen.blit(image_victoire, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100 ))
            self.screen.blit(self.font_pixel_32.render("Defaite", False, (170, 170, 170)),
                             (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 ))
        i=0
        for j in self.monGroup:
            self.screen.blit(self.font_pixel_20.render(j.pseudo +" : "+ str(j.score), False, (255, 255, 255)),
                            (20, 20 +i ))
            i += 30



    def touche_attaque(self, attackKeyPressed, event):
        if event.type == KEYDOWN:
            if event.key == pygame.K_q:
                if not attackKeyPressed:
                    print "attaque"
                    connection.Send({"action": "attack"})
                    attackKeyPressed = True
                #end if
            #end if
        #end if
        elif event.type == KEYUP:
            if event.key == pygame.K_q:
                if attackKeyPressed:
                    attackKeyPressed = False
                #end if
            #end if
        # end if

        return attackKeyPressed


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
            liste_event =  pygame.event.get()
            for event in liste_event:
                if event.type == pygame.QUIT:
                    return  # closing the window exits the program
                # end if

                #les touche pour les attaque de melle
                attackKeyPressed = self.touche_attaque(attackKeyPressed, event)

                #on regarde si le jeu est démarer ou si le personnage n'est pas en état mort pour activer le tir
                if self.run and not self.controlable.mort and self.controles_actif:
                    #gestion des tirs
                    shootStart = self.tir_detection(event, shootStart)
                #end if
            # end for

            # Gestion des événements (les touches sont celles d'un clavier anglais)
            touches = pygame.key.get_pressed()
            #on regarde si le personnage n'est pas en état mort  et le jeu commence
            if self.run:
                if not self.controlable.mort:
                    if self.controles_actif:
                        spaceBarPressed = self.mouvment_and_attack(spaceBarPressed, touches)
                        #l action d attaque
                        #attackKeyPressed,startAttack,lastAttack = self.touches_attaques(attackKeyPressed, touches,startAttack,lastAttack)
                    #escape et menu pause
                escapePressed = self.menu_pause(escapePressed, touches)


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

            if not self.run:
                self.ecran_attente()
            #end if

            #action a la fin du jeu
            if self.fin_du_jeu > 0:
                self.fin_partie_message()
                if not self.isPaused :
                    btn_recommencer = Button.Button((56,142,60), "Recommencer", 180, 48, (SCREEN_WIDTH / 2 - 64, SCREEN_HEIGHT / 2 + 100 ), 12, 4, (56,142,60))
                    btn_quitter = Button.Button((244,67,54), "Quitter", 180, 48, (SCREEN_WIDTH / 2 - 64, SCREEN_HEIGHT / 2 + 164 ), 12, 4, (244,67,54))
                    btn_recommencer.afficher(self.screen)
                    btn_quitter.afficher(self.screen)


                    for event in liste_event:
                        if (event.type == pygame.MOUSEBUTTONUP):
                            if(btn_recommencer.pressed(pygame.mouse.get_pos())):
                                self.screen.fill(0)
                                print "le joueur veux recommencer"
                                connection.Send({"action":"recommencer_partie"})
                            if(btn_quitter.pressed(pygame.mouse.get_pos())):
                                return


            #la pause
            if self.isPaused == True:
                self.pause(liste_event)


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
        #on a recu une identification on envoie le pseudo
        if self.pseudo != None:
            connection.Send({"action":"pseudo","pseudo":self.pseudo})
        else:
            connection.Send({"action":"pseudo","pseudo": "Player " + str(self.idServeur)})

    #end Network_identifiaction

    def Network_carteJeu(self,data):
        print 'En Attente de la carte '
        self.carte= Map.Map(self.screen,data['config'],data['carte'])
        print 'la carte à bien été recu '
        #la camera
        self.cam = Camera.Camera(Camera.complex_camera, SCREEN_WIDTH, SCREEN_HEIGHT, self.carte.largeur_map*self.carte.tile_width, self.carte.hauteur_map*self.carte.tile_height)
    #end Network_carteJeu

    def Network_game(self,data):
        self.chargement_musique()
        if data['statut'] == 'start':
            self.screen.fill(0)
            self.controlable = self.monGroup.getPlayerId(self.idServeur)
            self.controlable.chargement_image(2)
            self.run = True
            self.controles_actif = True
            #on demarre la musique
            pygame.mixer.music.play()
        elif data['statut'] == 'new' :
            self.fin_du_jeu = 0
            self.screen.fill(0)
            self.run = False
            self.controles_actif = False
            #on arrete la musique
            pygame.mixer.music.stop()

    #end Network_startGame

    def Network_pause(self, data):
        if self.isPaused == False:
            self.isPaused = True
            self.controles_actif = False
        else:
            self.isPaused = False
            self.controles_actif = True

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

    def Network_debut_jeu(self,data):
        self.fin_du_jeu =0
    
    def Network_victoire(self, data):
        if data["idGagnant"] ==  self.idServeur :
            self.fin_du_jeu =1 #victoire
        else:
            self.fin_du_jeu = 2 #defaite




#end Client

if __name__ == '__main__':
    pseudo = None
    if len(sys.argv) >= 4 :
        pseudo = sys.argv[3]

    client = Client(sys.argv[1], int(sys.argv[2]),pseudo)
    client.Loop()

    sys.exit(0)
#end if