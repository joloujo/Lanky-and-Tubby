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
all_platforms = []


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
                pass
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(self_hb, item_hb):
                self.posx -= move_x
                pass
        self.posy += move_y
        self_hb = self.posx + self.hbx, self.posy + self.hby, self.hbw, self.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(self_hb, item_hb) and item.move != self:
                self.posy -= move_y
                pass
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(self_hb, item_hb):
                self.posy -= move_y
                pass


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
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(tubby_hb, item_hb):
                tubby_touching_ground = True

        Tubby.move.posy -= 2

        tubby_touching_roof = False
        tubby_hb = Tubby.move.posx + Tubby.move.hbx, Tubby.move.posy + Tubby.move.hby, Tubby.move.hbw, Tubby.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(tubby_hb, item_hb) and item.move != Tubby.move:
                tubby_touching_roof = True
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(tubby_hb, item_hb):
                tubby_touching_roof = True

        Tubby.move.posy += 1

        Tubby.move.posx -= 1

        tubby_touching_lwall = False
        tubby_hb = Tubby.move.posx + Tubby.move.hbx, Tubby.move.posy + Tubby.move.hby, Tubby.move.hbw, Tubby.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(tubby_hb, item_hb) and item.move != Tubby.move:
                tubby_touching_lwall = True
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(tubby_hb, item_hb):
                tubby_touching_lwall = True

        Tubby.move.posx += 2

        tubby_touching_rwall = False
        tubby_hb = Tubby.move.posx + Tubby.move.hbx, Tubby.move.posy + Tubby.move.hby, Tubby.move.hbw, Tubby.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(tubby_hb, item_hb) and item.move != Tubby.move:
                tubby_touching_rwall = True
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(tubby_hb, item_hb):
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

        """     TO DO:
        Fix gap between platforms and players that is caused by float positions
        """

#        Tubby.move.posx = round(Tubby.move.posx)
#        Tubby.move.posy = round(Tubby.move.posy)

        pass

        Lanky.move.posy += 1

        lanky_touching_ground = False
        lanky_hb = Lanky.move.posx + Lanky.move.hbx, Lanky.move.posy + Lanky.move.hby, Lanky.move.hbw, Lanky.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(lanky_hb, item_hb) and item.move != Lanky.move:
                lanky_touching_ground = True
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(lanky_hb, item_hb):
                lanky_touching_ground = True

        Lanky.move.posy -= 2

        lanky_touching_roof = False
        lanky_hb = Lanky.move.posx + Lanky.move.hbx, Lanky.move.posy + Lanky.move.hby, Lanky.move.hbw, Lanky.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(lanky_hb, item_hb) and item.move != Lanky.move:
                lanky_touching_roof = True
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(lanky_hb, item_hb):
                lanky_touching_roof = True

        Lanky.move.posy += 1

        Lanky.move.posx -= 1

        lanky_touching_lwall = False
        lanky_hb = Lanky.move.posx + Lanky.move.hbx, Lanky.move.posy + Lanky.move.hby, Lanky.move.hbw, Lanky.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(lanky_hb, item_hb) and item.move != Lanky.move:
                lanky_touching_lwall = True
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(lanky_hb, item_hb):
                lanky_touching_lwall = True

        Lanky.move.posx += 2

        lanky_touching_rwall = False
        lanky_hb = Lanky.move.posx + Lanky.move.hbx, Lanky.move.posy + Lanky.move.hby, Lanky.move.hbw, Lanky.move.hbh
        for item in all_creatures:
            item_hb = item.move.posx + item.move.hbx, item.move.posy + item.move.hby, item.move.hbw, item.move.hbh
            if touching(lanky_hb, item_hb) and item.move != Lanky.move:
                lanky_touching_rwall = True
        for item in all_platforms:
            item_hb = item.x, item.y, item.w, item.h
            if touching(lanky_hb, item_hb):
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


platform_color = (0, 0, 200)


class Platform:
    def __init__(self, rect, color=platform_color):
        all_platforms.append(self)
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.rect = self.x, self.y, self.w, self.h
        self.box = Box(rect, color)


Tubby = Creature(10, (1000, 920), (0, 0), (0, 0, 90, 90))
Tubby.create_box(Tubby.move.hb(), (200, 0, 0))

Lanky = Creature(10, (450, 820), (0, 0), (0, 0, 90, 190))
Lanky.create_box(Lanky.move.hb(), (0, 200, 200))

pass

floor = Platform((0, 1030, 1920, 50), (0, 200, 0))

lwall = Platform((-1, -1, 1, 1080))

rwall = Platform((1920, -1, 1, 1080))

Roof = Platform((-1, -1, 1922, 1))

pass

Wall1 = Platform((610, 330, 100, 700))

lPlatform1 = Platform((10, 830, 150, 25))

lPlatform2 = Platform((360, 630, 150, 25))

lPlatform3 = Platform((110, 430, 150, 25))

Wall2 = Platform((1510, 430, 400, 600))
Wall2sub1 = Platform((1410, 830, 100, 200))

rPlatform1 = Platform((1050, 680, 100, 25))
rPlatform1sub1 = Platform((1125, 655, 25, 25))

rPlatform2 = Platform((850, 530, 100, 25))
rPlatform2sub1 = Platform((925, 505, 25, 25))

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
    for platform in all_platforms:
        pg.draw.rect(screen, platform.box.color, (platform.x, platform.y, platform.w, platform.h))

    print(Lanky.move.pos())

    pg.display.flip()

pg.quit()
quit()
