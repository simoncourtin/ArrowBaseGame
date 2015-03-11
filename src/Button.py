import pygame
import os
from pygame.locals import *
pygame.init()
class Button(pygame.sprite.Sprite):

    def __init__(self, color,texte ,width, height,position,marges,border, borderColor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.back = pygame.Surface([width + border*2, height + border*2])
        self.back.fill((0,0,0))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.border = border
        self.position = position
        self.marges = marges
        self.font = pygame.font.Font(os.path.dirname(__file__)+"/../data/font/pixelmix.ttf", 20)
        self.texte =self.font.render(texte, False, (0, 0, 0))

    def afficher(self, screen):
        screen.blit(self.back, (self.position[0]-self.border ,self.position[1]-self.border))
        screen.blit(self.image, self.position)
        screen.blit(self.texte, (self.position[0]+self.marges,self.position[1]+self.marges))



