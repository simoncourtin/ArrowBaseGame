import pygame
from pygame.locals import *
import os
import sys
from cPickle import load

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

# FUNCTIONS
def load_png(name):
    """Load image and return image object"""
    fullname=os.path.join('.',name)
    try:
        image=pygame.image.load(fullname)
        if image.get_alpha is None:
            image=image.convert()
        else:
            image=image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image,image.get_rect()


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

class Personnage (pygame.sprite.Sprite):
    
    def __init__(self, numero):
        pygame.sprite.Sprite.__init__(self)
        if numero == 1:
            self.image, self.rect = load_png("SpriteNeo.png")
            self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]  
            self.speed = [0,0]
        
    def sauter(self):
        self.image = pygame.image.load("SpriteNeoSaut.png")
        
        
    def down(self):
        self.image = pygame.image.load("SpriteNeoAccroupi.png")
        self.rect.y = self.rect.y+10
        
    def left(self):
        self.speed[0]=-5
        
    def right(self):
        self.speed[0]=5
    
    def stop(self):
        self.speed=[0,0]

    def update(self):
        self.rect = self.rect.move(self.speed)
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN | DOUBLEBUF)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1,1)    
    background_image, background_rect = load_png('background.png')
    
    while True:
        clock.tick(60)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return # closing the window exits the program  
        
        # Instanciation du personnage
        personnage=Personnage(1)
        perso_sprite = pygame.sprite.Group()
        perso_sprite.add(personnage)
        
        touches=pygame.key.get_pressed()
        
        if(touches[K_q]):
            return # exit the program    
        if(touches[K_DOWN]):  
            personnage.down()
        if(touches[K_LEFT]):  
            personnage.left()
        if(touches[K_RIGHT]):  
            personnage.right()
        if(touches[K_SPACE]):
            personnage.sauter()
            
        if not touches[K_LEFT] and not touches[K_RIGHT]:
            personnage.stop()
        
        perso_sprite.update()
        screen.blit(background_image, background_rect)
        perso_sprite.draw(screen)
        pygame.display.flip()
        
if __name__ == '__main__':
    main()
    sys.exit(0)