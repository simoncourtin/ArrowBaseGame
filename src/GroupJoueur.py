import pygame
from PodSixNet.Connection import connection, ConnectionListener
import Personnage

class GroupJoueur(pygame.sprite.Group,ConnectionListener):

    def Network_move(self, data):
        print str(data['id'])+" moves"
        for s in self:
            if s.idJoueur == data['id']:
                s.rect.center = data['data'][0]
                s.speed = data['data'][1]

    def Network_players(self,data):
        for i in data['ids']:
            if not self.existPlayer(i):
                self.add(Personnage.Personnage(1,i))


    def existPlayer(self,id):
        for s in self:
            if(s.idJoueur == id):
                return True
        return False

    def stopHorizontal(self):
        for s in self:
            s.stopHorizontal()