"""file = open('Parsing Test Text', 'r')

file_lines = file.readlines()

for line in file_lines:
    line_from_string = eval(line)
    print(line_from_string[0])
    print(type(line_from_string[0]))
    """


class Box:
    def __init__(self, rect, color):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.color = color

    def rect(self):
        return self.x, self.y, self.w, self.h


platform_default_color = (0, 0, 200)


class Platform:
    def __init__(self, rect, color):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.rect = self.x, self.y, self.w, self.h
        self.box = Box(rect, color)


all_platforms = []

level_file = open('Parsing Test Text')
level_lines = level_file.readlines()

for line in level_lines:
    platform_data = eval(line)

    """
    print("DEBUG: Line -", line, type(line))
    print("DEBUG: Plat_data -", platform_data, type(platform_data))
    print("DEBUG: Plat_data_sep2 -", platform_data[0], "sep", platform_data[1])
    print("DEBUG: Plat_data_sep1 -", platform_data, "sep")

    print(type(platform_data[0]) == tuple)
    """

    if type(platform_data[0]) == tuple:
        platform_rect = platform_data[0]
        platform_color = platform_data[1]
    else:
        platform_rect = platform_data
        platform_color = platform_default_color

    platform_temp = Platform(platform_rect, platform_color)
    all_platforms.append(platform_temp)

for platform in all_platforms:
    print(platform.rect, platform.box.color)
