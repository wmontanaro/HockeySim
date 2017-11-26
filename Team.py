'''
The Team class. For pass 1 we need:
    Name
    Roster
    Lines
    Stats (wins, losses, ties, goals for, goals against)
    
    Function to create random team
'''

import random
import Player, Stats

class Team(object):
    
    teams = set()
    
    def __init__(self, name):
        if __debug__:
            assert type(name) == str
        if name in Team.teams:
            print("Name already used")
            return
        self.name = name
        self.roster = Roster()
        self.lines = self.roster.lines
        self.stats = Stats.TeamStats()
        
    def __str__(self):
        return self.name
        
    def add_player(self, player):
        self.roster.add_player(player)
        
    def remove_player(self, player):
        self.roster.remove_player(player)
        
    def generate_default_lines(self):
        self.roster.generate_default_lines()
        
    def get_full_roster(self):
        return self.roster.get_full_roster()
        
    def show_lines(self):
        return self.lines.__str__()
        
    def print_player_stats(self):
        r = self.get_full_roster()
        name_col_length = max([len(p.name) for p in r]) + 2
        header = "Player".ljust(name_col_length) + "Pos  Goals  Assists  Points  Shots  Minutes  Saves  Shots Faced"
        print(header)
        for p in r:
            s = p.name.ljust(name_col_length)
            s += p.position.rjust(3)
            s += str(p.stats.stats["Goals"]).rjust(7)
            s += str(p.stats.stats["Assists"]).rjust(9)
            s += str(p.stats.stats["Goals"] + p.stats.stats["Assists"]).rjust(8)
            s += str(p.stats.stats["Shots"]).rjust(7)
            s += str(p.stats.stats["Minutes"]).rjust(9)
            s += str(p.stats.stats["Saves"]).rjust(7)
            s += str(p.stats.stats["Saves"] + p.stats.stats["Goals Allowed"]).rjust(13)
            print(s)
        
    def age_year(self):
        for player in self.roster:
            player.age_year()
            
            
class Roster(object):
    
    def __init__(self):
        self.roster = self.get_initial_roster()
        self.lines = Lines()
        
    def __str__(self):
        s = ""
        s += "C: "
        if len(self.roster["C"]) > 0:
            for player in self.roster["C"][:-1]:
                s += str(player) + ", "
            s += str(self.roster["C"][-1])
        s += "\nLW: "
        if len(self.roster["LW"]) > 0:
            for player in self.roster["LW"][:-1]:
                s += str(player) + ", "
            s += str(self.roster["LW"][-1])
        s += "\nRW: "
        if len(self.roster["RW"]) > 0:
            for player in self.roster["RW"][:-1]:
                s += str(player) + ", "
            s += str(self.roster["RW"][-1])
        s += "\nD: "
        if len(self.roster["D"]) > 0:
            for player in self.roster["D"][:-1]:
                s += str(player) + ", "
            s += str(self.roster["D"][-1])
        s += "\nG: "
        if len(self.roster["G"]) > 0:
            for player in self.roster["G"][:-1]:
                s += str(player) + ", "
            s += str(self.roster["G"][-1])
        return s
        
    def get_initial_roster(self):
        roster = {"C": [], "LW": [], "RW": [], "D": [], "G": []}
        return roster
        
    def get_full_roster(self):
        r = []
        for pos in self.roster:
            r += self.roster[pos]
        return r
    
    def generate_default_lines(self):
        self.lines.generate_default_lines(self.roster)
        
    def add_player(self, player):
        self.roster[player.position].append(player)
        self.sort_position(player.position)
        
    def remove_player(self, player):
        if player not in self.roster:
            print("Player not on roster; cannot remove")
            return
        self.roster[player.position].remove(player)
        
    def sort_position(self, position):
        self.roster[position].sort(key = lambda x: x.rating, reverse = True)


class Lines(object):
    
    def __init__(self):
        self.lines = self.get_initial_lines()
        
    def __str__(self):
        s = ""
        s += "L1: "
        if len(self.lines["L1"]) > 0:
            for player in self.lines["L1"][:-1]:
                s += str(player) + ", "
            s += str(self.lines["L1"][-1])
        s += "\nL2: "
        if len(self.lines["L2"]) > 0:
            for player in self.lines["L2"][:-1]:
                s += str(player) + ", "
            s += str(self.lines["L2"][-1])
        s += "\nL3: "
        if len(self.lines["L3"]) > 0:
            for player in self.lines["L3"][:-1]:
                s += str(player) + ", "
            s += str(self.lines["L3"][-1])
        s += "\nL3: "
        if len(self.lines["L4"]) > 0:
            for player in self.lines["L4"][:-1]:
                s += str(player) + ", "
            s += str(self.lines["L4"][-1])
        s += "\nD1: "
        if len(self.lines["D1"]) > 0:
            for player in self.lines["D1"][:-1]:
                s += str(player) + ", "
            s += str(self.lines["D1"][-1])
        s += "\nD2: "
        if len(self.lines["D2"]) > 0:
            for player in self.lines["D2"][:-1]:
                s += str(player) + ", "
            s += str(self.lines["D2"][-1])
        s += "\nD3: "
        if len(self.lines["D3"]) > 0:
            for player in self.lines["D3"][:-1]:
                s += str(player) + ", "
            s += str(self.lines["D3"][-1])
        s += "\nG: "
        if len(self.lines["G"]) > 0:
            for player in self.lines["G"][:-1]:
                s += str(player) + ", "
            s += str(self.lines["G"][-1])
        s += "\nScratch: "
        if len(self.lines["Scratch"]) > 0:
            for player in self.lines["Scratch"]:
                s += str(player) + ", "
            s += str(self.lines["Scratch"][-1])
        return s
        
    def get_initial_lines(self):
        lines = {"L1": [], "L2": [], "L3": [], "L4": [], "D1": [], "D2": [], "D3": [], "G": [], "Scratch": []}
        return lines
        
    def generate_default_lines(self, roster):
        if len(roster["C"]) < 4:
            print("Not enough C")
            return
        if len(roster["LW"]) < 4:
            print("Not enough LW")
            return
        if len(roster["RW"]) < 4:
            print("Not enough RW")
            return
        if len(roster["D"]) < 6:
            print("Not enough D")
            return
        if len(roster["G"]) < 2:
            print("Not enough G")
            return
        self.lines["L1"] = [roster["C"][0], roster["LW"][0], roster["RW"][0]]
        self.lines["L2"] = [roster["C"][1], roster["LW"][1], roster["RW"][1]]
        self.lines["L3"] = [roster["C"][2], roster["LW"][2], roster["RW"][2]]
        self.lines["L4"] = [roster["C"][3], roster["LW"][3], roster["RW"][3]]
        self.lines["D1"] = roster["D"][:2]
        self.lines["D2"] = roster["D"][2:4]
        self.lines["D3"] = roster["D"][4:6]
        self.lines["G"] = roster["G"]


team_name_list = []

def get_random_names():
    global team_name_list
    try:
        with open('TeamNames.txt', 'r') as f:
            team_name_list = [line.rstrip() for line in f]
    except FileNotFoundError:
        print("TeamNames.txt not found - random players cannot be created")
        return
    random.shuffle(team_name_list)
       
def generate_name():
    global team_name_list
    if len(team_name_list) == 0:
        print("No more team names found - random teams cannot be created")
        return
    tname = team_name_list.pop()
    return tname
           
def create_random_team():
    name = generate_name()
    team = Team(name)
    for i in range(4):
        for pos in ["C", "LW", "RW"]:
            team.add_player(Player.create_random_player(pos))
    for j in range(6):
        team.add_player(Player.create_random_player("D"))
    for k in range(2):
        team.add_player(Player.create_random_player("G"))
    team.generate_default_lines()
    return team
   
get_random_names()