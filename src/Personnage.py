import os
import pygame
import load_png



SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

ACCELERATION_DEPLACEMENT = 1
VITESSE_DEBUT_SAUT = 35
ACCELERATION_GRAVITE = 1.2
COEFF_FROTTEMENT = 0.1
VITESSE_MAX_X = 10
VITESSE_MAX_Y = 40


class Personnage(pygame.sprite.Sprite):
    def __init__(self, numero_sprite,id,center):
        pygame.sprite.Sprite.__init__(self)
        #chargement des images pour le joueur
        self.chargement_image(numero_sprite)
        self.idJoueur=id
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
        self.pseudo = "Player "+ str(self.idJoueur)

        self.speed = [0,0]
        self.acceleration = [0,0]

        self.image, self.rect = self.image_normale
        self.rect.center = center
        self.startAttack=0


    def sauter(self):
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

    def changer_image(self,image):
        self.image = image[0]
        self.rect.width = image[1].width
        self.rect.height = image[1].height

    def down(self):
        if self.isDown == False:
            self.isDown = True
            self.changer_image(self.image_accroupi_droite)
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
        if self.orientation != "bas" and self.isDown:
            self.isDown = False
            self.image = self.image_normale
            self.rect.width = self.image_normale[1].width
            self.rect.height = self.image_normale[1].height
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
            if not self.mort:
                if self.orientation=="droite":
                    self.changer_image(self.image_attaque_droite)
                if self.orientation=="gauche":
                    self.changer_image(self.image_attaque_gauche)
        else:
            if not self.mort:
                if self.orientation == "gauche":
                    self.changer_image(self.image_gauche)
                if self.orientation == "droite":
                    self.changer_image(self.image_droite)

    #end update

    def orienter(self, direction):
        if self.orientation != "gauche":
            if direction == "gauche":
                self.orientation = "gauche"
                self.changer_image(self.image_gauche)
        if self.orientation != "droite":
            if direction == "droite":
                self.orientation = "droite"
                self.changer_image(self.image_gauche)
        if self.orientation != "bas":
            if direction == "bas":
                self.orientation = "bas"
                self.down()
        #end if
    #end orienter
    
    def attaquer(self):
        self.isAttacking = True

    def afficher(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

    #end afficher
    def collision(self, cote):
        if      cote == "gauche":
            self.collisionGauche=True
        elif    cote == "droite":
            self.collisionDroite = True
        elif    cote == "haut"  :
            self.collisionHaut = True
        elif    cote == "bas"   :
            self.collisionBas = True
        #end if
    #end collision
    
    def mourir(self):
        self.mort = True
        self.image = self.image_mort[0]
        self.rect.width = self.image_mort[1].width
        self.rect.height = self.image_mort[1].height


    def resurrection(self,pos):
        self.mort = False
        self.image, self.rect = self.image_normale


    def chargement_image(self,numero_sprite):
        if numero_sprite == 1 :
             #les images de deplacements
            self.image_normale = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_bleu_gauche.png")
            self.image_gauche= self.image_normale
            self.image_droite = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_bleu_droite.png")
            self.image_haut = self.image_normale
            #image accroupi
            self.image_accroupi_droite = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_bleu_accroupi.png")
            self.image_accroupi_gauche = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_vert_acroupi_gauche.png")
            #image d'attaque
            self.image_attaque_gauche= load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_bleu_attaque_gauche.png")
            self.image_attaque_droite = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_bleu_attaque_droite.png")
        elif numero_sprite == 2 :
            #les images de deplacements
            self.image_normale = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_vert_gauche.png")
            self.image_gauche= self.image_normale
            self.image_droite = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_vert_droite.png")
            self.image_haut = self.image_normale
            #image accroupi
            self.image_accroupi_droite = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_vert_acroupi_droite.png")
            self.image_accroupi_gauche = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_vert_acroupi_gauche.png")
            #image d'attaque
            self.image_attaque_gauche= load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_vert_attaque_gauche.png")
            self.image_attaque_droite = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/archer_vert_attaque_droite.png")

        self.image_mort = load_png.load_png(os.path.dirname(__file__)+"/../data/sprite/archers/mort.png")

    #end chargement image
#end Personnage