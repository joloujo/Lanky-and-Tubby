import pygame as pg
import threading
import math

pg.init()

running = True

screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
pg.display.set_caption("Lanky and Tubby")
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


move_keys_pressed = [0] * len(pg.key.get_pressed())

Tubby_max_vel = 10
Lanky_max_vel = 10


def move_thread_func():
    global move_keys_pressed
    if running:
        Tubby.move.posy += 1

        tubby_touching_ground = False
        tubby_hb = Tubby.move.posx + Tubby.move.hbx, Tubby.move.posy + Tubby.move.hby, Tubby.move.hbw, Tubby.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(tubby_hb, item_hb) and item.move != Tubby.move:
                tubby_touching_ground = True

        Tubby.move.posy -= 2

        tubby_touching_roof = False
        tubby_hb = Tubby.move.posx + Tubby.move.hbx, Tubby.move.posy + Tubby.move.hby, Tubby.move.hbw, Tubby.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(tubby_hb, item_hb) and item.move != Tubby.move:
                tubby_touching_roof = True

        Tubby.move.posy += 1

        Tubby.move.posx -= 1

        tubby_touching_lwall = False
        tubby_hb = Tubby.move.posx + Tubby.move.hbx, Tubby.move.posy + Tubby.move.hby, Tubby.move.hbw, Tubby.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(tubby_hb, item_hb) and item.move != Tubby.move:
                tubby_touching_lwall = True

        Tubby.move.posx += 2

        tubby_touching_rwall = False
        tubby_touching_roof = False
        tubby_hb = Tubby.move.posx + Tubby.move.hbx, Tubby.move.posy + Tubby.move.hby, Tubby.move.hbw, Tubby.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(tubby_hb, item_hb) and item.move != Tubby.move:
                tubby_touching_rwall = True

        Tubby.move.posx -= 1

        if tubby_touching_ground:
            if move_keys_pressed[keys["w"]] >= 1:
                Tubby.move.vely = -20
            else:
                Tubby.move.vely = 0

        if tubby_touching_roof and Tubby.move.vely < 0:
            Tubby.move.vely = 0

        if tubby_touching_lwall and Tubby.move.velx < 0 or tubby_touching_rwall and Tubby.move.velx > 0:
            Tubby.move.velx = 0

        if not tubby_touching_ground:
            Tubby.move.vely += 1

        if move_keys_pressed[keys["a"]] >= 1 and Tubby.move.velx > -1 * Tubby_max_vel:
            Tubby.move.velx -= 1
        elif move_keys_pressed[keys["d"]] >= 1 and Tubby.move.velx < Tubby_max_vel:
            Tubby.move.velx += 1
        else:
            if -1 * Tubby_max_vel <= Tubby.move.velx < 0:
                Tubby.move.velx += 1
            elif Tubby_max_vel >= Tubby.move.velx > 0:
                Tubby.move.velx -= 1

        if Tubby.move.vel() != (0, 0):
            if math.fabs(Tubby.move.velx) > math.fabs(Tubby.move.vely):
                if Tubby.move.velx > 0:
                    for x in range(0, Tubby.move.velx):
                        Tubby.move.update_pos(1, Tubby.move.vely / Tubby.move.velx)
                else:
                    for x in range(0, -1 * Tubby.move.velx):
                        Tubby.move.update_pos(-1, Tubby.move.vely / (-1 * Tubby.move.velx))
            else:
                if Tubby.move.vely > 0:
                    for y in range(0, Tubby.move.vely):
                        Tubby.move.update_pos(Tubby.move.velx / Tubby.move.vely, 1)
                else:
                    for y in range(0, -1 * Tubby.move.vely):
                        Tubby.move.update_pos(Tubby.move.velx / (-1 * Tubby.move.vely), -1)

        pass

        Lanky.move.posy += 1

        lanky_touching_ground = False
        lanky_hb = Lanky.move.posx + Lanky.move.hbx, Lanky.move.posy + Lanky.move.hby, Lanky.move.hbw, Lanky.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(lanky_hb, item_hb) and item.move != Lanky.move:
                lanky_touching_ground = True

        Lanky.move.posy -= 2

        lanky_touching_roof = False
        lanky_hb = Lanky.move.posx + Lanky.move.hbx, Lanky.move.posy + Lanky.move.hby, Lanky.move.hbw, Lanky.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(lanky_hb, item_hb) and item.move != Lanky.move:
                lanky_touching_roof = True

        Lanky.move.posy += 1

        Lanky.move.posx -= 1

        lanky_touching_lwall = False
        lanky_hb = Lanky.move.posx + Lanky.move.hbx, Lanky.move.posy + Lanky.move.hby, Lanky.move.hbw, Lanky.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(lanky_hb, item_hb) and item.move != Lanky.move:
                lanky_touching_lwall = True

        Lanky.move.posx += 2

        lanky_touching_rwall = False
        lanky_hb = Lanky.move.posx + Lanky.move.hbx, Lanky.move.posy + Lanky.move.hby, Lanky.move.hbw, Lanky.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(lanky_hb, item_hb) and item.move != Lanky.move:
                lanky_touching_rwall = True

        Lanky.move.posx -= 1

        if lanky_touching_ground:
            if move_keys_pressed[keys["w"]] >= 1:
                Lanky.move.vely = -20
            else:
                Lanky.move.vely = 0

        if lanky_touching_roof and Lanky.move.vely < 0:
            Lanky.move.vely = 0

        if lanky_touching_lwall and Lanky.move.velx < 0 or lanky_touching_rwall and Lanky.move.velx > 0:
            Lanky.move.velx = 0

        if not lanky_touching_ground:
            Lanky.move.vely += 1

        if move_keys_pressed[keys["a"]] >= 1 and Lanky.move.velx > -1 * Lanky_max_vel:
            Lanky.move.velx -= 1
        elif move_keys_pressed[keys["d"]] >= 1 and Lanky.move.velx < Lanky_max_vel:
            Lanky.move.velx += 1
        else:
            if -1 * Lanky_max_vel <= Lanky.move.velx < 0:
                Lanky.move.velx += 1
            elif Lanky_max_vel >= Lanky.move.velx > 0:
                Lanky.move.velx -= 1

        if Lanky.move.vel() != (0, 0):
            if math.fabs(Lanky.move.velx) > math.fabs(Lanky.move.vely):
                if Lanky.move.velx > 0:
                    for x in range(0, Lanky.move.velx):
                        Lanky.move.update_pos(1, Lanky.move.vely / Lanky.move.velx)
                else:
                    for x in range(0, -1 * Lanky.move.velx):
                        Lanky.move.update_pos(-1, Lanky.move.vely / (-1 * Lanky.move.velx))
            else:
                if Lanky.move.vely > 0:
                    for y in range(0, Lanky.move.vely):
                        Lanky.move.update_pos(Lanky.move.velx / Lanky.move.vely, 1)
                else:
                    for y in range(0, -1 * Lanky.move.vely):
                        Lanky.move.update_pos(Lanky.move.velx / (-1 * Lanky.move.vely), -1)

        move_keys_pressed = [0] * len(pg.key.get_pressed())

        move_thread = threading.Timer(1 / 100, move_thread_func)
        move_thread.start()


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


Tubby = Creature(10, (1000, 920), (0, 0), (0, 0, 90, 90))
Tubby.create_box(Tubby.move.hb(), (200, 0, 0))

Lanky = Creature(10, (450, 820), (0, 0), (0, 0, 90, 190))
Lanky.create_box(Lanky.move.hb(), (0, 200, 200))

pass

floor = Creature(1, (0, 1030), (0, 0), (0, 0, 1920, 50))
floor.create_box(floor.move.hb(), (0, 200, 0))

lwall = Creature(1, (-1, -1), (0, 0), (0, 0, 1, 1080))
lwall.create_box(lwall.move.hb(), (0, 0, 200))

rwall = Creature(1, (1920, -1), (0, 0), (0, 0, 1, 1080))
rwall.create_box(rwall.move.hb(), (0, 0, 200))

Roof = Creature(1, (-1, -1), (0, 0), (0, 0, 1922, 1))
Roof.create_box(Roof.move.hb(), (0, 0, 200))

pass

Wall1 = Creature(1, (610, 330), (0, 0), (0, 0, 100, 700))
Wall1.create_box(Wall1.move.hb(), (0, 0, 200))

lPlatform1 = Creature(1, (10, 830), (0, 0), (0, 0, 150, 25))
lPlatform1.create_box(lPlatform1.move.hb(), (0, 0, 200))

lPlatform2 = Creature(1, (360, 630), (0, 0), (0, 0, 150, 25))
lPlatform2.create_box(lPlatform2.move.hb(), (0, 0, 200))

lPlatform3 = Creature(1, (110, 430), (0, 0), (0, 0, 150, 25))
lPlatform3.create_box(lPlatform3.move.hb(), (0, 0, 200))

Wall2 = Creature(1, (1510, 430), (0, 0), (0, 0, 400, 600))
Wall2.create_box(Wall2.move.hb(), (0, 0, 200))
Wall2sub1 = Creature(1, (1410, 830), (0, 0), (0, 0, 100, 200))
Wall2sub1.create_box(Wall2sub1.move.hb(), (0, 0, 200))

rPlatform1 = Creature(1, (1050, 680), (0, 0), (0, 0, 100, 25))
rPlatform1.create_box(rPlatform1.move.hb(), (0, 0, 200))
rPlatform1sub1 = Creature(1, (1125, 655), (0, 0), (0, 0, 25, 25))
rPlatform1sub1.create_box(rPlatform1sub1.move.hb(), (0, 0, 200))

rPlatform2 = Creature(1, (850, 530), (0, 0), (0, 0, 100, 25))
rPlatform2.create_box(rPlatform2.move.hb(), (0, 0, 200))
rPlatform2sub1 = Creature(1, (925, 505), (0, 0), (0, 0, 25, 25))
rPlatform2sub1.create_box(rPlatform2sub1.move.hb(), (0, 0, 200))

# Platform3 = Creature(1, (0, 570), (0, 0), (0, 0, 200, 100))
# Platform3.create_box(Platform3.move.hb(), (0, 0, 200))

move_thread_func()

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

    pg.display.flip()

pg.quit()
quit()
