import os

import pygame

import load_png
import Animable


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

ACCELERATION_GRAVITE = 1
VITESSE_DEBUT_LANCER = 20
COEFF_FROTTEMENT = 0.003
PUISSANCE_MIN = 20
PUISSANCE_MAX = 60


class Tir(Animable.Animable):
    def __init__(self, idJoueur, idFleche, origine, direction, puissance):
        pygame.sprite.Sprite.__init__(self)
        Animable.Animable.__init__(self, cooldown=6)

        self.idJoueur = idJoueur
        self.idFleche = idFleche
        self.isActive = True
        self.orientation = "droite"
        self.image, self.rect = load_png.load_png(os.path.dirname(__file__) + "/../data/sprite/arrow.png")
        self.origine = origine
        self.rect.center = origine
        self.puissance = puissance / 10

        if self.puissance > PUISSANCE_MAX:
            self.puissance = PUISSANCE_MAX
        elif self.puissance < PUISSANCE_MIN:
            self.puissance = PUISSANCE_MIN

        self.speed = [self.puissance, 0]
        self.acceleration = [0, 0]

        if direction == "gauche":
            self.image = pygame.transform.flip(self.image, True, False)
            self.speed[0] *= -1


    def afficher(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def update(self):
        self.rect = self.rect.move(self.speed)
        Animable.Animable.update(self)

        self.acceleration[1] += -VITESSE_DEBUT_LANCER

        self.acceleration[1] = self.acceleration[0] + ACCELERATION_GRAVITE

        self.speed[0] -= self.speed[0] * COEFF_FROTTEMENT
        self.speed[1] -= self.speed[1] * COEFF_FROTTEMENT

        self.speed[0] += self.acceleration[0]
        self.speed[1] += self.acceleration[1]

        self.acceleration = [0,0]

        # Enlever le missile s'il depasse de l'ecran
        #if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
        #    self.kill()

            # Arreter la fleche s'il y a collision
