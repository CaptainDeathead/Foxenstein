import pygame as pg
import math
from settings import *

class caco(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 30
        self.angle = 0
        self.health = 1
        self.dead = False
        self.attacking = False
        self.timePerFrame = 0.1
        self.timeSinceLastFrame = 0
        self.frame = 0
        self.idle = pg.image.load("enemy/caco_demon/0.png").convert_alpha()
        self.attackAnims = []
        self.deathAnims = []

        for i in range(0, 4):
            self.attackAnims.append(pg.image.load("enemy/caco_demon/attack/" + str(i) + ".png").convert_alpha())

        for i in range(0, 5):
            self.deathAnims.append(pg.image.load("enemy/caco_demon/death/" + str(i) + ".png").convert_alpha())

        self.image = self.idle
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, dt, px, py, objects):
        if self.dead:
            self.timeSinceLastFrame += dt
            if self.timeSinceLastFrame >= self.timePerFrame:
                self.timeSinceLastFrame = 0
                self.frame += 1
                if self.frame >= len(self.deathAnims):
                    self.kill()
                else:
                    self.image = self.deathAnims[self.frame]
        elif self.attacking:
            self.timeSinceLastFrame += dt
            if self.timeSinceLastFrame >= self.timePerFrame:
                self.timeSinceLastFrame = 0
                self.frame += 1
                if self.frame >= len(self.attackAnims):
                    self.frame = 0
                    self.attacking = False
                    self.image = self.idle
                    xDist = abs(px - self.x)
                    yDist = abs(py - self.y)
                    dist = math.sqrt(xDist**2 + yDist**2)
                    return dist
                else:
                    self.image = self.attackAnims[self.frame]
        else:
            self.image = self.idle

        playerAngle = math.atan2(py - self.y, px - self.x)
        self.angle = playerAngle
        self.x += math.cos(playerAngle) * self.speed * dt
        self.y += math.sin(playerAngle) * self.speed * dt

        xDist = abs(px - self.x)
        yDist = abs(py - self.y)
        dist = math.sqrt(xDist**2 + yDist**2)
        
        if dist <= CACO_ATK_DIST:
            self.attacking = True

        for obj in objects:
            if self.x >= obj.x and self.x <= obj.x + obj.width and self.y >= obj.y and self.y <= obj.y + obj.height:
                self.x -= math.cos(playerAngle) * self.speed * dt
                self.y -= math.sin(playerAngle) * self.speed * dt
                break
        
        self.rect.center = (self.x, self.y)

        return 0

    def attack(self):
        self.attacking = True

    def die(self):
        self.dead = True

    def kill(self):
        super().kill()