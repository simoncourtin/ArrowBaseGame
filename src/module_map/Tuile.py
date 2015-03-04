__author__ = 'Simon'
import pygame

# Simple sprite representant un element du decor avec
# lequel le joueur peut entrer en collision
class Tuile(pygame.sprite.Sprite):
	# Constructeur
    def __init__(self,image,numero,x, y):
       pygame.sprite.Sprite.__init__(self)

       # Image de la tuile
       self.image = image
       self.rect = self.image.get_rect()

       # Position de la tuile sur l'ecran
       self.rect.x = x
       self.rect.y = y

       # Variable contenant le type de tuile
       self.numero = numero

