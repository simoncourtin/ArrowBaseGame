__author__ = 'Simon Courtin'

import Calque, CalqueImage
import os

class Map():
    # Constructeur
    def __init__(self,screen,config_file,information_claque):
        self.spawn = []
        self.calques = []
        #tableau sous forme [(schema sur la map, tilset ,calque de collision, calque d'objet, taille x des tiles ,taille y des tiles),(...)]
        self.futureCalques = information_claque
        self.screen =screen
        self.largeur_map = 0
        self.hauteur_map =0
        self.tile_width = 0
        #recuperation des configs
        self.mapConfiguration(config_file)
        #construction de la carte
        self.buildLayerOnMap()

    # Creation des differents calques
    def buildLayerOnMap(self):
        for calque_elem in self.futureCalques:
            if calque_elem[0]=='':
                calque = Calque.Calque(self.screen,calque_elem[1],calque_elem[2],calque_elem[3],calque_elem[4])
                if len(calque.spawn)>0:
                    self.spawn = calque.spawn
            elif calque_elem[0]=="Image":
                calque = CalqueImage.CalqueImage(self.screen,calque_elem[1],calque_elem[2])
            self.calques.append(calque)


    def mapConfiguration(self,config_file):
        #fichier de config de la carte
        s= open(os.path.dirname(__file__)+config_file,"r")
        #on parcours le fichier
        with open (os.path.dirname(__file__)+config_file, "r") as file:
            #lecture ligne par ligne
            line=file.readline()
            if line.strip("=")[0]=="width":
                #largeur de la map
                self.largeur_map = line.split('=')[1]
            elif line.strip("=")[0]=="height":
                #hauteur de la map
                self.hauteur_map = line.split('=')[1]
            elif line.strip("=")[0]=="tileheight":
                #hauteur de la map
                self.tile_width = line.split('=')[1]

    #avec une camera
    def afficherCarteCamera(self, camera):
        for calque in self.calques:
            calque.afficher_calque_camera(camera)

    def afficherRangCalqueCamera(self,debut,fin,camera):
        for i in range(debut-1,fin-1):
            self.afficherCalque(i,camera)

    def afficherCalqueCamera(self,indice,camera):
        self.calques[indice-1].afficher_calque_camera(camera)

    #sans camera
    def afficherCarte(self):
        for calque in self.calques:
            calque.afficher_calque()

    def afficherRangCalque(self,debut,fin):
        for i in range(debut,fin):
            self.afficherCalque(i)

    def afficherCalque(self,indice):
        self.calques[indice].afficher_calque()

    def getSpawn(self):
        return self.spawn

    def getCalqueIndice(self,indice):
        return self.calques[indice]




