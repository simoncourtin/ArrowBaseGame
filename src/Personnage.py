import pygame
import load_png
import os
import Animable

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

class Personnage(Animable.Animable):
    def __init__(self, numero):
        pygame.sprite.Sprite.__init__(self)
        Animable.Animable.__init__(self, cooldown=6)
        self.numero = numero
        if self.numero == 1:
            self.image, self.rect = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteNeo.png")
            self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]  
            self.speed = [0,0]
        if self.numero == 2:
        	self.image, self.rect = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteDarkVador.png")
        	self.rect.center = [SCREEN_WIDTH/2+50, SCREEN_HEIGHT/2]  
        	self.speed = [0,0]
        if self.numero == 3:
        	self.image, self.rect = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteDeadpool.png")
        	self.rect.center = [SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2]  
        	self.speed = [0,0]
        if self.numero == 4:
        	self.image, self.rect = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteVegeta.png")
        	self.rect.center = [SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2]  
        	self.speed = [0,0]
        
        def debout(self):
            if self.isAccroupi == True:
            	if self.numero == 1:
            		self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeo.png")
        
        def sauter(self):
            if self.numero == 1:
            	self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoSaut.png")
            if self.numero == 2:
            	self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteDarkVadorSaut.png")
            if self.numero == 3:
            	self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteDeadpoolSaut.png")
            if self.numero == 4:
            	self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteVegetaSaut.png")
        
        def down(self):
            if self.numero == 1:
            	if self.isAccroupi == False:
            		self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoAccroupi.png")
            		self.rect.y = self.rect.y+10
            		self.isAccroupi = True
            		self.debout()
            if self.numero == 2:
            	self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteDarkVadorAccroupi.png")
            	self.rect.y = self.rect.y+20
            if self.numero == 3:
            	self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteDeadpoolAccroupi.png")
            	self.rect.y = self.rect.y+35
            if self.numero == 4:
            	self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteVegetaAccroupi.png")
            	self.rect.y = self.rect.y+10
            #end down
            
        def left(self):
            self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours1.png"))
            self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours2.png"))
            self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours3.png"))
            self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours4.png"))
            self.speed[0]=-5
        #end left
        
        def right(self):
            self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours1.png"))
            self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours2.png"))
            self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours3.png"))
            self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours4.png"))
            self.speed[0]=5
        #end right
        
        def stopHorizontal(self):
            self.speed[0]=0
        #end stopHorizontal
        
        def stopVertical(self):
            self.speed[1]=0
        #end stopHorizontal
        
        def update(self):
            self.rect = self.rect.move(self.speed)
            Animable.Animable.update(self)

#end Personnage