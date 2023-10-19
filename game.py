import pygame as pg
from math import cos, sin, tan, pi
import time
from settings import *

pg.init()

dt = 1

debug = False

def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path)
    texture = pg.transform.scale(texture, res)
    return texture

def load_wall_textures():
    return {
        0: get_texture("textures/1.png"),
        1: get_texture("textures/2.png"),
        2: get_texture("textures/3.png")
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
        new_x = self.x + dx * dt * 32
        new_y = self.y + dy * dt * 32

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

        distanceMultiplier = 2

        for i in range(int(DISTANCE/distanceMultiplier)):
            for e, obj in enumerate(objects):
                if x > obj.x and x < obj.x + obj.width and y > obj.y and y < obj.y + obj.height:
                    if debug:
                        l = pg.draw.line(screen, (255, 255, 255), (ox, oy), (x, y))
                        pg.display.update(l)

                    return i *distanceMultiplier, (x, y), obj, e

            x += grad[0] *distanceMultiplier
            y += grad[1] *distanceMultiplier

        if debug:
            l = pg.draw.line(screen, (255, 255, 255), (ox, oy), (x, y))
            pg.display.update(l)

        return DISTANCE, (x, y), None, None

    def rayTrace(self, plainMap, objects) -> list:
        y_buff = []
        rayAngle = self.fov / self.num_rays # maybe a - 1 after num rays

        for i in range(int(self.num_rays + 1)):
            #print((i+1)*rayAngle)
            distance, endPoint, obj, index = self.drawRay((self.rot - self.fov / 2) + i * rayAngle, plainMap, objects)
            distance *= cos(self.rot - (self.rot - self.fov / 2) + (i) * rayAngle + pi/2)
            #print((self.rot - self.fov / 2) + (i+1) * rayAngle * 57.2957795 * 21.333333333333)
            y_buff.append((distance, endPoint, (self.rot - self.fov / 2) + i * rayAngle * 57.2957795 * 13.25, obj, index))

        return y_buff
    
def main(width, height, resolution_scale, fov, color_darken_scale):
    global dt
    global RECTS_ON_SCREEN
    global RAY_HITS
    global screen
    
    global WIDTH
    global HEIGHT
    global RESOLUTION_SCALE
    global FOV
    global COLOR_DARKEN_SCALE

    WIDTH = width
    HEIGHT = height
    RESOLUTION_SCALE = resolution_scale
    FOV = fov
    COLOR_DARKEN_SCALE = color_darken_scale

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Foxenstine")

    plainMap = []
    #objects = [pg.rect.Rect(200, 200, 100, 100), pg.rect.Rect(400, 600, 100, 25)]
    player = Player(600, 300, 3.14159265, int(WIDTH)/RESOLUTION_SCALE)
    lastSwitch = time.time()
    lastDt = time.time()

    clock = pg.time.Clock()
    running = True
    while running:
        clock.tick(60)
        pg.display.set_caption("Foxenstine!!!    |    FPS: " + str(int(clock.get_fps())) + "    Delta time: " + str(round(dt, 2)) + "    Resolution Scale: " + str(RESOLUTION_SCALE) + "    Resolution: " + str(WIDTH) + "x" + str(HEIGHT) + "    FOV: " + str(FOV) + "    Ray Hits: " + str(int(RAY_HITS)) + "%" + "    Color darken scale: " + str(COLOR_DARKEN_SCALE))
        screen.fill((0,0,0))

        dt = time.time() - lastDt
        lastDt = time.time()

        pg.draw.rect(screen, (0, 100, 255), (0, 0, WIDTH, HEIGHT/2))
        pg.draw.rect(screen, (140, 100, 0), (0, HEIGHT/2, WIDTH, HEIGHT))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False

        if running == False:
            break

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
            player.rot -= player.rot_speed * dt * 32
        if keys[pg.K_RIGHT]:
            player.rot += player.rot_speed * dt * 32

        if player.rot > pi*2:
            player.rot = 0
        elif player.rot < -(pi*2):
            player.rot = 0

        if keys[pg.K_SPACE] and lastSwitch < time.time() - 0.5:
            global debug
            debug = not debug
            lastSwitch = time.time()

        if debug:
            for obj in objects:
                pg.draw.rect(screen, (255, 255, 255), obj)

        y_buff = player.rayTrace(plainMap, objects)

        if debug == False:
            if len(y_buff) > 0:
                RECTS_ON_SCREEN = 0

            lastObj = 99999999999
            x_clip_start = 0

            for y in y_buff:
                if y[4] == None:
                    continue
                #if player.y + y[0] < HEIGHT:
                #    color = min(255, abs(255 / ((y[0] + 0.01) / 100)))
                #    l = pg.draw.line(screen, (color, color, color), (y[2], HEIGHT-min(HEIGHT/2, y[0])), (y[2], 0), RESOLUTION_SCALE)
                #    pg.display.update(l)

                # define all y values
                # y[0] = distance
                # y[1] = endpoint
                # y[2] = angle
                # y[3] = object
                # y[4] = object index

                proj_height = abs((SCREEN_DIST / (y[0] + 0.01)) * 100)

                color = min(255, abs(255 / ((y[0] + 0.01) / COLOR_DARKEN_SCALE)))
                #pg.draw.line(screen, (color, color, color), (y[2], HEIGHT/2 - proj_height/2), (y[2], HEIGHT/2 + proj_height/2), RESOLUTION_SCALE)
                #pg.draw.rect(screen, (color, color, color), (y[2], HEIGHT/2 + proj_height/2, RESOLUTION_SCALE, abs(proj_height)))

                # draw textures
                texture = textures[objectTypes[y[4]]]

                # clip texture x to resolution scale
                #texture = texture.subsurface((int(y[0] * 0.1) % TEXTURE_SIZE, 0, 1, TEXTURE_SIZE))

                if lastObj != y[4] or x_clip_start > texture.get_width():
                    x_clip_start = 0
                else:
                    texture = texture.subsurface((x_clip_start, 0, 1, TEXTURE_SIZE))
                    x_clip_start += RESOLUTION_SCALE

                texture = pg.transform.scale(texture, (RESOLUTION_SCALE, int(proj_height)))

                # change texture color based on distance
                texture.fill((color, color, color), special_flags=pg.BLEND_MULT)

                screen.blit(texture, (y[2] + (WIDTH/2 - player.x) % RESOLUTION_SCALE // 32, HEIGHT/2 - proj_height/2))

                lastObj = y[4]

                RECTS_ON_SCREEN += 1

        RAY_HITS = RECTS_ON_SCREEN / (1200 / RESOLUTION_SCALE + 1) * 100

        pg.display.flip()

if __name__ == "__main__":
    main()