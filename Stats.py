'''
The Stats module, with PlayerStats, TeamStats, and GameStats.
'''
        
class PlayerStats(object):
    
    def __init__(self):
        self.stats = self.get_initial_stats()
        
    def get_initial_stats(self):
        stats = {"Goals": 0, "Assists": 0, "Minutes": 0, "Shots": 0, "Saves": 0, "Goals Allowed": 0}
        return stats
        
    def add_stat(self, stat, amount):
        self.stats[stat] += amount
        
    def show_stats(self):
        s = ""
        points = self.stats["Goals"] + self.stats["Assists"]
        s += "GAP: " + str(self.stats["Goals"]) + "-" + str(self.stats["Assists"]) + "-" + str(points)
        s += "\nShots: " + str(self.stats["Shots"])
        s += "\nSaves: " + str(self.stats["Saves"]) + "-" + str(self.stats["Saves"] + self.stats["Goals Allowed"])
        s += "\nMinutes: " + str(self.stats["Minutes"])
        return s
        

class TeamStats(object):
    
    def __init__(self):
        self.stats = self.get_initial_stats()
        
    def get_initial_stats(self):
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
        

class GameStats(object):
    
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
                