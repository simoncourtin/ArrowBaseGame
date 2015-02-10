import pygame

class Personnage (pygame.sprite.Sprite):
    
    def __init__(self, numero):
        pygame.sprite.Sprite.__init__(self)
        self.numero = numero
        if self.numero == 1:
            self.image, self.rect = load_png("data/sprite/SpriteNeo.png")
            self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]  
            self.speed = [0,0]
        if self.numero == 2:
            self.image, self.rect = load_png("data/sprite/SpriteDarkVador.png")
            self.rect.center = [SCREEN_WIDTH/2+50, SCREEN_HEIGHT/2]  
            self.speed = [0,0]
        if self.numero == 3:
            self.image, self.rect = load_png("data/sprite/SpriteDeadpool.png")
            self.rect.center = [SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2]  
            self.speed = [0,0]
        if self.numero == 4:
            self.image, self.rect = load_png("data/sprite/SpriteVegeta.png")
            self.rect.center = [SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2]  
            self.speed = [0,0]
        
    def sauter(self):
        if self.numero == 1:
            self.image = pygame.image.load("data/sprite/SpriteNeoSaut.png")
        if self.numero == 2:
            self.image = pygame.image.load("data/sprite/SpriteDarkVadorSaut.png")
        if self.numero == 3:
            self.image = pygame.image.load("data/sprite/SpriteDeadpoolSaut.png")
        if self.numero == 4:
            self.image = pygame.image.load("data/sprite/SpriteVegetaSaut.png")
        
    def down(self):
        if self.numero == 1:
            self.image = pygame.image.load("data/sprite/SpriteNeoAccroupi.png")
            self.rect.y = self.rect.y+10
        if self.numero == 2:
            self.image = pygame.image.load("data/sprite/SpriteDarkVadorAccroupi.png")
            self.rect.y = self.rect.y+20
        if self.numero == 3:
            self.image = pygame.image.load("data/sprite/SpriteDeadpoolAccroupi.png")
            self.rect.y = self.rect.y+35
        if self.numero == 4:
            self.image = pygame.image.load("data/sprite/SpriteVegetaAccroupi.png")
            self.rect.y = self.rect.y+10
        
    def left(self):
        self.speed[0]=-5
        
    def right(self):
        self.speed[0]=5
    
    def stop(self):
        self.speed=[0,0]

    def update(self):
        self.rect = self.rect.move(self.speed)