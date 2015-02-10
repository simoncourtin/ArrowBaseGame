import pygame
from pygame.locals import *
import os
from cPickle import load
from src import Personnage
from src import Animable
from src import load_png

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN | DOUBLEBUF)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1,1)    
    background_image, background_rect = load_png.load_png('data/sprite/background.png')
    
    # Instanciation du personnage
    neo=Personnage.Personnage(1)
    darkVador=Personnage.Personnage(2)
    deadpool=Personnage.Personnage(3)
    personnage=Personnage.Personnage(4)
    team1 = pygame.sprite.Group()
    team2 = pygame.sprite.Group()
    team1.add(neo)
    team1.add(darkVador)
    team1.add(deadpool)
    team1.add(personnage)
    
    while True:
        clock.tick(60)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return # closing the window exits the program  
        
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
        
        team1.update()
        screen.blit(background_image, background_rect)
        team1.draw(screen)
        pygame.display.flip()