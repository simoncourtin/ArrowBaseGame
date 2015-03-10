import os
import pygame
import load_png
import Animable


SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

ACCELERATION_DEPLACEMENT = 1
VITESSE_DEBUT_SAUT = 40
ACCELERATION_GRAVITE = 2
COEFF_FROTTEMENT = 0.1
VITESSE_MAX_X = 10
VITESSE_MAX_Y = 40


class Personnage(Animable.Animable):
    def __init__(self, numero,id):
        pygame.sprite.Sprite.__init__(self)
        Animable.Animable.__init__(self, cooldown=6)
        #chargement des images pour le joueur
        self.chargement_image(1)
        self.idJoueur=id
        self.numero = numero
        self.isAnimated = False
        self.isDown = False
        self.isJumping = False
        self.isAttacking = False
        self.orientation = "gauche"
        self.score = 0
        self.mort = False
        self.capture_frame_actuel = 0
        self.collisionGauche = False
        self.collisionDroite = False
        self.collisionHaut = False
        self.collisionBas = False

        self.speed = [0,0]
        self.acceleration = [0,0]

        self.image, self.rect = self.image_normale
        self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]


    def sauter(self):
        #changement de l'image sauter
        self.image = self.image_sauter
        #le saut
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
            self.isDown = True
            self.peutAttaquer = False
            self.image = self.image_accroupi
            self.rect.y = self.rect.y+10
    #end down

    def left(self):
        self.acceleration[0]=-ACCELERATION_DEPLACEMENT
    #end left

    def right(self):
        self.acceleration[0]=ACCELERATION_DEPLACEMENT
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
            self.image = self.image_attaque

    #end update

    def orienter(self, direction):
        if self.orientation != "gauche":
            if direction == "gauche":
                self.orientation = "gauche"
                self.image = self.image_gauche
        if self.orientation != "droite":
            if direction == "droite":
                self.orientation = "droite"
                self.image = self.image_droite
        if self.orientation != "bas":
            if direction == "bas":
                self.orientation = "bas"
                self.image = self.image_bas
        if self.orientation != "haut":
            if direction == "haut":
                self.orientation = "haut"
                self.image = self.image_haut
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
    
    def mourir(self):
        self.mort = True
        self.image = self.image_accroupi
        #self.rect.center = [SCREEN_WIDTH-300, SCREEN_HEIGHT-300]

    def chargement_image(self,numero_sprite):
        self.image_normale = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/SpriteNeo.png")
        self.image_sauter = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoSaut.png")
        self.image_accroupi = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoAccroupi.png")
        self.image_attaque = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoHit.png")
        self.image_droite = self.image_normale[0]
        self.image_gauche= pygame.transform.flip(self.image_droite, True, False)
        self.image_bas = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeoAccroupi.png")
        self.image_haut = pygame.image.load(os.path.dirname(__file__)+"/../data/sprite/SpriteNeo.png")
    #end chargement image
#end Personnage