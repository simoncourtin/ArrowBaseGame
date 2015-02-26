import pygame
import load_png
import os
import Animable

ACCELERATION_GRAVITE = 1

class Tir(Animable.Animable):
    def __init__(self, idJoueur, idFleche):
        pygame.sprite.Sprite.__init__(self)
        Animable.Animable.__init__(self, cooldown = 6)
        self.idJoueur = idJoueur
        self.idFleche = idFleche
        self.isActive = True
        self.orientation = "droite"

        self.image, self.rect = load_png.load_png(os.path.dirname(__file__) + "/../data/sprite/arrow.png")
        self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        self.speed = [0, 0]

    def update(self):
        self.rect = self.rect.move(self.speed)
        Animable.Animable.update(self)

        if self.isActive:
            self.speed[1] = self.speed[1] + ACCELERATION_GRAVITE

        # Arreter la fleche s'il y a collision
