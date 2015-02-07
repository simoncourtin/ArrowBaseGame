__author__ = 'Simon Courtin'
import pygame
import Tuile as _tuile

class Calque():

    def __init__(self,screen,fichier,image,x_tile=32,y_tile=32,):
        #fenetre ou ajouter
        self.screen = screen

        #tilset de l'image du calque
        self.tilset = pygame.image.load(image).convert_alpha()

        #hauteur et largeur des tuile dans le tilset
        self.x_tile=x_tile
        self.y_tile=y_tile

        #tableau des spawn et des objet interactif
        self.spawn = []

        #largeur de la map
        self.largeur_map = 0
        self.hauteur_map = 0

        #le fichier ou se situe le schema de la map
        self.fichier = fichier

        #le groupe de tuiles
        self.group_tuiles = pygame.sprite.Group()

        self.creation_tableau_calque()
        self.construire_layer()


    def creation_tableau_calque(self):
        #Debut de le creation du calque
        #lecture du fichier
        self.f = open(self.fichier, "r")
        self.ligne = self.f.read()
        self.ligne = self.ligne.replace('\n','\n,')

        #generation du tableau pour les differents element du calque
        self.calque=[]
        self.calque= self.ligne.split(',')

    def construire_layer(self):
        hauteur = self.x_tile
        largeur = self.y_tile
        x=0
        y=0
        for element in self.calque:
            if element != '\n':
                self.largeur_map += 1
                if element!='0':
                    X ,Y = self.calcul_position_tuile_tilset(element)
                    tile = self.tilset.subsurface(X,Y,hauteur,largeur)
                    tuile = _tuile.Tuile(tile,element,x,y)
                    self.group_tuiles.add(tuile)
                    if element == '256':
                        self.group_tuiles.remove(tuile)
                        self.spawn.append((x ,y))
                x+=largeur
            else:
                y+=hauteur
                x=0
                self.hauteur_map += 1
                self.largeur_map = 0

    def calcul_position_tuile_tilset(self,element):
        #calul de la position x et y sur le tileset
        if int(element) % 16 == 0 and int(element) != 256:
            element = str(int(element) - 16)
        X = (((int(element))-(((int(element)-1)/16)*16))-1)*32
        Y=(int(element)/16)*32
        if(Y==512):
            Y= 512-32
        return X,Y

    def afficher_calque_camera(self, cam):
        for tuile in self.group_tuiles:
            self.screen.blit(tuile.image, cam.apply(tuile))

    def afficher_calque(self):
        for tuile in self.group_tuiles:
            self.screen.blit(tuile.image,tuile.rect)

    def getGroupeTuiles(self):
        return self.group_tuiles