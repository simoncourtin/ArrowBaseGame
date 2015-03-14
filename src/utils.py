import os
import pygame

### Chargement d'un fichier image ###
def load_png(name):
    """Load image and return image object"""
    fullname=os.path.join('.',name)
    try:
        image=pygame.image.load(fullname)
        if image.get_alpha is None:
            image=image.convert()
        else:
            image=image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image,image.get_rect()
#end load_png

def removekey(d, key):
        r = dict(d)
        del r[key]
        return r
