__author__ = 'Simon'
import pygame
class Tuile(pygame.sprite.Sprite):


    def __init__(self,image,numero,x, y):
       pygame.sprite.Sprite.__init__(self)
       self.image = image
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.numero = numero

