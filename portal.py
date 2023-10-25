import pygame as pg

class Portal(pg.Rect):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texturePath = pg.image.load("specialTextures/portal.png").convert_alpha()