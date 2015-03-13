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
import Tir
from  module_map import Map
import random

for x in range(20):
  map = random.randint(1,4)

listeImages = {}
TAB_MAP = [("Image","/../../data/map/map0" + str(map) + "/background.png",True),
            ("","/../../data/map/map0" + str(map) + "/plateforme.map","/../../data/map/map0" + str(map) + "/terre.png",32,32)]
CONFIG_FILE = "/../../data/map/map0" + str(map) + "/config.map"
MAX_JOUEUR = 2

class Serveur(Server):
    channelClass = ClientChannel.ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.nb_joueur = 0
        self.ids=[]
        self.clients = []
        self.joueurs = pygame.sprite.Group()
        self.tirs = pygame.sprite.Group()
        print('Server launched')
        self.clock = pygame.time.Clock()
        #definiriton de le la fenetre
        self.screen = pygame.display.set_mode((50, 50))
        self.carte = None
        self.temp_jeu = 0
    #end __init_

    def Connected(self, channel, addr):
        print 'New connection'
        print 'Nouveau client'
        self.clients.append(channel)
        if len(self.clients) <= MAX_JOUEUR:
            self.nb_joueur += 1
            print 'Client avec id : ' + str(self.nb_joueur)
            #on attibut un id au channel
            channel.set_identifiant(self.nb_joueur)
            #on ajoute l'identifants a la liste des ids
            self.ids.append(self.nb_joueur)
            #on envoie l'identifiant au client
            channel.Send({'action':'identification','id':self.nb_joueur})
            #envoi de la map generer par le serveur
            channel.Send({'action':'carteJeu','carte':TAB_MAP,'config':CONFIG_FILE})
            #on envoie les position de tous les personnage a tous le monde
            self.SendMessageAll({'action':'players','ids':self.ids})
            for c in self.clients:
                c.sendMove()
        else:
            #nombre de joueur max atteind
            print "Nombre de joueurs max Atteint"
            #on envoie un message de refus
            channel.Send({'action':'refused','message':"Nombre de joueur max Atteind"})
            channel.Close()
        #end if
        if len(self.clients)==MAX_JOUEUR:
            self.SendMessageAll({'action':'game','statut':'start'})
            #on remet le temp de jeu a 0
            self.temp_jeu = 0
        #end if
    #end Connected

    def del_client(self,channel):
        print('client deconnecte')
        if channel.identifiant !=0:
            #le client a ete identifie
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
        #creation de la carte
        carte = Map.Map(self.screen,CONFIG_FILE,TAB_MAP)
        self.carte=carte
        return carte
    #end generationMap

    def Loop(self):
        #for c in self.clients:
        #    c.personnage.stopHorizontal()
        #end for

        # Stuff
        self.Pump()
        self.clock.tick(60) # max speed is 60 frames per second

        # Updates
        self.carte.afficherCarte()
        self.joueurs.update()
        self.tirs.update()

        # Events


        # Collisions
        #fleche et carte
        collisionsTirsMur = pygame.sprite.groupcollide(self.tirs,self.carte.getCalqueIndice(1).getGroupeTuiles(),True,False)
        for tir in collisionsTirsMur.keys():
            # On envoie au client le tir a detruire
            self.SendMessageAll({"action":"kill_tir","idTir":tir.idFleche})

        #joueur et fleches
        collisionsTirsJoueur = pygame.sprite.groupcollide(self.tirs,self.joueurs,True,False)
        for tir in collisionsTirsJoueur.keys():
            for joueur in collisionsTirsJoueur[tir] :
                #si le joueur touhe est deja mort
                if joueur.mort == False :
                    #On tue le personnage
                    joueur.mourir()
                    print str(joueur.rect.center)
                    joueur.capture_frame_actuel = self.temp_jeu
                    #on envoie le message aux clients pour savoir qui est le tueur et qui est le tue
                    self.SendMessageAll({"action":"kill_pers","methode":"fleche","id_tuer":joueur.idJoueur,"id_tueur":tir.idJoueur})
                    #on envoie aux clients la fleche a detruire
                    self.SendMessageAll({"action":"kill_tir","idTir":tir.idFleche})
                    #on recherche le tireur pour lui attribuer un point
                    for tireur in self.joueurs:
                        if tireur.idJoueur == tir.idJoueur:
                            #si le tir vient de lui meme alors on enleve un tir
                            if tireur.idJoueur == joueur.idJoueur:
                                ajout_score = -1
                            else:
                                ajout_score = 1
                            #end if
                            #On ajoute ou enleve le score au tireur
                            tireur.score += ajout_score
                            #on envoie le nouveau score aux client
                            self.SendMessageAll({"action" : "ajout_score","joueur" : tireur.idJoueur,"score" : tireur.score})
                        #end if
                    #end for
                #end if
            #end for
        #end for


        #joueurs et carte
        listeCollisions = pygame.sprite.groupcollide(self.joueurs,self.carte.getCalqueIndice(1).getGroupeTuiles(),False,False)
        for joueur in listeCollisions.keys():
            # On recupere le channel du joueur
            channel = None
            for c in self.clients:
                if c.personnage == joueur:
                    channel = c

            # On parcourt tous les tuiles en collisions et on cherche de quel cote elle se fait
            for tile in listeCollisions[joueur]:
                # Initialisation des variables
                rightCol = False 
                leftCol = False 
                topCol = False 
                bottomCol = False 
                horizontalOffset = 0
                verticalOffset = 0

                # Collision par la droite du joueur
                if joueur.rect.centerx < tile.rect.centerx and joueur.rect.right > tile.rect.left:
                    # S'il n'y a pas de tuile a gauche de la tuile intersectee
                    if not self.carte.getCalqueIndice(1).hasTuileAt(tile.rect.centerx-tile.rect.w, tile.rect.centery):
                        rightCol = True
                        horizontalOffset = joueur.rect.right - tile.rect.left
                    #end if
                #end if

                # Collision par la gauche du joueur
                if joueur.rect.centerx > tile.rect.centerx and joueur.rect.left < tile.rect.right:
                    # S'il n'y a pas de tuile a droite de la tuile intersectee
                    if not self.carte.getCalqueIndice(1).hasTuileAt(tile.rect.centerx+tile.rect.w, tile.rect.centery):
                        leftCol = True
                        horizontalOffset =  tile.rect.right - joueur.rect.left
                    #end if
                #end if

                # Collision par le bas du joueur
                if joueur.rect.centery < tile.rect.centery and joueur.rect.bottom > tile.rect.top:
                    # S'il n'y a pas de tuile en haut de la tuile intersectee
                    if not self.carte.getCalqueIndice(1).hasTuileAt(tile.rect.centerx, tile.rect.centery-tile.rect.h):
                        bottomCol = True
                        verticalOffset = joueur.rect.bottom - tile.rect.top
                    #end if
                #end if

                # Collision par le haut du joueur
                if joueur.rect.centery > tile.rect.centery and joueur.rect.top < tile.rect.bottom:
                    # S'il n'y a pas de tuile en bas de la tuile intersectee
                    if not self.carte.getCalqueIndice(1).hasTuileAt(tile.rect.centerx, tile.rect.centery+tile.rect.h):
                        topCol = True
                        verticalOffset = tile.rect.bottom - joueur.rect.top
                    #end if
                #end if

                # Si collision verticale et horizontale
                if verticalOffset>0 and horizontalOffset>0:
                    if verticalOffset > horizontalOffset:
                        topCol = False
                        bottomCol = False
                    else:
                        leftCol = False
                        rightCol = False
                    #end fi
                #end if

                if rightCol:
                    self.SendMessageAll({'action':'collision','id':channel.identifiant, 'cote':'droite'})
                    joueur.rect.right = tile.rect.left+5
                    joueur.collision('droite')
                #end if

                if leftCol:
                    self.SendMessageAll({'action':'collision','id':channel.identifiant, 'cote':'gauche'})
                    joueur.rect.left = tile.rect.right-5
                    joueur.collision('gauche')
                #end if

                if topCol:
                    self.SendMessageAll({'action':'collision','id':channel.identifiant, 'cote':'haut'})
                    joueur.rect.top = tile.rect.bottom-5
                    joueur.collision('haut')
                #end if

                if bottomCol:
                    self.SendMessageAll({'action':'collision','id':channel.identifiant, 'cote':'bas'})
                    joueur.rect.bottom = tile.rect.top+5
                    joueur.collision('bas')
                #end if
            #end for
            
            # Check des collisions entre joueurs
            listeCollisionsJoueurs = pygame.sprite.groupcollide(self.joueurs,self.joueurs,False,False)
            for joueur in listeCollisionsJoueurs.keys():
                listeCollisionsJoueur = listeCollisionsJoueurs[joueur]
                if len(listeCollisionsJoueur)>1:
                    listeCollisionsJoueur = [x for x in listeCollisionsJoueur if x != joueur]
                    for joueurTouche in listeCollisionsJoueur:
                        #si le joueur est en phase d'attaque
                        if joueur.isAttacking:
                            #on regarde si le joueur est deja mot ou pas
                            if joueurTouche.mort == False :
                                #On tue le personnage
                                joueurTouche.mourir()
                                joueurTouche.capture_frame_actuel = self.temp_jeu
                                #on envoie le message aux clients pour savoir qui est le tueur et qui est le tue
                                self.SendMessageAll({"action":"kill_pers","methode":"melee","id_tuer":joueurTouche.idJoueur,"id_tueur":joueur.idJoueur})
                                #On ajoute le score au killer
                                joueur.score += 1
                                #on envoie le nouveau score aux client
                                self.SendMessageAll({"action" : "ajout_score","joueur" : joueur.idJoueur,"score" : joueur.score})
                        else:
                            if joueur.rect.centerx > joueurTouche.rect.centerx:
                                self.SendMessageAll({'action':'collisionJoueur','id':channel.identifiant, 'cote':'gauche'})
                                joueur.rect.left = joueurTouche.rect.right-5
                                joueur.collision('gauche')
                            #end if
                            if joueur.rect.centerx < joueurTouche.rect.centerx:
                                self.SendMessageAll({'action':'collisionJoueur','id':channel.identifiant, 'cote':'droite'})
                                joueur.rect.right = joueurTouche.rect.left+5
                                joueur.collision('droite')
                            #end if
                        #end if
                    #end for
                #end if
            #end for
            # Envoi des nouvelles coordonnees de ce joueur
            channel.sendMove();
        #end for
        for j in self.joueurs:
                if j.mort == True:
                    if j.capture_frame_actuel + (4*60) <= self.temp_jeu:
                        print "joueur " + str(j.idJoueur) + " ressucite"
                        position = [random.randint(carte.tile_width,(carte.largeur_map*carte.tile_width)-carte.tile_width),random.randint(carte.tile_height,(carte.hauteur_map*carte.tile_height)-carte.tile_height)]
                        print str(position)
                        self.SendMessageAll({"action":"resurrection","id_joueur":j.idJoueur,"position":position})
                        j.resurrection(position)
                        j.rect.center=position
                        for c in self.clients:
                            if c.personnage == j:
                                c.sendMove()

        #condition de victoire
        for joueur in self.joueurs:
            if joueur.score == 2:
                #print "joueur " + str(joueur.idJoueur) + " a gagne"
                self.SendMessageAll({"action":"victoire", "idGagnant":joueur.idJoueur})


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)  # closing the window exits the program
            # end if
        # end for
        self.temp_jeu +=1
    #end Loop
#end Serveur

if __name__ == '__main__':
    server = Serveur(localaddr = (sys.argv[1], int(sys.argv[2])))
    carte = server.generationMap()
    cooldown_attack = 30
    while True:
        server.Loop()
    sys.exit(0)
    #end MyServer
