import pygame as pg
from math import cos, sin, tan, pi
import time

pg.init()

WIDTH = 1200
HEIGHT = 800
RESOLUTION_SCALE = 12
MAX_DEPTH = 20
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

plainMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1]
    ]

textures = load_wall_textures()

class Player:
    def __init__(self, x, y, rot, num_rays):
        self.x = x
        self.y = y
        self.rot = rot
        self.num_rays = int(num_rays)
        self.fov = FOV
        self.move_speed = 5
        self.rot_speed = 0.05

    def map_pos(self):
        return int(self.x // 100), int(self.y // 100)

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position is within the screen boundaries or doesn't collide with objects.
        if 0 < new_x < WIDTH and 0 < new_y < HEIGHT and not self.checkWallCollision(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def checkWallCollision(self, x, y):
        if plainMap[int(y) // 100][int(x) // 100] == 0:
            return True
        else:
            return False

    def rayTrace(self, plainMap) -> list:
        ox, oy = self.x, self.y
        map_x, map_y = self.map_pos()

        ray_angle = self.rot - HALF_FOV + 0.0001
        for ray in range(self.num_rays):
            sin_a = sin(ray_angle)
            cos_a = cos(ray_angle)

            # horizontals
            y_hor, dy = (map_x + 1, 1) if sin_a >= 0 else (map_x - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor // 100), int(y_hor // 100)
                if tile_hor in plainMap:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth
             
            # verticals
            x_vert, dx = (map_x + 1, 1) if cos_a >= 0 else (map_x - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert // 100), int(y_vert // 100)
                if tile_vert in plainMap:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            pg.draw.line(screen, (255, 255, 255), (ox, oy), (x_hor, y_hor))

            ray_angle += self.fov / self.num_rays

def main():
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
            for y in range(len(plainMap)):
                for x in range(len(plainMap[y])):
                    if plainMap[y][x] == 1:
                        pg.draw.rect(screen, (255, 255, 255), (x*100, y*100, 100, 100))
                    elif plainMap[y][x] == 2:
                        pg.draw.rect(screen, (0, 255, 0), (x*100, y*100, 100, 100))

        y_buff = player.rayTrace(plainMap)

        if debug == False and 1==2:
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