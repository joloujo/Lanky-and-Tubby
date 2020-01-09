import pygame as pg
import threading
import math
from PIL import Image
pg.init()

running = True

Clock = pg.time.Clock()

screen_scale = 1

if screen_scale == 1:
    screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
else:
    screen = pg.display.set_mode((round(screen_scale * 1920), round(screen_scale * 1080)))
pg.display.set_caption("Mech Test")
screen.fill((100, 100, 100))
pg.display.flip()

pg.event.get()
key_states = [0] * len(pg.key.get_pressed())
keys = {
    "esc": 27, "w": 119, "a": 97, "s": 115, "d": 100
}

all_creatures = []


def touching(rect_1, rect_2):
    touching_x = rect_2[0] < rect_1[0] + rect_1[2] and rect_1[0] < rect_2[0] + rect_2[2]
    touching_y = rect_2[1] < rect_1[1] + rect_1[3] and rect_1[1] < rect_2[1] + rect_2[3]
    if touching_x and touching_y:
        return True
    return False


class Movement:
    def __init__(self, refresh_rate, position=(0, 0), velocity=(0, 0), hitbox=(0, 0, 0, 0)):
        self.rr = refresh_rate
        self.posx = position[0]
        self.posy = position[1]
        self.velx = velocity[0]
        self.vely = velocity[1]
        self.hbx = hitbox[0]
        self.hby = hitbox[1]
        self.hbw = hitbox[2]
        self.hbh = hitbox[3]

    def pos(self):
        return self.posx, self.posy

    def vel(self):
        return self.velx, self.vely

    def hb(self):
        return self.hbx, self.hby, self.hbw, self.hbh

    def update_pos(self, move_x, move_y):
        self.posx += move_x
        self_hb = self.posx + self.hbx, self.posy + self.hby, self.hbw, self.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(self_hb, item_hb) and item.move != self:
                self.posx -= move_x
        self.posy += move_y
        self_hb = self.posx + self.hbx, self.posy + self.hby, self.hbw, self.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(self_hb, item_hb) and item.move != self:
                self.posy -= move_y

    """
    def update_pos(self):
        self_hb = self.posx + self.hbx, self.posy + self.hby, self.hbw, self.hbh
        if round(math.fabs(self.velx)) >= round(math.fabs(self.vely)):
            for x in range(0, round(math.fabs(self.velx))):
                self.posy += self.vely / self.velx
                self.posx += round(math.fabs(self.velx) / self.velx)
                for item in all_creatures:
                    item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
                    if touching(self_hb, item_hb) and item.move != self:
                        self.posy -= self.vely / self.velx
                        self.posx -= round(math.fabs(self.velx) / self.velx)
                        return
                        
                        
                        
                        
        else:
            for y in range(0, round(math.fabs(self.vely))):
                self.posx += self.velx/self.vely
                self.posy += round(math.fabs(self.vely) / self.vely)
                for item in all_creatures:
                    item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
                    if touching(self_hb, item_hb) and item.move != self:
                        self.posx -= self.velx / self.vely
                        self.posy -= round(math.fabs(self.vely) / self.vely)
                        return
    """


move_keys_pressed = [0] * len(pg.key.get_pressed())

Tubby_max_vel = 10

move_loop_speed = 1


def move_thread_func():
    global move_keys_pressed
    global touching_ground
    if running:
        Tubby.move.posy += 1
        touching_ground = False
        Tubby_hb = Tubby.move.posx + Tubby.move.hbx, Tubby.move.posy + Tubby.move.hby, Tubby.move.hbw, Tubby.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(Tubby_hb, item_hb) and item.move != Tubby.move:
                touching_ground = True
        Tubby.move.posy -= 1
        if move_keys_pressed[keys["w"]] >= 1 and Tubby.move.vely > -1 * Tubby_max_vel and touching_ground:
            Tubby.move.vely = -20
        # elif move_keys_pressed[keys["s"]] >= 1 and Tubby.move.vely < Tubby_max_vel:
            # pass
            # Tubby.move.vely += 1
        if not touching_ground:
            Tubby.move.vely += 1
            """
            if -1 * Tubby_max_vel <= Tubby.move.vely < 0:
                Tubby.move.vely += 1
            elif Tubby_max_vel >= Tubby.move.vely > 0:
                Tubby.move.vely -= 1
            """

        if move_keys_pressed[keys["a"]] >= 1 and Tubby.move.velx > -1 * Tubby_max_vel:
            Tubby.move.velx -= 1
        elif move_keys_pressed[keys["d"]] >= 1 and Tubby.move.velx < Tubby_max_vel:
            Tubby.move.velx += 1
        else:
            if -1 * Tubby_max_vel <= Tubby.move.velx < 0:
                Tubby.move.velx += 1
            elif Tubby_max_vel >= Tubby.move.velx > 0:
                Tubby.move.velx -= 1

        """
        if round(math.fabs(Tubby.move.velx)) >= round(math.fabs(Tubby.move.vely)):
            for x in range(0, round(math.fabs(Tubby.move.velx))):
                x_movement = round(math.fabs(Tubby.move.velx) / Tubby.move.velx)
                y_movement = Tubby.move.vely/Tubby.move.velx
                Tubby.move.update_pos(x_movement, y_movement)

        else:
            for y in range(0, round(math.fabs(Tubby.move.vely))):
                Tubby.move.update_pos(Tubby.move.velx/Tubby.move.vely, 1)
                
        """

        if Tubby.move.vel() != (0, 0):
            if math.fabs(Tubby.move.velx) > math.fabs(Tubby.move.vely):
                if Tubby.move.velx > 0:
                    for x in range(0, Tubby.move.velx):
                        Tubby.move.update_pos(1, Tubby.move.vely/Tubby.move.velx)
                else:
                    for x in range(0, -1 * Tubby.move.velx):
                        Tubby.move.update_pos(-1, Tubby.move.vely/(-1 * Tubby.move.velx))
            else:
                if Tubby.move.vely > 0:
                    for y in range(0, Tubby.move.vely):
                        Tubby.move.update_pos(Tubby.move.velx/Tubby.move.vely, 1)
                else:
                    for y in range(0, -1 * Tubby.move.vely):
                        Tubby.move.update_pos(Tubby.move.velx/(-1 * Tubby.move.vely), -1)

        move_keys_pressed = [0] * len(pg.key.get_pressed())

        move_thread = threading.Timer(1/100, move_thread_func)
        move_thread.start()


class Animation:
    def __init__(self, file, size, table):
        self.file = file
        self.w = size[0]
        self.h = size[1]
        self.tx = table[0]
        self.ty = table[1]
        self.loop = 0


def animation_thread_function():
    if Tubby.animations["walk"].loop <= 7 and key_states[keys["d"]] >= 1:
        Tubby.animations["walk"].loop += 1
    if Tubby.animations['walk'].loop > 7:
        Tubby.animations["walk"].loop = 0
    # if touching_ground:
    #     Tubby.animations["jump"].loop = 0
    animation_thread = threading.Timer(1/8, animation_thread_function)
    animation_thread.start()


class Box:
    def __init__(self, rect, color):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.color = color

    def rect(self):
        return self.x, self.y, self.w, self.h


class Creature:
    def __init__(self, m_refresh_rate, m_position=(0, 0), m_velocity=(0, 0), m_hitbox=(0, 0, 0, 0)):
        self.move = Movement(m_refresh_rate, m_position, m_velocity, m_hitbox)
        all_creatures.append(self)
        self.box = None
        self.animations = {}

    def create_box(self, b_rect, b_color):
        self.box = Box(b_rect, b_color)

    def create_animation(self, name, file, size, table):
        self.animations[name] = Animation(file, size, table)


Tubby = Creature(10, (500, 300), (0, 0), (0, 0, 100, 100))
Tubby.create_box((10, 10, 10, 10), (200, 0, 0))
tubby_charsheet = Image.open("test_character_sheet_tubby.png")
tubby_charsheet.thumbnail((800, 300), Image.ANTIALIAS)
tubby_charsheet_pg = pg.image.fromstring(tubby_charsheet.tobytes(), tubby_charsheet.size, tubby_charsheet.mode)

Tubby.create_animation("idle", tubby_charsheet_pg, (100, 100), (8, 3))
Tubby.create_animation("walk", tubby_charsheet_pg, (100, 100), (8, 3))
Tubby.create_animation("jump", tubby_charsheet_pg, (100, 100), (6, 3))

Platform1 = Creature(1, (200, 770), (0, 0), (0, 0, 300, 100))
Platform1.create_box(Platform1.move.hb(), (0, 0, 200))

Platform2 = Creature(1, (10, 970), (0, 0), (0, 0, 1900, 100))
Platform2.create_box(Platform2.move.hb(), (0, 200, 0))

Platform3 = Creature(1, (0, 570), (0, 0), (0, 0, 200, 100))
Platform3.create_box(Platform3.move.hb(), (0, 0, 200))


"""
rect1 = (0, 0, 10, 10)

rect2 = (10, 0, 10, 10)

rect3 = (15, 5, 10, 10)

print(touching(rect1, rect2))
print(touching(rect2, rect3))
print(touching(rect1, rect3))
"""

move_thread_func()
animation_thread_function()

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    for key_id in range(0, len(pg.key.get_pressed())):
        if pg.key.get_pressed()[key_id] == 1:
            key_states[key_id] += 1
            move_keys_pressed[key_id] = 1
        else:
            key_states[key_id] = 0

    if key_states[keys["esc"]] >= 1:
        running = False

    screen.fill((100, 100, 100))

    for creature in all_creatures:
        creature_x = creature.move.posx + creature.box.x
        creature_y = creature.move.posy + creature.box.y
        pg.draw.rect(screen, creature.box.color, (creature_x, creature_y, creature.box.w, creature.box.h))

    Tubby_x = Tubby.move.posx + Tubby.move.hbx
    Tubby_y = Tubby.move.posy + Tubby.move.hby
    Tubby_anim_x = Tubby.animations["walk"].w * Tubby.animations["walk"].loop
    Tubby_anim_y = 000

    screen.blit(Tubby.animations["walk"].file, (Tubby_x, Tubby_y), (Tubby_anim_x, Tubby_anim_y, Tubby.animations["walk"].w, Tubby.animations["walk"].h))

    pg.display.flip()

    Clock.tick()

pg.quit()
quit()
