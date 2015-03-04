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


    def existPlayer(self,id):
        for s in self:
            if(s.idJoueur == id):
                return True
        return False

    def stopHorizontal(self):
        for s in self:
            s.stopHorizontal()