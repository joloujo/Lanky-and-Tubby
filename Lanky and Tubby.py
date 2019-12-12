import pygame as pg  # pygame is used for graphics and keyboard interaction
import threading  # threading is used for keeping movement and animation at a consistent speed
import math  # math is used for math, wow!

pg.init()

running = True  # this is the variable that keeps track of if the program should quit or not

# Initialise a full screen display object
screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
pg.display.set_caption("Lanky and Tubby")
screen.fill((100, 100, 100))
pg.display.flip()

# set up a key states list for key interactions. This way you can tell how long a key has been pressed
pg.event.get()
key_states = [0] * len(pg.key.get_pressed())
keys = {"esc": 27, "w": 119, "a": 97, "s": 115, "d": 100}  # define important keys

all_creatures = []  # create an empty list to keep track of all creatures that are created
all_platforms = []  # create an empty list to keep track of all platforms that are created


def touching(rect_1, rect_2):
    touching_x = rect_2[0] < rect_1[0] + rect_1[2] and rect_1[0] < rect_2[0] + rect_2[2]  # overlap on x axis?
    touching_y = rect_2[1] < rect_1[1] + rect_1[3] and rect_1[1] < rect_2[1] + rect_2[3]  # overlap on y axis?
    if touching_x and touching_y:  # if the two rectangles overlap in both axises...
        return True  # they are touching
    return False  # otherwise they are not touching


class Movement:  # this is the class that manages movement, velocities, collisions, and hitboxes.
    def __init__(self, position=(0, 0), velocity=(0, 0), hitbox=(0, 0, 0, 0)):
        self.posx = position[0]
        self.posy = position[1]
        self.velx = velocity[0]
        self.vely = velocity[1]
        self.hbx = hitbox[0]
        self.hby = hitbox[1]
        self.hbw = hitbox[2]
        self.hbh = hitbox[3]

    def pos(self):  # returns position as a tuple
        return self.posx, self.posy

    def vel(self):  # returns velocity as a tuple
        return self.velx, self.vely

    def hb(self):  # returns hitbox as a tuple
        return self.hbx, self.hby, self.hbw, self.hbh

    def colliding(self):
        self_hb = self.posx + self.hbx, self.posy + self.hby, self.hbw, self.hbh  # calculate it's own hitbox
        for item in all_creatures:  # do this for every creature
            if touching(self_hb, item.hb()) and item.move != self:  # if the creatures are touching and not the same...
                return True  # then it is colliding
        for item in all_platforms:  # do this for every platform
            if touching(self_hb, item.hb()):  # if the platforms are touching...
                return True  # then it is colliding
        return False  # if it isn't touching anything, it is not colliding

    def update_pos(self, move_x, move_y):
        self.posx += move_x  # move how much you need to move along the x axis
        if self.colliding():  # check if you are colliding
            self.posx -= move_x  # if so, move back
        self.posy += move_y  # move how much you need to move along the y axis
        if self.colliding():  # check if you are colliding
            self.posy -= move_y  # if so, move back


move_keys_pressed = [0] * len(pg.key.get_pressed())  # this is a list similar to key_states, but for each movement frame

# set maximum velocities for characters
Tubby_max_vel = 10
Lanky_max_vel = 10


def move_thread_func():  # thread function for movement to keep movement speed consistent.
    global move_keys_pressed
    if running:  # if the program shouldn't quit

        Tubby.move.posy += 1  # move down 1 to check floor

        tubby_touching_ground = False  # default value is false
        if Tubby.move.colliding():  # check if you are colliding
            tubby_touching_ground = True  # if so, tubby is touching the ground

        Tubby.move.posy -= 2  # move up 2 to undo the last check and to check roof

        tubby_touching_roof = False  # default value is false
        if Tubby.move.colliding():  # check if you are colliding
            tubby_touching_roof = True  # if so, tubby is touching the roof

        Tubby.move.posy += 1  # move down 1 to undo the last check

        Tubby.move.posx -= 1  # move left 1 to check left wall

        tubby_touching_lwall = False  # default value is false
        if Tubby.move.colliding():  # check if you are colliding
            tubby_touching_lwall = True  # if so, tubby is touching the left wall

        Tubby.move.posx += 2  # move right 2 to undo the last check and to check right wall

        tubby_touching_rwall = False  # default value is false
        if Tubby.move.colliding():  # check if you are colliding
            tubby_touching_rwall = True  # if so, tubby is touching the right wall

        Tubby.move.posx -= 1  # move left 1 to undo the last check

        if tubby_touching_ground:  # if tubby is on the ground...
            if move_keys_pressed[keys["w"]] >= 1:  # if the player is trying to jump
                Tubby.move.vely = -20  # jump
            else:
                Tubby.move.vely = 0  # otherwise stay don't jump and don't accelerate downwards.

        if tubby_touching_roof and Tubby.move.vely < 0:  # if tubby is going up and hits the roof...
            Tubby.move.vely = 0  # stop going upwards

        # if tubby is going in a direction and hits something on that side
        if tubby_touching_lwall and Tubby.move.velx < 0 or tubby_touching_rwall and Tubby.move.velx > 0:
            # stop going moving side to side
            Tubby.move.velx = 0

        if not tubby_touching_ground:  # if tubby is in the air
            Tubby.move.vely += 1  # experience gravity

        # if left is pressed and tubby isn't going too fast
        if move_keys_pressed[keys["a"]] >= 1 and Tubby.move.velx > -1 * Tubby_max_vel:
            Tubby.move.velx -= 1  # accelerate left
        # if right is pressed and tubby isn't going too fast
        elif move_keys_pressed[keys["d"]] >= 1 and Tubby.move.velx < Tubby_max_vel:
            Tubby.move.velx += 1  # accelerate right
        else:  # if tubby does not accelerate left or right
            if Tubby.move.velx < 0:  # if tubby is moving left
                Tubby.move.velx += 1  # decelerate left (accelerate right until 0)
            elif Tubby.move.velx > 0:  # if tubby is moving right
                Tubby.move.velx -= 1  # decelerate right (accelerate left until 0)

        """
        to do: change above so velocity does not fluctuate between max and max-1.
        """

        if Tubby.move.vel() != (0, 0):  # if tubby is moving
            # if there is more movement along the x axis rather than the y axis
            if math.fabs(Tubby.move.velx) > math.fabs(Tubby.move.vely):
                if Tubby.move.velx > 0:  # if tubby is moving right (positive x)
                    for x in range(0, Tubby.move.velx):  # for each pixel tubby moves along the x axis
                        # move the corresponding amount along the y axis so tubby travels at the correct angle.
                        Tubby.move.update_pos(1, Tubby.move.vely / Tubby.move.velx)
                else:  # if tubby is moving left (negative x)
                    for x in range(0, -1 * Tubby.move.velx):  # for each pixel tubby moves along the x axis
                        # move the corresponding amount along the y axis so tubby travels at the correct angle.
                        Tubby.move.update_pos(-1, Tubby.move.vely / (-1 * Tubby.move.velx))
            else:  # if there is more movement along the y axis rather than the x axis
                if Tubby.move.vely > 0:  # if tubby is moving down (positive y)
                    for y in range(0, Tubby.move.vely):  # for each pixel tubby moves along the y axis
                        # move the corresponding amount along the x axis so tubby travels at the correct angle.
                        Tubby.move.update_pos(Tubby.move.velx / Tubby.move.vely, 1)
                else:  # if tubby is moving up (negative y)
                    for y in range(0, -1 * Tubby.move.vely):  # for each pixel tubby moves along the y axis
                        # move the corresponding amount along the x axis so tubby travels at the correct angle.
                        Tubby.move.update_pos(Tubby.move.velx / (-1 * Tubby.move.vely), -1)

        """     TO DO:
        Fix gap between platforms and players that is caused by float positions
        """

        #        Tubby.move.posx = round(Tubby.move.posx)
        #        Tubby.move.posy = round(Tubby.move.posy)

        Lanky.move.posy += 1

        lanky_touching_ground = False
        if Lanky.move.colliding():  # check if you are colliding
            lanky_touching_ground = True

        Lanky.move.posy -= 2

        lanky_touching_roof = False
        if Lanky.move.colliding():  # check if you are colliding
            lanky_touching_roof = True

        Lanky.move.posy += 1

        Lanky.move.posx -= 1

        lanky_touching_lwall = False
        if Lanky.move.colliding():  # check if you are colliding
            lanky_touching_lwall = True

        Lanky.move.posx += 2

        lanky_touching_rwall = False
        if Lanky.move.colliding():  # check if you are colliding
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
    def __init__(self, m_position=(0, 0), m_velocity=(0, 0), m_hitbox=(0, 0, 0, 0)):
        self.move = Movement(m_position, m_velocity, m_hitbox)
        all_creatures.append(self)
        self.box = None
        self.animations = {}

    def create_box(self, b_rect, b_color):
        self.box = Box(b_rect, b_color)

    def hb(self):
        return self.move.posx + self.move.hbx, self.move.posy + self.move.hby, self.move.hbw, self.move.hbh


platform_default_color = (0, 0, 200)


class Platform:
    def __init__(self, rect, color):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.rect = self.x, self.y, self.w, self.h
        self.box = Box(rect, color)

    def hb(self):
        return self.x, self.y, self.w, self.h


level_file = open('Level Platforms.txt')
level_lines = level_file.readlines()

for line in level_lines:
    platform_data = eval(line)

    if type(platform_data[0]) == tuple:
        platform_rect = platform_data[0]
        platform_color = platform_data[1]
    else:
        platform_rect = platform_data
        platform_color = platform_default_color

    platform_temp = Platform(platform_rect, platform_color)
    all_platforms.append(platform_temp)

Tubby = Creature((1000, 920), (0, 0), (0, 0, 90, 90))
Tubby.create_box(Tubby.move.hb(), (200, 0, 0))

Lanky = Creature((450, 820), (0, 0), (0, 0, 90, 190))
Lanky.create_box(Lanky.move.hb(), (0, 200, 200))

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

    pg.display.flip()

pg.quit()
quit()
