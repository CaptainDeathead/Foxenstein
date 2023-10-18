import pygame as pg
from math import cos, sin, tan, pi
import time

pg.init()

WIDTH = 1200
HEIGHT = 800
RESOLUTION_SCALE = 12
DISTANCE = 1000
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FOV = 1.57079632679 # 90 degrees
HALF_FOV = FOV / 2

SCREEN_DIST = HALF_WIDTH / tan(HALF_FOV)

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Foxenstine")

debug = False

def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path)
    texture = pg.transform.scale(texture, res)
    return texture

def load_wall_textures():
    return {
        0: get_texture("textures/red_brick_wall.png"),
        1: get_texture("textures/grey_brick_wall.png"),
        2: get_texture("textures/moss_grey_brick_wall.png")
    }

objects = [pg.rect.Rect(0, 0, WIDTH, 100), pg.rect.Rect(WIDTH-100, 0, 100, HEIGHT), pg.rect.Rect(0, HEIGHT-100, WIDTH, 100), pg.rect.Rect(0, 0, 100, HEIGHT), pg.rect.Rect(200, 200, 100, 100), pg.rect.Rect(400, 600, 100, 25)]
objectTypes = [0, 0, 0, 0, 1, 1]

textures = load_wall_textures()

class Player:
    def __init__(self, x, y, rot, num_rays):
        self.x = x
        self.y = y
        self.rot = rot
        self.num_rays = num_rays
        self.fov = FOV
        self.move_speed = 5
        self.rot_speed = 0.05

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position is within the screen boundaries or doesn't collide with objects.
        if 0 < new_x < WIDTH and 0 < new_y < HEIGHT and not self.checkCollision(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def checkCollision(self, x, y):
        for obj in objects:
            if x > obj.x and x < obj.x + obj.width and y > obj.y and y < obj.y + obj.height:
                return True

    def drawRay(self, angle, plainMap, objects) -> int:
        x = int(self.x)
        y = int(self.y)

        ox = x
        oy = y

        grad = (cos(angle), sin(angle))

        for i in range(DISTANCE):
            for obj in objects:
                if x > obj.x and x < obj.x + obj.width and y > obj.y and y < obj.y + obj.height:
                    if debug:
                        l = pg.draw.line(screen, (255, 255, 255), (ox, oy), (x, y))
                        pg.display.update(l)

                    return i, (x, y)
                
            x += grad[0]
            y += grad[1]

        if debug:
            l = pg.draw.line(screen, (255, 255, 255), (ox, oy), (x, y))
            pg.display.update(l)
            
        return DISTANCE, (x, y)

    def rayTrace(self, plainMap, objects) -> list:
        y_buff = []
        rayAngle = self.fov / self.num_rays # maybe a - 1 after num rays
        # offset ray angle by half fov

        for i in range(int(self.num_rays)):
            #print((i+1)*rayAngle)
            distance, endPoint = self.drawRay((self.rot - self.fov / 2) + (i+1) * rayAngle, plainMap, objects)
            distance *= cos(self.rot - (self.rot - self.fov / 2) + (i+1) * rayAngle + pi/2)
            #print((self.rot - self.fov / 2) + (i+1) * rayAngle * 57.2957795 * 21.333333333333)
            y_buff.append((distance, endPoint, (self.rot - self.fov / 2) + (i+1) * rayAngle * 57.2957795 * 13.3 - 180))

        return y_buff

def main():
    plainMap = []
    #objects = [pg.rect.Rect(200, 200, 100, 100), pg.rect.Rect(400, 600, 100, 25)]
    player = Player(600, 300, 180, int(WIDTH)/RESOLUTION_SCALE)
    lastSwitch = time.time()

    clock = pg.time.Clock()
    while True:
        clock.tick(60)
        pg.display.set_caption("Foxenstine!!! FPS: " + str(int(clock.get_fps())))
        screen.fill((0,0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        keys=pg.key.get_pressed()

        dx, dy = 0, 0

        if keys[pg.K_w]:
            dx = player.move_speed * cos(player.rot)
            dy = player.move_speed * sin(player.rot)
        if keys[pg.K_s]:
            dx = -player.move_speed * cos(player.rot)
            dy = -player.move_speed * sin(player.rot)
        if keys[pg.K_a]:
            dx = player.move_speed * cos(player.rot - pi/2)
            dy = player.move_speed * sin(player.rot - pi/2)
        if keys[pg.K_d]:
            dx = player.move_speed * cos(player.rot + pi/2)
            dy = player.move_speed * sin(player.rot + pi/2)

        player.move(dx, dy)

        if keys[pg.K_LEFT]:
            player.rot -= 0.05
        if keys[pg.K_RIGHT]:
            player.rot += 0.05

        if keys[pg.K_SPACE] and lastSwitch < time.time() - 0.5:
            global debug
            debug = not debug
            lastSwitch = time.time()

        if debug:
            for obj in objects:
                pg.draw.rect(screen, (255, 255, 255), obj)

        y_buff = player.rayTrace(plainMap, objects)

        if debug == False:
            for y in y_buff:
                #if player.y + y[0] < HEIGHT:
                #    color = min(255, abs(255 / ((y[0] + 0.01) / 100)))
                #    l = pg.draw.line(screen, (color, color, color), (y[2], HEIGHT-min(HEIGHT/2, y[0])), (y[2], 0), RESOLUTION_SCALE)
                #    pg.display.update(l)

                # define all y values
                # y[0] = distance
                # y[1] = endpoint
                # y[2] = angle

                proj_height = (SCREEN_DIST / (y[0] + 0.01)) * 100

                color = min(255, abs(255 / ((y[0] + 0.01) / 100)))
                #pg.draw.line(screen, (color, color, color), (y[2], HEIGHT/2 - proj_height/2), (y[2], HEIGHT/2 + proj_height/2), RESOLUTION_SCALE)
                pg.draw.rect(screen, (color, color, color), (y[2], HEIGHT/2 + proj_height/2, RESOLUTION_SCALE, abs(proj_height)))

        pg.display.flip()

main()