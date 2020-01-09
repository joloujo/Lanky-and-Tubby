import pygame as pg
import math
from threading import Timer
pg.init()

Clock = pg.time.Clock()

loop_num = 0
loop_trump = 0

screen_scale = 0.5

screen = pg.display.set_mode((round(1920 * screen_scale), round(1080 * screen_scale)))
pg.display.set_caption("Sprite Test")
screen.fill((100, 100, 100))
pg.display.flip()

pg.event.get()
key_states = [0] * len(pg.key.get_pressed())


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class Sprite:
    def __init__(self, image, x_sprites, y_sprites, scale=0.0):
        self.sheet = pg.image.load(image)
        self.size = [self.sheet.get_rect()[2], self.sheet.get_rect()[3]]
        self.sheet = pg.transform.scale(self.sheet, (round(self.size[0] * scale), round(self.size[1] * scale)))
        self.size = [self.sheet.get_rect()[2], self.sheet.get_rect()[3]]
        self.x_sprites = x_sprites
        self.y_sprites = y_sprites
        self.tile_x = self.size[0] / self.x_sprites
        self.tile_y = self.size[1] / self.y_sprites
        self.ctile_x = math.fmod(0, self.x_sprites)
        self.ctile_y = math.floor(0 / self.x_sprites)

    def tile(self, sprite_num):
        self.ctile_x = math.fmod(sprite_num, self.x_sprites)
        self.ctile_y = math.floor(sprite_num / self.x_sprites)
        return (self.ctile_x * self.tile_x, self.ctile_y * self.tile_y, self.tile_x, self.tile_y)



player = Sprite("Sprite Sheet Test.png", 6, 4, screen_scale)
player2 = Sprite("Donald Trump Sprite Sheet.png", 6, 4, screen_scale)


def update_display():
    global loop_num
    screen.fill((100, 100, 100))
    screen.blit(player.sheet, (0, 0), player.tile(math.fmod(loop_num, 23)))
    loop_num += 1
    pg.display.flip()

def update_trump():
    global loop_trump
    screen.blit(player2.sheet, (100, 0), player.tile(math.fmod(loop_trump, 23)))
    loop_trump += 1
    pg.display.flip()

def hello():
    print("Hello")


screen_update = RepeatedTimer(1/24, update_display)
#trump_update = RepeatedTimer(1/24, update_trump)


running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    for key_id in range(0, len(pg.key.get_pressed())):
        if pg.key.get_pressed()[key_id] == 1:
            key_states[key_id] += 1
        else:
            key_states[key_id] = 0



    Clock.tick()

pg.quit()
screen_update.stop()
trump_update.stop()
quit()
