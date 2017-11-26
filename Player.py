'''
The Player class. For pass 1, we need:
    Name
    Age
    Position
    Team
    Rating (Scoring if non-G, Saving if G)
    Stats (If non-G: minutes, shots, goals, assists; if G: saves, goals allowed)
    
    Method to age
    
    Function to create random player
'''
 
import random
import Stats
 
class Player(object):
   
    used_names = set()
   
    def __init__(self, name, age, position, rating, team = None):
        if __debug__:
            assert type(name) == str, "Name not a string"
            assert type(age) == int, "Age not an integer"
            assert age in range(1, 100), "Age out of range"
            assert type(position) == str, "Position not a string"
            assert position in ("C", "LW", "RW", "D", "G"), "No such position"
            assert type(rating) == int, "Rating not an integer"
            assert rating in range(0, 100), "Rating out of range"
        while name in Player.used_names:
            name += " Jr"
        self.name = name
        Player.used_names.add(name)
        self.age = age
        self.position = position
        self.rating = rating
        self.team = team
        self.stats = Stats.PlayerStats()
        
    def __str__(self):
        return self.name
       
    def age_year(self):
        self.age += 1
        self.rating += random.randrange(-5,6)
        if self.rating < 0:
            self.rating = 0
        if self.rating > 99:
            self.rating = 99
        
    def show_profile(self):
        s = ""
        s += "Player: " + self.name + ", " + str(self.age) + ", " + self.position
        s += "\nTeam: " + str(self.team)
        s += "\nRating: " + str(self.rating)
        s += "\n" + self.show_stats()
        return s


player_name_list = []
 
def get_random_names():
    global player_name_list
    try:
        with open('PlayerNames.txt', 'r') as f:
            player_name_list = [line.rstrip() for line in f]
    except FileNotFoundError:
        print("PlayerNames.txt not found - random players cannot be created")
       
def generate_name():
    global player_name_list
    fn = random.choice(player_name_list)
    ln = random.choice(player_name_list)
    name = fn + " " + ln
    return name
           
def create_random_player(pos = None):
    age = random.randrange(18,40)
    if not pos:
        pos = random.choice(["C", "LW", "RW", "D", "G"])
    rating = random.randrange(40, 90)
    name = generate_name()
    player = Player(name, age, pos, rating)
    return player
   
get_random_names()