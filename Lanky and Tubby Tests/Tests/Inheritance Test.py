class Being():
    def __init__(self, hitbox, alliance):
        self.hitbox = hitbox
        self.alliance = alliance

    def say_hitbox(self):
        print(self.hitbox)


class Player(Being):
    def __init__(self, name, hitbox, alliance):
        super().__init__(hitbox, alliance)
        self.name = name

    def say_name(self):
        print("My name is", self.name)

enemy1 = Being((50, 50), "enemies")
player1 = Player("Tubby", (100, 100), "players")

enemy1.say_hitbox()
player1.say_hitbox()
player1.say_name()
