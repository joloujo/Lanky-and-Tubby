import pygame as pg
from PIL import Image
import math
import time

running = True

background_darkness = 150

size = 220

char_sheet_PIL = Image.open("lanky_char_sheet.png")
animation_timer = 0
to_render = (0, 0, 100, 100)

char_sheet_PIL.thumbnail((size * 8, size * 5), Image.ANTIALIAS)
char_sheet_string = char_sheet_PIL.tobytes(), char_sheet_PIL.size, char_sheet_PIL.mode
char_sheet = pg.image.fromstring(char_sheet_PIL.tobytes(), char_sheet_PIL.size, char_sheet_PIL.mode)

screen = pg.display.set_mode((300, 300))

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    animation_timer += 1
    to_render = (math.fmod(animation_timer, 8) * size, size, size, size)

    screen.fill((background_darkness, background_darkness, background_darkness))

    pg.draw.rect(screen, (200, 0, 0), (120, 55, 55, 180))
    
    screen.blit(char_sheet, (40, 15), to_render)
    
    pg.display.flip()

    time.sleep(0.1)
