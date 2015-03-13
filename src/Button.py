import pygame
import os
from pygame.locals import *
pygame.init()
class Button(pygame.sprite.Sprite):

    def __init__(self, color,texte ,width, height,position,marges,border, borderColor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.front = pygame.Surface([width + border*2, height + border*2],pygame.SRCALPHA)
        self.back = pygame.Surface([width + border*2, height + border*2])
        self.back.fill(borderColor)
        self.front.fill((255,255,255,0))
        self.image.fill(color)
        self.rect = self.front.get_rect()
        self.rect.x=position[0]
        self.rect.y=position[1]
        self.border = border
        self.position = position
        self.marges = marges
        self.font = pygame.font.Font(os.path.dirname(__file__)+"/../data/font/pixelmix.ttf", 20)
        self.texte =self.font.render(texte, False, (0, 0, 0))

    def afficher(self, screen):
        screen.blit(self.back, (self.position[0]-self.border ,self.position[1]-self.border))
        screen.blit(self.image, self.position)
        screen.blit(self.texte, (self.position[0]+self.marges,self.position[1]+self.marges))
        screen.blit(self.front, (self.position[0]-self.border ,self.position[1]-self.border))

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        print "pressed!"
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False




