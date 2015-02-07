__author__ = 'Simon Courtin'

import Calque, CalqueImage
class Map():

    def __init__(self,screen,information_claque):
        self.spawn = []
        self.calques = []
        #tableau sous forme [(schema sur la map, tilset ,calque de collision, calque d'objet, taille x des tiles ,taille y des tiles),(...)]
        self.futureCalques = information_claque
        self.screen =screen

        self.buildLayerOnMap()

    def buildLayerOnMap(self):
        for calque_elem in self.futureCalques:
            if calque_elem[0]=='':
                calque = Calque.Calque(self.screen,calque_elem[1],calque_elem[2],calque_elem[3],calque_elem[4])
                if len(calque.spawn)>0:
                    self.spawn = calque.spawn
            elif calque_elem[0]=="Image":
                calque = CalqueImage.CalqueImage(self.screen,calque_elem[1],calque_elem[2])
            self.calques.append(calque)


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


"""
carte = Map(screen,[("../maps/cobblestone2/background.txt",'../maps/cobblestone2/cobblestone.png',False,False,32,32),
            ("../maps/cobblestone2/collision.txt",'../maps/cobblestone2/cobblestone.png',True,False,32,32),
            ("../maps/cobblestone2/spawn.txt",'../maps/cobblestone2/cobblestone.png',False,False,32,32),
            ("../maps/cobblestone2/piece.txt",'../maps/cobblestone2/piece_tile.png',False,True,32,32)])
print carte.spawn
"""



