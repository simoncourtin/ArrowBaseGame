import pygame
from PodSixNet.Connection import connection, ConnectionListener
import Tir

class GroupTir(pygame.sprite.Group, ConnectionListener):

    def Network_move(self, data):
        for s in self:
            if s.idFleche == data['id']:
                s.rect.center = data['data'][0]
                s.speed = data['data'][1]

    def Network_tirs(self, data):
        print 'Tir recu '+ str(data['data'][0])
        self.add(Tir.Tir(0,0,data['data'][0],data['data'][1]))

    def draw(self,screen,camera):
        for t in self:
            t.afficher(screen, camera)
