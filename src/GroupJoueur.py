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
                if data['data'][3]:
                    s.attaquer()
                else:
                    s.isAttacking = False

    def Network_playerQuit(self, data):
        print str(data['id'])+" left the game"
        for s in self:
            if s.idJoueur == data['id']:
               self.remove(s)

    def Network_players(self,data):
        for i in data['ids']:
            if not self.existPlayer(i):
                self.add(Personnage.Personnage(1,i))
        print len(self)

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
                print "joueur "+ str(data["id_tuer"]) +" tue"
                joueur.mourir()
            #end if
        #end for
    #end Network_kill_pers

    def Network_ajout_score(self,data):
        player_killer = self.getPlayerId(data['joueur'])
        player_killer.score = data['score']
    #end Network_ajout_score

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


