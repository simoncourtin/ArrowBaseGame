__author__ = 'Simon Courtin'
import pygame
import Tuile as _tuile
import os

class Calque():

    # Constructeur
    def __init__(self,screen,fichier,image,x_tile=32,y_tile=32,):
        #fenetre ou ajouter
        self.screen = screen

        #tilset de l'image du calque
        self.tilset = pygame.image.load(os.path.dirname(__file__)+"/"+image).convert_alpha()

        #hauteur et largeur des tuiles dans le tilset
        self.x_tile=x_tile
        self.y_tile=y_tile

        #tableau des spawn et des objets interactifs
        self.spawn = []
        #largeur de la map
        self.largeur_map = 0
        self.hauteur_map = 0

        #le fichier ou se situe le schema de la map
        self.fichier = os.path.dirname(__file__)+"/"+fichier

        #le groupe de tuiles
        self.group_tuiles = pygame.sprite.Group()

        self.creation_tableau_calque()
        self.construire_layer()

    # Lit les donnees du fichier contenant le schema de la map et les place dans un tableau
    def creation_tableau_calque(self):
        #Debut de le creation du calque
        #lecture du fichier
        self.f = open(self.fichier, "r")
        self.ligne = self.f.read()
        self.ligne = self.ligne.replace('\n','\n,')

        #generation du tableau pour les differents element du calque
        self.calque=[]
        self.calque= self.ligne.split(',')

    # Construit les tuiles de ce calque a partir du tableau contenant le schema de la map
    # cree dans la methode creation_tableau_calque()
    def construire_layer(self):
        hauteur = self.x_tile
        largeur = self.y_tile

        # Abscisse de la tuile sur l'ecran
        x=0
        # Ordonnee de la tuile sur l'ecran
        y=0

        for element in self.calque:
            if element != '\n':
                self.largeur_map += 1
                if element!="0":
                    # Calcul de la position de l'image de la tuile dans le fichier .png
                    X ,Y = self.calcul_position_tuile_tilset(element)

                    # Recuperation de l'image
                    tile = self.tilset.subsurface(X,Y,hauteur,largeur)

                    # Instanciation d'un objet tuile et ajout au groupe
                    tuile = _tuile.Tuile(tile, int(element),x,y)
                    self.group_tuiles.add(tuile)

                    # Cas de ...
                    if element == '256':
                        self.group_tuiles.remove(tuile)
                        self.spawn.append((x ,y))
                # On va vers la droite
                x+=largeur
            else:
                # Retour a la ligne
                y+=hauteur
                x=0
                self.hauteur_map += 1
                self.largeur_map = 0

    # Calcule la position d'un tuile dans le fichier contenant l'ensemble des tuiles
    def calcul_position_tuile_tilset(self,element):
        numero = int(element)

        #calul de la position x et y sur le tileset
        if numero % 16 == 0 and numero != 256:
            numero = numero - 16
        #end if

        #X = (  ( numero - (((numero-1)/16)*16) )-1  )*32
        X = ((numero-1)%16 )*32
        Y = (numero/16)*32
        if(Y==512):
            Y= 512-32
        return X,Y

    # Affiche ce calque partiellement ou non suivant la camera
    def afficher_calque_camera(self, cam):
        for tuile in self.group_tuiles:
            self.screen.blit(tuile.image,cam.apply(tuile))

    # Affiche ce calque en entier(pas de camera)
    def afficher_calque(self):
        for tuile in self.group_tuiles:
            self.screen.blit(tuile.image,tuile.rect)

    # Renvoie un objet de type pygame.sprite.Group contenant les tuiles de ce calque
    def getGroupeTuiles(self):
        return self.group_tuiles

    # Renvoie vrai si une tuile se trouve aux coordonnees (x,y) (centre de la tuile)
    def hasTuileAt(self, x, y):
        for tuile in self.group_tuiles:
            if tuile.rect.centerx == x and tuile.rect.centery == y:
                return True
            #end if
        #end for
        return False
    #end hasTuileAt