__author__ = 'Simon Courtin'
import pygame
import os

class CalqueImage:

    def  __init__(self,screen,image,fixe=True):
        self.image = pygame.image.load(os.path.dirname(__file__)+"/"+image).convert_alpha()
        self.screen = screen
        self.fixe = fixe


    def afficher_calque_camera(self,cam):
        self.screen.blit(self.image,(0,0))

    def afficher_calque(self):
        self.screen.blit(self.image,(0,0))
