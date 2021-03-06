# coding: utf-8

import pygame

class Camera():

    def __init__(self, camera_func, width, height, mapWidth, mapHeight):
        #jeu

        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
    #end __init__

    def apply(self, target):
        return target.rect.move([-self.state.left,-self.state.top])
    #end apply

    def apply_rect(self, rect):
        return rect.move([-self.state.left,-self.state.top])
    #end apply_rect

    def update(self, target, screen):
        self.state = self.camera_func(self, target.rect, screen)
    #end update
#end Camera


def simple_camera(camera, target_rect, screen):
    HALF_WIDTH = screen.get_rect().width / 2
    HALF_HEIGHT = screen.get_rect().height / 2
    l, t, _, _ = target_rect # l = left,  t = top
    _, _, w, h = camera      # w = width, h = height
    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect, screen):
    HALF_WIDTH = screen.get_rect().width / 2
    HALF_HEIGHT = screen.get_rect().height / 2
    WIN_WIDTH = screen.get_rect().width
    WIN_HEIGHT = screen.get_rect().height
    l, t, _, _ = target_rect
    _, _, w, h = camera.state
    l, t, _, _ = l-HALF_WIDTH, t-HALF_HEIGHT, w, h # center player

    l = min(camera.mapWidth-camera.state.width, l)   # stop scrolling at the right edge
    l = max(0, l)                           # stop scrolling at the left edge
    t = min(camera.mapHeight-camera.state.height, t) # stop scrolling at the bottom
    t = max(0, t)                           # stop scrolling at the top
    """
    if camera.x+camera.width >= WIN_WIDTH:
        l = min(WIN_WIDTH-camera.width, l)
    else:

    """
    #print str(camera.mapWidth-camera.state.width)+";"+str(camera.mapHeight-camera.state.height)
    return pygame.Rect(l, t, w, h)
