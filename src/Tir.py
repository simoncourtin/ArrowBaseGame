import pygame
import load_png
import os
import Animable

ACCELERATION_GRAVITE = 1

class Tir(Animable.Animable):
    def __init__(self,idJoueur,idFleche,origine,direction):
        pygame.sprite.Sprite.__init__(self)
        Animable.Animable.__init__(self, cooldown=6)
        self.idJoueur = idJoueur
        self.idFleche = idFleche
        self.isActive = True
        self.orientation = "droite"
        self.image, self.rect = load_png.load_png(os.path.dirname(__file__) + "/../data/sprite/arrow.png")
        if direction == "gauche":
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.center = origine
        self.speed=[20,0]
        if direction == "gauche":
            self.speed[0]*= -1

    def afficher(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    def update(self):
        self.rect = self.rect.move(self.speed)
        Animable.Animable.update(self)

        # Arreter la fleche s'il y a collision
