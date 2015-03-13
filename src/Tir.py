import os

import pygame
import  math
import load_png
import Animable


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

ACCELERATION_GRAVITE = 1
COEFF_FROTTEMENT = 0.003
PUISSANCE_MIN = 20
PUISSANCE_MAX = 40
FACTEUR_PUISSANCE = 0.05


class Tir(Animable.Animable):
    def __init__(self, idJoueur, idFleche, origine, vitesse, puissance):
        pygame.sprite.Sprite.__init__(self)
        Animable.Animable.__init__(self, cooldown=6)

        self.idJoueur = idJoueur
        self.idFleche = idFleche
        self.isActive = True
        self.orientation = "droite"
        self.image, self.rect = load_png.load_png(os.path.dirname(__file__) + "/../data/sprite/arrow.png")
        self.image_base=self.image
        self.origine = origine
        self.rect.center = origine
        self.puissance = puissance / 10

        if self.puissance > PUISSANCE_MAX:
            self.puissance = PUISSANCE_MAX
        elif self.puissance < PUISSANCE_MIN:
            self.puissance = PUISSANCE_MIN

        #self.speed = [self.puissance, 0]
        self.acceleration = [0, 0]

        self.speed = [FACTEUR_PUISSANCE * self.puissance * vitesse[0], FACTEUR_PUISSANCE * self.puissance * vitesse[1]]


    def afficher(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.speed[0]!= 0 or self.speed[1]!= 0:
            self.image = pygame.transform.rotate(self.image_base,180*math.atan2(-self.speed[1],self.speed[0])/math.pi)
        Animable.Animable.update(self)

        self.acceleration[1] = ACCELERATION_GRAVITE

        self.speed[0] -= self.speed[0] * COEFF_FROTTEMENT
        self.speed[1] -= self.speed[1] * COEFF_FROTTEMENT

        self.speed[0] += self.acceleration[0]
        self.speed[1] += self.acceleration[1]

        self.acceleration = [0, 0]

