#!/usr/bin/env python
# coding : utf-8

from PodSixNet.Channel import Channel
import Personnage
import Tir
import math
import random

VITESSE_DEBUT_LANCER = 20


class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.identifiant = 0
        self.pseudo = ""
        position = [
                random.randint(self._server.carte.tile_width, (self._server.carte.largeur_map * self._server.carte.tile_width) - self._server.carte.tile_width),
                random.randint(self._server.carte.tile_height, (self._server.carte.hauteur_map * self._server.carte.tile_height) - self._server.carte.tile_height)]
        self.personnage = Personnage.Personnage(1,self.identifiant,position)
        self._server.joueurs.add(self.personnage)
    # end __init__


    def sendMove(self):
        message = {"action":"move", "data":(self.personnage.rect.center,self.personnage.speed, self.personnage.orientation,self.personnage.isAttacking),'id':self.identifiant}
        self._server.SendMessageAll(message)
    #end sendMove


    def sendTir(self,id, puissance, vitesse):
        message = {"action":"tirs", "data":(self.personnage.rect.center, vitesse,id, puissance)}
        self._server.SendMessageAll(message)
    #end sendTir

    def set_identifiant(self,id):
        self.identifiant = id
        self.personnage.idJoueur = id


    def Close(self):
        self._server.del_client(self)
        print 'Client parti'
    #end Close



    def Network_move(self, data):
        if self.personnage.mort == False:
            mouvement=data['touche']
            if(mouvement == "bas"):
                if self.personnage.orientation == "droite" or self.personnage.orientation == "gauche":
                    self.personnage.orienter("bas")
                #end if

                self.personnage.down()
            elif(mouvement == "saut"):
                if self.personnage.orientation == "bas" or self.personnage.orientation == "gauche" or self.personnage.orientation == "droite" :
                    self.personnage.orienter("haut")
                #end if

                self.personnage.sauter()
            elif(mouvement == "gauche"):
                if self.personnage.orientation == "droite" or self.personnage.orientation == "bas" :
                    self.personnage.orienter("gauche")
                self.personnage.left()
            elif(mouvement == "droite"):
                if self.personnage.orientation == "gauche" or self.personnage.orientation == "bas":
                    self.personnage.orienter("droite")
                self.personnage.right()
            elif(mouvement == "saut"):
                self.personnage.sauter()

            self.sendMove()
        #end if

    def Network_tir(self, data):
        #si le personnage est mort il n'a pas le droit de tirer
        if self.personnage.mort == False:
            id_tir= len(self._server.tirs)
            #Calcul de la vitesse du projectile
            vitesseTir = [data["clic"][0]-self.personnage.rect.centerx, data["clic"][1]-self.personnage.rect.centery]
            normeVitesse = math.sqrt(vitesseTir[0]*vitesseTir[0] + vitesseTir[1]*vitesseTir[1])
            vitesseTir[0] = int( float(vitesseTir[0]) * VITESSE_DEBUT_LANCER / normeVitesse )
            vitesseTir[1] = int( float(vitesseTir[1]) * VITESSE_DEBUT_LANCER / normeVitesse )
            #calcul avec vitesse du personnage
            vitesseFlechex =self.personnage.rect.centerx+vitesseTir[0]+self.personnage.speed[0]
            vitesseFlechey =self.personnage.rect.centery+vitesseTir[1]+self.personnage.speed[1]
            self._server.tirs.add(Tir.Tir(data['idJoueur'],id_tir,[vitesseFlechex,vitesseFlechey],vitesseTir, data['puissance']))
            self.sendTir(id_tir, data['puissance'], vitesseTir)
        #end if
        
    def Network_attack(self, data):
        #si le personnage est mort il n'a pas le droit d'attaquer
        if self.personnage.mort == False:
            self.personnage.attaquer()
            self.personnage.startAttack=self._server.temp_jeu
            self._server.SendMessageAll({"action":"attaque","idJoueur": self.identifiant})
        
    def Network_pseudo(self, data):
        self._server.ids[self.identifiant] = data["pseudo"]
        self.pseudo = data["pseudo"]
        self.personnage.pseudo = data["pseudo"]
        self._server.SendMessageAll({"action":"pseudo","pseudo":self.pseudo,"identifiant":self.identifiant})

    def Network_pause(self, data):
        message = {"action": "pause", "idJoueur": self.identifiant}
        self._server.SendMessageAll(message)

    def Network_recommencer_partie(self,data):
        self._server.remise_a_zero()

#end ClientChannel
