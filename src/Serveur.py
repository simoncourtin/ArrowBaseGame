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

listeImages = {}
TAB_MAP = [("Image","/../../data/map/map03/background.png",True),
            ("","/../../data/map/map03/plateforme.map",'/../../data/map/map03/terre.png',32,32)]
CONFIG_FILE = "/../../data/map/map03/config.map"
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


    #end __init_

    def Connected(self, channel, addr):
        print 'New connection'
        print 'Nouveau client'
        if len(self.clients)<MAX_JOUEUR:
            self.nb_joueur += 1
            print 'Client avec id : ' + str(self.nb_joueur)
            channel.identifiant = self.nb_joueur
            self.ids.append(self.nb_joueur)
            self.clients.append(channel)
            channel.Send({'action':'identification','id':self.nb_joueur})
            #envoi de la map generer par le serveur
            channel.Send({'action':'carteJeu','carte':TAB_MAP,'config':CONFIG_FILE})
            #on envoie les position de tous les personnage a tous le monde
            self.SendMessageAll({'action':'players','ids':self.ids})
            for c in self.clients:
                c.sendMove()
        else:
            print "Nombre de joueurs max Atteint"
            channel.Send({'action':'refused','message':"Nombre de joueur max Atteind"})
        #end if
        if len(self.clients)==MAX_JOUEUR:
            self.SendMessageAll({'action':'game','statut':'start'})
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
                    for collision in listeCollisionsJoueur:
                        #si le joueur est en phase d'attaque
                        if joueur.isAttacking:
                            collision.mourir()
                        else:
                            if joueur.rect.centerx > collision.rect.centerx:
                                self.SendMessageAll({'action':'collisionJoueur','id':channel.identifiant, 'cote':'gauche'})
                                joueur.rect.left = collision.rect.right-5
                                joueur.collision('gauche')
                            if joueur.rect.centerx < collision.rect.centerx:
                                self.SendMessageAll({'action':'collisionJoueur','id':channel.identifiant, 'cote':'droite'})
                                joueur.rect.right = collision.rect.left+5
                                joueur.collision('droite')
                            if joueur.rect.centery < collision.rect.centery:
                                self.SendMessageAll({'action':'collisionJoueur','id':channel.identifiant, 'cote':'bas'})
                                joueur.rect.top = collision.rect.bottom-5
                                joueur.collision('bas')
                            if joueur.rect.centery > collision.rect.centery:
                                self.SendMessageAll({'action':'collisionJoueur','id':channel.identifiant, 'cote':'haut'})
                                joueur.rect.bottom = collision.rect.top+20
                                joueur.collision('haut')
            
            # Envoi des nouvelles coordonnees de ce joueur
            channel.sendMove();
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
    cooldown_attack = 30
    while True:
        server.Loop()

    sys.exit(0)
    #end MyServer
