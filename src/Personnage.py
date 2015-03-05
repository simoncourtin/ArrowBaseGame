import pygame
import load_png
import os
import Animable

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

VITESSE_DEPLACEMENT = 5
VITESSE_DEBUT_SAUT = 30
ACCELERATION_GRAVITE = 2
COEFF_FROTTEMENT = 0.1
VITESSE_MAX_X = 20
VITESSE_MAX_Y = 30


class Personnage(Animable.Animable):
    def __init__(self, numero,id):
        pygame.sprite.Sprite.__init__(self)
        Animable.Animable.__init__(self, cooldown=6)
        self.idJoueur=id
        self.numero = numero
        self.isAnimated = False
        self.isDown = False
        self.isJumping = False
        self.isAttacking = False
        self.orientation = "droite"

        self.collisionGauche = False
        self.collisionDroite = False
        self.collisionHaut = False
        self.collisionBas = False

        self.speed = [0,0]
        self.acceleration = [0,0]

        if self.numero == 1:
            self.image, self.rect = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteNeo.png")
            self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        #self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours1.png"))
        #self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours2.png"))
        #self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours3.png"))
        #self.add_frame(pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoCours4.png"))
        if self.numero == 2:
            self.image, self.rect = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteDarkVador.png")
            self.rect.center = [SCREEN_WIDTH/2+50, SCREEN_HEIGHT/2]
        if self.numero == 3:
            self.image, self.rect = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteDeadpool.png")
            self.rect.center = [SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2]
        if self.numero == 4:
            self.image, self.rect = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteVegeta.png")
            self.rect.center = [SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2]

    def sauter(self):
        if self.numero == 1:
            self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoSaut.png")
        if self.numero == 2:
            self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteDarkVadorSaut.png")
        if self.numero == 3:
            self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteDeadpoolSaut.png")
        if self.numero == 4:
            self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteVegetaSaut.png")

        if not self.isJumping:
            self.acceleration[1] += -VITESSE_DEBUT_SAUT
            self.isJumping = True
        elif self.collisionGauche: # wall jump
            self.acceleration[0] += VITESSE_DEBUT_SAUT
            self.acceleration[1] += -VITESSE_DEBUT_SAUT
        elif self.collisionDroite: # wall jump
            self.acceleration[0] += -VITESSE_DEBUT_SAUT
            self.acceleration[1] += -VITESSE_DEBUT_SAUT
        #end if
    #end sauter

    def down(self):
        if self.isDown == False:
            if self.numero == 1:
                self.isDown = True
                self.peutAttaquer = False
                self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoAccroupi.png")
                self.rect.y = self.rect.y+10
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
        self.acceleration[0]=-VITESSE_DEPLACEMENT
    #end left

    def right(self):
        self.acceleration[0]=VITESSE_DEPLACEMENT
    #end right

    def stopHorizontal(self):
        self.speed[0]=0
    #end stopHorizontal

    def stopVertical(self):
        self.speed[1]=0
    #end stopHorizontal

    def update(self):
        # Collisions
        if      self.collisionGauche    and self.speed[0]<0:
            self.stopHorizontal()
        elif    self.collisionDroite    and self.speed[0]>0:
            self.stopHorizontal()
        elif    self.collisionHaut      and self.speed[1]<0:
            self.stopVertical()
        elif    self.collisionBas       and self.speed[1]>0:
            self.stopVertical()
        #end if

        self.isJumping = True
        if self.collisionBas:
            self.isJumping = False

        self.rect = self.rect.move(self.speed)
        Animable.Animable.update(self)

        if self.isJumping:
            self.acceleration[1] = self.acceleration[1] + ACCELERATION_GRAVITE
            print "Pas de saut"
        #end if

        self.speed[0] -= self.speed[0]*COEFF_FROTTEMENT
        self.speed[1] -= self.speed[1]*COEFF_FROTTEMENT

        self.speed[0] += self.acceleration[0]
        self.speed[1] += self.acceleration[1]

        if self.speed[0]>VITESSE_MAX_X:
            self.speed[0] = VITESSE_MAX_X
        if self.speed[0]<-VITESSE_MAX_X:
            self.speed[0] = -VITESSE_MAX_X
        if self.speed[1]>VITESSE_MAX_Y:
            self.speed[1] = VITESSE_MAX_Y
        if self.speed[1]<-VITESSE_MAX_Y:
            self.speed[1] = -VITESSE_MAX_Y

        self.acceleration = [0,0]
        self.collisionGauche = False
        self.collisionDroite = False
        self.collisionHaut = False
        self.collisionBas = False
   
        if self.isAttacking:
        	self.image = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoHit.png")[0]
        else:
        	self.image = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteNeo.png")[0]

    #end update

    def orienter(self, direction):
        if self.orientation != "gauche":
            if direction == "gauche":
                self.orientation = "gauche"
                self.image = pygame.transform.flip(self.image, True, False)
        if self.orientation != "droite":
            if direction == "droite":
                self.orientation = "droite"
                self.image = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteNeo.png")[0]
        if self.orientation != "bas":
            if direction == "bas":
                self.orientation = "bas"
                self.image = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoAccroupi.png")
        if self.orientation != "haut":
            if direction == "haut":
                self.orientation = "droite"
                self.image = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteNeo.png")[0]
                self.rect.y = self.rect.y-10
                self.isDown = False
        #end if
    #end orienter
    
    def attaquer(self):
    	if self.isAttacking == False:
	    	self.isAttacking = True

    def afficher(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    #end afficher
    def collision(self, cote):
        if      cote == "gauche":
            self.collisionGauche=True;
        elif    cote == "droite":
            self.collisionDroite = True;
        elif    cote == "haut"  :
            self.collisionHaut = True;
        elif    cote == "bas"   :
            self.collisionBas = True;
        #end if
    #end collision

#end Personnage