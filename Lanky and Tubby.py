import pygame as pg  # pygame is used for graphics and keyboard interaction
import threading  # threading is used for keeping movement and animation at a consistent speed
import math  # math is used for math, wow!
from PIL import Image
import random

pg.init()
pg.font.init()

running = True  # this is the variable that keeps track of if the program should quit or not

tubby_touching_ground = True
lanky_touching_ground = True

tubby_char_sheet_PIL = Image.open("tubby_char_sheet.png")
tubby_facing = "right"
tubby_doing = "idle"
tubby_animation_timer = 0
tubby_to_render = (0, 0, 1, 1)

tubby_char_sheet_PIL.thumbnail((960, 600), Image.ANTIALIAS)
tubby_char_sheet_string = tubby_char_sheet_PIL.tobytes(), tubby_char_sheet_PIL.size, tubby_char_sheet_PIL.mode
tubby_char_sheet = pg.image.fromstring(tubby_char_sheet_PIL.tobytes(), tubby_char_sheet_PIL.size,
                                       tubby_char_sheet_PIL.mode)

lanky_char_sheet_PIL = Image.open("lanky_char_sheet.png")
lanky_facing = "right"
lanky_doing = "idle"
lanky_animation_timer = 0
lanky_to_render = (0, 0, 1, 1)

lanky_char_sheet_PIL.thumbnail((1760, 1100), Image.ANTIALIAS)
lanky_char_sheet_string = lanky_char_sheet_PIL.tobytes(), lanky_char_sheet_PIL.size, lanky_char_sheet_PIL.mode
lanky_char_sheet = pg.image.fromstring(lanky_char_sheet_PIL.tobytes(), lanky_char_sheet_PIL.size,
                                       lanky_char_sheet_PIL.mode)

level_sheet = pg.image.load("Level_1_frame.png")
level_animation_timer = 0
level_to_render = (0, 0, 1, 1)

background_sheet = [pg.image.load("hell\hell_0.png"), pg.image.load("hell\hell_1.png"),
                    pg.image.load("hell\hell_2.png"), pg.image.load("hell\hell_3.png"),
                    pg.image.load("hell\hell_4.png"), pg.image.load("hell\hell_5.png"),
                    pg.image.load("hell\hell_6.png"), pg.image.load("hell\hell_7.png"),
                    pg.image.load("hell\hell_8.png"), pg.image.load("hell\hell_9.png"),
                    pg.image.load('hell\hell_10.png'), pg.image.load("hell\hell_11.png")]
background_animation_timer = 0
background_to_render = (0, 0, 1, 1)

# Initialise a full screen display object
screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)  # *ADD FULLSCREEN TO MAKE THE PROGRAM FULLSCREEN*
pg.display.set_caption("Lanky and Tubby")
screen.fill((100, 100, 100))
pg.display.flip()

# set up a key states list for key interactions. This way you can tell how long a key has been pressed
pg.event.get()
key_states = [0] * len(pg.key.get_pressed())
# define important keys
keys = {"esc": 27, "w": 119, "a": 97, "s": 115, "d": 100, "up": 273, "down": 274, "right": 275, "left": 276, "r": 114}

all_creatures = []  # create an empty list to keep track of all creatures that are created
all_platforms = []  # create an empty list to keep track of all platforms that are created

comic_sans = pg.font.SysFont('Comic Sans MS', 100)

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

    global move_keys_pressed  # make move_keys_pressed accessible in this function
    global tubby_touching_ground, lanky_touching_ground

    if running:  # if the program shouldn't quit

        move_thread = threading.Timer(1 / 100, move_thread_func)  # redefine the function so it can run again
        move_thread.start()  # restart the function

        left_pressed = move_keys_pressed[keys["a"]] >= 1 or move_keys_pressed[keys["left"]] >= 1
        right_pressed = move_keys_pressed[keys["d"]] >= 1 or move_keys_pressed[keys["right"]] >= 1

        # *add jump_pressed for jumping*

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
            # if the player is trying to jump
            if move_keys_pressed[keys["w"]] >= 1 or move_keys_pressed[keys["up"]] >= 1:
                Tubby.move.vely = -20  # jump
            else:
                Tubby.move.vely = 0  # otherwise stay don't jump and don't accelerate downwards.

        if tubby_touching_roof and Tubby.move.vely < 0:  # if tubby is going up and hits the roof...
            Tubby.move.vely = 0  # stop going upwards

        # if tubby is going in a direction and hits something on that side
        if tubby_touching_lwall and Tubby.move.velx < 0 or tubby_touching_rwall and Tubby.move.velx > 0:
            Tubby.move.velx = 0  # stop going moving side to side

        if not tubby_touching_ground:  # if tubby is in the air
            Tubby.move.vely += 1  # experience gravity

        # if left is pressed and tubby isn't going too fast
        if left_pressed >= 1 and Tubby.move.velx > -1 * Tubby_max_vel:
            Tubby.move.velx -= 1  # accelerate left
        # if right is pressed and tubby isn't going too fast
        elif right_pressed >= 1 and Tubby.move.velx < Tubby_max_vel:
            Tubby.move.velx += 1  # accelerate right
        else:  # if tubby does not accelerate left or right
            if Tubby.move.velx < 0:  # if tubby is moving left
                Tubby.move.velx += 1  # decelerate left (accelerate right until 0)
            elif Tubby.move.velx > 0:  # if tubby is moving right
                Tubby.move.velx -= 1  # decelerate right (accelerate left until 0)

        """
        *to do: change above so velocity does not fluctuate between max and max-1.*
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
        *Fix gap between platforms and players that is caused by float positions*
        """

        #        Tubby.move.posx = round(Tubby.move.posx)
        #        Tubby.move.posy = round(Tubby.move.posy)

        Lanky.move.posy += 1  # move down 1 to check floor

        lanky_touching_ground = False  # default value is false
        if Lanky.move.colliding():  # check if you are colliding
            lanky_touching_ground = True  # if so, lanky is touching the ground

        Lanky.move.posy -= 2

        lanky_touching_roof = False  # default value is false
        if Lanky.move.colliding():  # check if you are colliding
            lanky_touching_roof = True  # if so, lanky is touching the roof

        Lanky.move.posy += 1  # move down 1 to undo the last check

        Lanky.move.posx -= 1  # move left 1 to check left wall

        lanky_touching_lwall = False  # default value is false
        if Lanky.move.colliding():  # check if you are colliding
            lanky_touching_lwall = True  # if so, lanky is touching the left wall

        Lanky.move.posx += 2  # move right 2 to undo the last check and to check right wall

        lanky_touching_rwall = False  # default value is false
        if Lanky.move.colliding():  # check if you are colliding
            lanky_touching_rwall = True  # if so, lanky is touching the right wall

        Lanky.move.posx -= 1  # move left 1 to undo the last check

        if lanky_touching_ground:  # if lanky is on the ground...
            # if the player is trying to jump
            if move_keys_pressed[keys["w"]] >= 1 or move_keys_pressed[keys["up"]] >= 1:
                Lanky.move.vely = -20  # jump
            else:
                Lanky.move.vely = 0  # otherwise stay don't jump and don't accelerate downwards.

        if lanky_touching_roof and Lanky.move.vely < 0:  # if lanky is going up and hits the roof...
            Lanky.move.vely = 0  # stop going upwards

        # if lanky is going in a direction and hits something on that side
        if lanky_touching_lwall and Lanky.move.velx < 0 or lanky_touching_rwall and Lanky.move.velx > 0:
            Lanky.move.velx = 0  # stop going moving side to side

        if not lanky_touching_ground:  # if lanky is in the air
            Lanky.move.vely += 1  # experience gravity

        # if left is pressed and lanky isn't going too fast
        if left_pressed >= 1 and Lanky.move.velx > -1 * Lanky_max_vel:
            Lanky.move.velx -= 1  # accelerate left
        # if right is pressed and lanky isn't going too fast
        elif right_pressed >= 1 and Lanky.move.velx < Lanky_max_vel:
            Lanky.move.velx += 1  # accelerate right
        else:  # if lanky does not accelerate left or right
            if -1 * Lanky_max_vel <= Lanky.move.velx < 0:  # if lanky is moving left
                Lanky.move.velx += 1  # decelerate left (accelerate right until 0)
            elif Lanky_max_vel >= Lanky.move.velx > 0:  # if lanky is moving right
                Lanky.move.velx -= 1  # decelerate right (accelerate left until 0)

        if Lanky.move.vel() != (0, 0):  # if lanky is moving
            # if there is more movement along the x axis rather than the y axis
            if math.fabs(Lanky.move.velx) > math.fabs(Lanky.move.vely):
                if Lanky.move.velx > 0:  # if lanky is moving right (positive x)
                    for x in range(0, Lanky.move.velx):  # for each pixel lanky moves along the x axis
                        # move the corresponding amount along the y axis so lanky travels at the correct angle.
                        Lanky.move.update_pos(1, Lanky.move.vely / Lanky.move.velx)
                else:  # if lanky is moving left (negative x)
                    for x in range(0, -1 * Lanky.move.velx):  # for each pixel lanky moves along the x axis
                        # move the corresponding amount along the y axis so lanky travels at the correct angle.
                        Lanky.move.update_pos(-1, Lanky.move.vely / (-1 * Lanky.move.velx))
            else:  # if there is more movement along the y axis rather than the x axis
                if Lanky.move.vely > 0:  # if lanky is moving down (positive y)
                    for y in range(0, Lanky.move.vely):  # for each pixel lanky moves along the y axis
                        # move the corresponding amount along the x axis so lanky travels at the correct angle.
                        Lanky.move.update_pos(Lanky.move.velx / Lanky.move.vely, 1)
                else:  # if lanky is moving up (negative y)
                    for y in range(0, -1 * Lanky.move.vely):  # for each pixel lanky moves along the y axis
                        # move the corresponding amount along the x axis so lanky travels at the correct angle.
                        Lanky.move.update_pos(Lanky.move.velx / (-1 * Lanky.move.vely), -1)

        move_keys_pressed = [0] * len(pg.key.get_pressed())  # reset the keys that have been pressed


def animation_thread_func():
    global tubby_facing, tubby_doing, tubby_animation_timer, tubby_to_render
    global lanky_facing, lanky_doing, lanky_animation_timer, lanky_to_render
    global level_animation_timer, level_to_render
    global background_to_render, background_animation_timer
    if running:  # if the program shouldn't quit

        animation_thread = threading.Timer(1 / 10, animation_thread_func)  # redefine the function so it can run again
        animation_thread.start()  # restart the function

        tubby_last_animation = tubby_facing, tubby_doing

        if Tubby.move.velx <= -1:
            tubby_facing = "left"

        if Tubby.move.velx >= 1:
            tubby_facing = "right"

        if tubby_touching_ground:
            if -1 < Tubby.move.velx < 1:
                tubby_doing = "idle"
            else:
                tubby_doing = "walk"
        else:
            tubby_doing = "jump"

        tubby_animation_timer += 1

        if tubby_last_animation != (tubby_facing, tubby_doing):
            tubby_animation_timer = 0

        if tubby_doing == "idle":
            if tubby_facing == "right":
                tubby_to_render = (math.fmod(tubby_animation_timer, 8) * 120, 120, 120, 120)
            else:
                tubby_to_render = (math.fmod(tubby_animation_timer, 8) * 120, 480, 120, 120)

        if tubby_doing == "walk":
            if tubby_facing == "right":
                tubby_to_render = (math.fmod(tubby_animation_timer, 8) * 120, 0, 120, 120)
            else:
                tubby_to_render = (math.fmod(tubby_animation_timer, 8) * 120, 360, 120, 120)

        if tubby_doing == "jump":
            if tubby_facing == "right":
                tubby_to_render = (0, 240, 120, 120)
            else:
                tubby_to_render = (120, 240, 120, 120)

        pass

        lanky_last_animation = lanky_facing, lanky_doing

        if Lanky.move.velx >= 1:
            lanky_facing = "right"

        if Lanky.move.velx <= -1:
            lanky_facing = "left"

        if lanky_touching_ground:
            if -1 < Lanky.move.velx < 1:
                lanky_doing = "idle"
            else:
                lanky_doing = "walk"
        else:
            lanky_doing = "jump"

        lanky_animation_timer += 1

        if lanky_last_animation != (lanky_facing, lanky_doing):
            lanky_animation_timer = 0

        if lanky_doing == "idle":
            if math.fmod(lanky_animation_timer, 8) == 1 and random.randint(1, 100) < 95:
                lanky_animation_timer -= 1
            lanky_to_render = (math.fmod(lanky_animation_timer, 8) * 220, 220, 220, 220)

        if lanky_doing == "walk":
            if lanky_facing == "right":
                lanky_to_render = (math.fmod(lanky_animation_timer, 8) * 220, 0, 220, 220)
            else:
                lanky_to_render = (math.fmod(lanky_animation_timer, 8) * 220, 660, 220, 220)

        if lanky_doing == "jump":
            if lanky_facing == "right":
                lanky_to_render = (0, 440, 220, 200)
            else:
                lanky_to_render = (220, 440, 220, 220)

        level_animation_timer += 1

        # level_to_render = (math.fmod(level_animation_timer, 11) * 1080, 0, 1080, 1920)

        level_to_render = (0, 0, 1920, 1080)

        background_animation_timer += 1
        if background_animation_timer >= 12:
            background_animation_timer = 0
        background_to_render = (0, 0, 1920, 1080)


class Box:  # Box is a class for displaying a rectangle
    def __init__(self, rect, color):
        self.x = rect[0]  # x position
        self.y = rect[1]  # y position
        self.w = rect[2]  # width
        self.h = rect[3]  # height
        self.color = color  # color in (r, g, b)

    def rect(self):  # function that returns the box's rectangle as a tuple
        return self.x, self.y, self.w, self.h


class Creature:  # Creature is a class for lanky and tubby
    def __init__(self, m_position=(0, 0), m_velocity=(0, 0), m_hitbox=(0, 0, 0, 0)):
        self.move = Movement(m_position, m_velocity, m_hitbox)  # create a movement subclass for each creature
        all_creatures.append(self)  # add each new creature to the creature list
        self.box = None  # no box... for now.
        self.animations = {}  # no animations: *in development*

    def create_box(self, b_rect, b_color):  # create a box if a box is needed
        self.box = Box(b_rect, b_color)

    def hb(self):  # return hitbox as a tuple
        return self.move.posx + self.move.hbx, self.move.posy + self.move.hby, self.move.hbw, self.move.hbh


platform_default_color = (0, 0, 200)  # this is the default platform color


class Platform:  # Platform class is for platforms.
    def __init__(self, rect, color):
        self.x = rect[0]  # x position
        self.y = rect[1]  # y position
        self.w = rect[2]  # width
        self.h = rect[3]  # height
        self.rect = self.x, self.y, self.w, self.h  # the platforms initial rectangle *Fix so it updates constantly*
        self.box = Box(rect, color)  # create a box based on the rectangle

    def hb(self):  # returns hitbox as a rect syntax tuple
        return self.x, self.y, self.w, self.h


level_file = open('Level Platforms.txt')  # open the file that has the level data
level_lines = level_file.readlines()  # create a list with each element being a line in the file

for line in level_lines:  # for each line in the level...
    platform_data = eval(line)  # evaluate turns the string into a tuple containing the level data

    # if the tuple has sub-tuples, the first item of the tuple will also be a tuple. Then it has an assigned color
    if type(platform_data[0]) == tuple:
        platform_rect = platform_data[0]  # the rectangle is the first tuple
        platform_color = platform_data[1]  # the color is the second tuple
    else:
        platform_rect = platform_data  # the rectangle is the tuple
        platform_color = platform_default_color  # the color is the default platform color

    platform_temp = Platform(platform_rect, platform_color)  # create a platform with the proper rect and color
    all_platforms.append(platform_temp)  # add that platform to the platform list *move to the class init() function*

Tubby = Creature((1000, 850), (0, -10), (0, 0, 70, 90))  # create the creature that represents tubby
Tubby.create_box(Tubby.move.hb(), (200, 0, 0))  # create a box to show the hitbox of tubby

Lanky = Creature((475, 750), (0, -10), (0, 0, 55, 180))  # create a creature that represents lanky
Lanky.create_box(Lanky.move.hb(), (0, 200, 200))  # create a box to show the hitbox of lanky

win_text = comic_sans.render("You Win!", False, (0, 0, 0), )

move_thread_func()  # start the move function loop
animation_thread_func()  # start the animation function loop

while running:  # if the program is running...
    for event in pg.event.get():  # check to see if the | x | button is clicked, and if so, close the tab
        if event.type == pg.QUIT:
            running = False

    for key_id in range(0, len(pg.key.get_pressed())):  # for every key...
        if pg.key.get_pressed()[key_id] == 1:  # if that key is pressed...
            key_states[key_id] += 1  # change how long the key has been pressed for by 1
            move_keys_pressed[key_id] = 1  # tell the movement function the key has been pressed in the past frame
        else:  # if that key isn't pressed
            key_states[key_id] = 0  # then change how long the kay had been pressed for to 0

    if key_states[keys["esc"]] >= 1:  # if the escape key is pressed
        running = False  # quit the game

    if key_states[keys["r"]] == 1:
        Tubby.move.posx = 1000
        Tubby.move.posy = 850
        Tubby.move.vely = -10
        Lanky.move.posx = 475
        Lanky.move.posy = 750
        Lanky.move.vely = -10

    screen.fill((100, 100, 100))  # fill the background with the background color

    Tubby_x = Tubby.move.posx + Tubby.box.x  # find the rect x
    Tubby_y = Tubby.move.posy + Tubby.box.y  # find the rect y
    # render that creature
    # pg.draw.rect(screen, Tubby.box.color, (Tubby_x, Tubby_y, Tubby.box.w, Tubby.box.h))

    Lanky_x = Lanky.move.posx + Lanky.box.x  # find the rect x
    Lanky_y = Lanky.move.posy + Lanky.box.y  # find the rect y
    # render that creature
    # pg.draw.rect(screen, Lanky.box.color, (Lanky_x, Lanky_y, Lanky.box.w, Lanky.box.h))

    # screen.blit(background_sheet[background_animation_timer], (0, 0), background_to_render)
    screen.blit(tubby_char_sheet, (Tubby.move.posx - 20, Tubby.move.posy - 28), tubby_to_render)
    if lanky_doing != "jump":
        screen.blit(lanky_char_sheet, (Lanky.move.posx - 80, Lanky.move.posy - 39), lanky_to_render)
    else:
        screen.blit(lanky_char_sheet, (Lanky.move.posx - 80, Lanky.move.posy - 9), lanky_to_render)
    # screen.blit(level_sheet, (0, 0), level_to_render)

    # """
    for platform in all_platforms:  # for each platform
        # render that platform
        pg.draw.rect(screen, platform.box.color, (platform.x, platform.y, platform.w, platform.h))
    # """

    Lanky_and_Tubby_on_platforms = 0

    if 1660 - 70 <= Tubby.move.posx <= 1660 + 100 and 430 - 95 <= Tubby.move.posy <= 430 - 85:
        pg.draw.rect(screen, (255, 255, 0), (1655, 430, 110, 15))
        Lanky_and_Tubby_on_platforms += 1

    if 350 - 55 <= Lanky.move.posx <= 350 + 100 and 1030 - 185 <= Lanky.move.posy <= 1030 - 175:
        pg.draw.rect(screen, (255, 255, 0), (345, 1030, 110, 15))
        Lanky_and_Tubby_on_platforms += 1

    if Lanky_and_Tubby_on_platforms == 2:
        pg.draw.rect(screen, (255, 255, 0), (720, 465, 480, 150))
        screen.blit(win_text, (760, 465))

    pg.draw.rect(screen, (255, 169, 169), (1660, 430, 100, 10))
    pg.draw.rect(screen, (192, 52, 239), (350, 1030, 100, 10))

    pg.display.flip()  # update the display window

pg.font.quit()
pg.quit()  # terminate pygame
quit()  # terminate the program
