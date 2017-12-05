'''
The Stats module, with PlayerStats, TeamStats, and GameStats.

Refactor:
Attribs:
Stats

Methods:
Init, Get Initial Stats, Show Stats, Add Stats, Get Statline

Future:
more stats
keep team with stats
separate goalies and players
'''
        
class PlayerStats(object):
    
    def __init__(self):
        self.season_stats = self.get_blank_stats()
        self.playoff_stats = self.get_blank_stats()
        self.career_stats = self.get_blank_stats()
        self.stats = [self.season_stats, self.playoff_stats, self.career_stats]
        
    def get_blank_stats(self):
        stats = {"Goals": 0, "Assists": 0, "Minutes": 0, "Shots": 0, "Saves": 0, "Goals Allowed": 0}
        return stats
        
    def add_stat(self, era, stat, amount):
        self.stats[era][stat] += amount
        
    def show_stats(self, era):
        cur_stats = self.stats[era]
        s = ""
        points = cur_stats["Goals"] + cur_stats["Assists"]
        s += "GAP: " + str(cur_stats["Goals"]) + "-" + str(cur_stats["Assists"]) + "-" + str(points)
        s += "\nShots: " + str(cur_stats["Shots"])
        s += "\nSaves: " + str(cur_stats["Saves"]) + "-" + str(cur_stats["Saves"] + cur_stats["Goals Allowed"])
        s += "\nMinutes: " + str(cur_stats["Minutes"])
        return s
        
    def get_statline(self):
        pass #TODO:
        
    def update_career_stats(self):
        pass #TODO:
        

class TeamStats(object): #TODO: check rest of this class, combine eras
    
    def __init__(self):
        self.stats = self.get_blank_stats()
        
    def get_blank_stats(self):
        stats = {"Wins": 0, "Losses": 0, "Ties": 0, "Goals For": 0, "Goals Against": 0}
        return stats
        
    def add_stat(self, stat, amount):
        self.stats[stat] += amount
        
    def show_stats(self):
        s = ""
        s += "Record: " + str(self.stats["Wins"]) + "-" + str(self.stats["Losses"]) + "-" + str(self.stats["Ties"])
        points = 2 * self.stats["Wins"] + self.stats["Ties"]
        s += "\nPoints: " + str(points)
        s += "\nGoals For: " + str(self.stats["Goals For"])
        s += "\nGoals Against: " + str(self.stats["Goals Against"])
        return s
        
    def get_statline(self):
        pass #TODO:
        

class GameStats(object): #TODO: check rest of this class
    
    def __init__(self, teams):
        self.player_stats = self.get_initial_player_stats(teams)
        self.team_stats = self.get_initial_team_stats(teams)
        
    def get_initial_player_stats(self, teams):
        players = []
        for team in teams:
            players += team.get_full_roster()
        player_stats = {player: {"Goals": 0, "Assists": 0, "Minutes": 0, "Shots": 0, "Saves": 0, "Goals Allowed": 0} for player in players}
        return player_stats
        
    def get_initial_team_stats(self, teams):
        team_stats = {team: {"Wins": 0, "Losses": 0, "Ties": 0, "Goals For": 0, "Goals Against": 0} for team in teams}
        return team_stats
        
    def add_player_stats(self, player, stat, amount):
        self.player_stats[player][stat] += amount
        
    def add_team_stats(self, team, stat, amount):
        self.team_stats[team][stat] += amount
        
    def update_player_stats(self):
        for player in self.player_stats:
            for stat in self.player_stats[player]:
                player.stats.add_stat(stat, self.player_stats[player][stat])
    
    def update_team_stats(self):
        for team in self.team_stats:
            for stat in self.team_stats[team]:
                team.stats.add_stat(stat, self.team_stats[team][stat])
                