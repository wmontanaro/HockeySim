'''
Game class. For pass 1 we need:

Play three periods
Sudden death OT if tied
If playoff, play more OTs until goal
Update stats

stat display, minute, period, game, tests
'''

import random, math
import Stats

class Game(object):
    
    def __init__(self, team1, team2, playoff = False):
        self.team1 = team1
        self.team2 = team2
        self.stats = Stats.GameStats([team1, team2])
        self.playoff = playoff
        self.olines = ["L1", "L2", "L3", "L4"]
        self.dlines = ["D1", "D2", "D3"]
        
    def get_lines(self, offense, defense):
        offoline = random.choice(self.olines)
        offdline = random.choice(self.dlines)
        oline = [player for player in offense.lines.lines[offoline] + offense.lines.lines[offdline]]
        defoline = random.choice(self.olines)
        defdline = random.choice(self.dlines)
        dline = [player for player in defense.lines.lines[defoline] + defense.lines.lines[defdline]]
        dline.append(defense.lines.lines["G"][0])
        return (oline, dline)
        
    def simulate_shot(self, oline, dline):
        oscore = 0
        for player in oline:
            oscore += player.rating
        dscore = 0
        for player in dline:
            dscore += player.rating
        dadv = dscore - oscore
        prob = 1 / (1 + math.exp(0.05 * dadv))
        luck = random.random()
        if prob > luck:
            return "Goal"
        else:
            return "Miss"
            
    def process_result(self, offense, defense, oline, dline, result):
        for player in oline + dline:
            self.stats.add_player_stats(player, "Minutes", 1)
        offgoalie = offense.lines.lines["G"][0]
        self.stats.add_player_stats(offgoalie, "Minutes", 1)
        shooter = oline.pop(random.randrange(len(oline)))
        self.stats.add_player_stats(shooter, "Shots", 1)
        if result == "Goal":
            self.stats.add_player_stats(shooter, "Goals", 1)
            self.stats.add_player_stats(dline[-1], "Goals Allowed", 1)
            self.stats.add_team_stats(offense, "Goals For", 1)
            self.stats.add_team_stats(defense, "Goals Against", 1)
            numassists = random.randrange(3)
            for i in range(numassists):
                p = oline.pop(random.randrange(len(oline)))
                self.stats.add_player_stats(p, "Assists", 1)
        elif result == "Miss":
            self.stats.add_player_stats(dline[-1], "Saves", 1)
        
    def play_minute(self):
        offense = random.choice([self.team1, self.team2])
        if offense == self.team1:
            defense = self.team2
        else:
            defense = self.team1
        oline, dline = self.get_lines(offense, defense)
        result = self.simulate_shot(oline, dline)
        self.process_result(offense, defense, oline, dline, result)
        
    def play_period(self):
        for i in range(20):
            self.play_minute()
        
    def play_overtime(self):
        if self.playoff:
            minutes = 10000
        else:
            minutes = 5
        for i in range(minutes):
            self.play_minute()
            if self.stats.team_stats[self.team1]["Goals For"] != self.stats.team_stats[self.team2]["Goals For"]:
                return
    
    def play_game(self):
        for i in range(3):
            self.play_period()
        if self.stats.team_stats[self.team1]["Goals For"] == self.stats.team_stats[self.team2]["Goals For"]:
            self.play_overtime()
        self.stats.update_player_stats()
        if self.stats.team_stats[self.team1]["Goals For"] > self.stats.team_stats[self.team2]["Goals For"]:
            self.stats.add_team_stats(self.team1, "Wins", 1)
            self.stats.add_team_stats(self.team2, "Losses", 1)
        elif self.stats.team_stats[self.team1]["Goals For"] < self.stats.team_stats[self.team2]["Goals For"]:
            self.stats.add_team_stats(self.team1, "Losses", 1)
            self.stats.add_team_stats(self.team2, "Wins", 1)
        else:
            self.stats.add_team_stats(self.team1, "Ties", 1)
            self.stats.add_team_stats(self.team2, "Ties", 1)
        self.stats.update_team_stats()
        