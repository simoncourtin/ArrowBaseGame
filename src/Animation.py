import load_png

DUREE_ANIMATION = 30
ANIME_PAR_DEFAUT = True

### Classe gerant une animation
class Animation:
    ### Constructeur : prend en parametre la liste d'image liee a cette animation
	def __init__(self, listeImages):
		self.images = listeImages
		self.nbImages = len(listeImages)
		self.compteur = 0
		self.derniereValeurCompteur = 0
		self.stopped = not ANIME_PAR_DEFAUT
	#end __init__

	### Arrete cette animation 
	def stopAnimation(self, clock):
		if not self.stopped:
			# Mise à jour des compteurs
			self.compteur = self.compteur + clock - self.derniereValeurCompteur
			self.derniereValeurCompteur = clock

			# Arret de l'animation 
			self.stopped = True
		#end if
	#end stopAnimation

	### Démarre ou redémarre cette animation
	def startAnimation(self, clock):
		if self.stopped:
			self.derniereValeurCompteur = clock		
			self.stopped = False
		#end if
	#end startAnimation	

	### Retourne l'image que cette animation doit afficher
	def getImage(self, clock):
		# Mise à jour des compteurs
		if not self.stopped:
			self.compteur = self.compteur + clock - self.derniereValeurCompteur
			self.derniereValeurCompteur = clock
		#end if

		# Récupération de l'image
		index = self.compteur%DUREE_ANIMATION
		index = index/(DUREE_ANIMATION/self.nbImages)

		return self.listeImages[index]
	#end getImage

	### Reset de l'animation : on revient à la première image
	def reset(self, clock):
		self.compteur = 0
		self.derniereValeurCompteur = clock
	#end reset
#end Animation