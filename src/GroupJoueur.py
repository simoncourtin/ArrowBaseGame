import pygame
from PodSixNet.Connection import connection, ConnectionListener
import Personnage

class GroupJoueur(pygame.sprite.Group,ConnectionListener):

    def Network_move(self, data):
        for s in self:
            if s.idJoueur == data['id']:
                s.rect.center = data['data'][0]
                s.speed = data['data'][1]
                s.orienter(data['data'][2])
                s.isAttacking = data['data'][3]

    def Network_playerQuit(self, data):
        print str(data['id'])+" left the game"
        for s in self:
            if s.idJoueur == data['id']:
               self.remove(s)

    def Network_players(self,data):
        for i in data['ids']:
            if not self.existPlayer(i):
                self.add(Personnage.Personnage(1,i,[0,0]))

    def Network_collisionJoueur(self, data):
        for joueur in self:
            if joueur.idJoueur == data['id']:
                joueur.collision(data['cote'])
            #end if
        #end for
    #end Network_collision

    def Network_kill_pers(self, data):
        for joueur in self:
            if joueur.idJoueur == data["id_tuer"]:
                joueur.mourir()
            #end if
        #end for
    #end Network_kill_pers

    def Network_resurrection(self,data):
        joueur = self.getPlayerId(data['id_joueur'])
        joueur.resurrection(data["position"])
    #end Network_ajout_score

    def Network_ajout_score(self,data):
        player_killer = self.getPlayerId(data['joueur'])
        player_killer.score = data['score']
    #end Network_ajout_score

    def Network_attaque(self, data):
        personnage = self.getPlayerId(data["idJoueur"])
        #si le personnage est mort il n'a pas le droit d'attaquer
        if personnage.mort == False:
            personnage.attaquer()

    def Network_stop_attaque(self, data):
        personnage = self.getPlayerId(data["idJoueur"])
        personnage.isAttacking = False


    def getPlayerId(self,id):
        for s in self:
            if(s.idJoueur == id):
                return s
        return False

    def existPlayer(self,id):
        for s in self:
            if(s.idJoueur == id):
                return True
        return False

    def stopHorizontal(self):
        for s in self:
            s.stopHorizontal()

    def draw(self,screen,camera):
        for s in self:
            s.afficher(screen, camera)


