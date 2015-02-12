__author__ = 'Simon'
import pygame
import utils
import os
import Animable

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

class Personnage(Animable.Animable):
    def __init__(self, imageFolder):
        pygame.sprite.Sprite.__init__(self)
        Animable.Animable.__init__(self, cooldown=6)
        self.imageFolder = imageFolder
        self.image = utils.load_png(self.imageFolder+"/base.png")
        self.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        self.speed = [0,0]

	def debout(self):
		self.image = utils.load_png(self.imageFolder+"/base.png")

	def sauter(self):
		self.image = utils.load_png(self.imageFolder+"/saut.png")

	def down(self):
		self.image = utils.load_png(self.imageFolder+"/accroupi.png")
		#end down

	def left(self):
		self.image = utils.load_png(self.imageFolder+"/gauche.png")
		self.speed[0]=-5
	#end left

    def right(self):
        self.image = utils.load_png(self.imageFolder+"/droite.png")
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