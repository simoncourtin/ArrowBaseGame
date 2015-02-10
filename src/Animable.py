import pygame

class Animable(pygame.sprite.Sprite):
    def __init__(self, cooldown=20):
        pygame.sprite.Sprite.__init__(self)

        self.liste_images = []
        self.etape = 0
        self.cooldown_max = cooldown
        self.cooldown = cooldown

    def add_frame(self, image):
        self.liste_images.append(image)

    def update(self):
        if self.etape < len(self.liste_images): # On evite les crashs si le tableau est vide
            if self.cooldown > 0:
                self.cooldown -= 1
            else:
                if self.etape == len(self.liste_images)-1: # Derniere etape
                    self.etape = 0 # On retourne au debut
                else:
                    self.etape += 1 # Sinon on passe a  l'image suivante
                self.cooldown = self.cooldown_max

            # Enfin on change l'image
            self.image = self.liste_images[self.etape]