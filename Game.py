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
    
    """The Game class.
    
    This is the class that represents a game. It includes all the functions
    needed to play the game and update the statistics of the teams involved.
    
    Class Attributes:
        None
        
    Attributes:
        team1: The first Team to play.
        team2: The second Team to play.
        era: A string representing the era in which this game takes place;
            expected to be "season" or "playoff" (future: "preseason"?).
            
    Future:
        Home vs Away with an advantage for Home
        Better simulate shot function
        Better way to simulate the game (for instance randomizing when shots
            occur)
        Better fidelity to real results
        Way for human player to interact
    """
    
    def __init__(self, team1, team2, era = "season"):
        """Inits a Game class.
        
        Args:
            team1: A Team object (home team).
            team2: A Team object (away team).
            era: A string representing the era in which this game takes place;
                expected to be "season" or "playoff" (future: "preseason"?).
            
        Returns:
            None
        """
        self.team1 = team1
        self.team2 = team2
        self.era = era
        self.olines = ["L1", "L2", "L3", "L4"]
        self.dlines = ["D1", "D2", "D3"]
        
    def get_lines(self, offense, defense):
        """Get the lines on the ice for a shot.
        
        The lines are chosen randomly from all possible offensive and 
        defensive lines (goalies are fixed).
        
        Args:
            offense: The Team that will take the shot.
            defense: The Team that is on defense.
            
        Returns:
            A tuple of lists of players; the first list is the offensive 
            players on the ice for the shot and the second list is the 
            defensive players.
        """
        offoline = random.choice(self.olines)
        offdline = random.choice(self.dlines)
        oline = [player for player in offense.get_line(offoline) + offense.get_line(offdline)]
        defoline = random.choice(self.olines)
        defdline = random.choice(self.dlines)
        dline = [player for player in defense.get_line(defoline) + defense.get_line(defdline)]
        dline.append(defense.get_line("G")[0])
        return (oline, dline)
        
    def simulate_shot(self, oline, dline):
        """Get the randomized result of a shot by the given oline against
        the given dline.
        
        For v1, this adds the oline ratings and the dline ratings (combined
        with the defensive team's goalie), then compares a random number
        between 0 and 1 to a weighted probability function with the difference
        between offensive and defensive scores as the weight. If the random
        number is less than the function result, then we have a goal. 
        Otherwise, we have a miss.
        
        Args:
            oline: A list of Players on offense.
            dline: A list of Players on defense (including the goalie).
        
        returns:
            A String with the result; either Goal or Miss.
        """
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
        """For the given result, update the team and player stats.
        
        Note that we choose the shooter at this point (for v1, who is shooting
        does not change the scoring probability).
        
        Args:
            offense: The Team on offense.
            defense: The Team on defense.
            oline: The list of Players on offense.
            dline: The list of Players on defense (with the goalie last).
            result: A string containing the outcome: Goal or Miss.
        
        Returns:
            None
        """
        for player in oline + dline:
            player.add_stat("game", "Minutes", 1)
        offgoalie = offense.get_line("G")[0]
        offgoalie.add_stat("game", "Minutes", 1)
        shooter = oline.pop(random.randrange(len(oline)))
        shooter.add_stat("game", "Shots", 1)
        defgoalie = dline[-1]
        if result == "Goal":
            shooter.add_stat("game", "Goals", 1)
            defgoalie.add_stat("game", "Goals Allowed", 1)
            offense.add_stat("game", "Goals For", 1)
            defense.add_stat("game", "Goals Against", 1)
            numassists = random.randrange(3)
            for i in range(numassists):
                p = oline.pop(random.randrange(len(oline)))
                p.add_stat("game", "Assists", 1)
        elif result == "Miss":
            defgoalie.add_stat("game", "Saves", 1)
        
    def play_minute(self):
        """Simulate a minute of play.
        
        Choose which team is offense and which is defense. Get the players
        on the ice. Simulate a shot. Process the result.
        
        Args:
            None
            
        Returns:
            None
        """
        teams = [self.team1, self.team2]
        offense = teams.pop(random.randrange(2))
        defense = teams[0]
        oline, dline = self.get_lines(offense, defense)
        result = self.simulate_shot(oline, dline)
        self.process_result(offense, defense, oline, dline, result)
        
    def play_period(self):
        """For 20 minutes, play a minute.
        
        Args:
            None
            
        Returns:
            None
        """
        for i in range(20):
            self.play_minute()
        
    def play_overtime(self):
        """Play sudden death overtime for 5 minutes (non-playoff) or 10000
        (playoff).
        
        Note that we avoid doing while True for playoff because if the game
        goes 10000 minutes without a goal, that will indicate we need to 
        adjust the goal-scoring somehow but will not crash.
        
        Args:
            None
        
        Returns:
            None
        """
        if self.era == "playoff":
            minutes = 10000
        else:
            minutes = 5
        for i in range(minutes):
            self.play_minute()
            if self.team1.get_stat("game", "Goals For") != self.team2.get_stat("game", "Goals For"):
                return
                
    def determine_game_result(self):
        """Determine the winner and set the game stats accordingly.
        
        Args:
            None
            
        Returns:
            None
        """
        if self.team1.get_stat("game", "Goals For") > self.team2.get_stat("game", "Goals For"):
            self.team1.add_stat("game", "Wins", 1)
            self.team2.add_stat("game", "Losses", 1)
        elif self.team1.get_stat("game", "Goals For") < self.team2.get_stat("game", "Goals For"):
            self.team1.add_stat("game", "Losses", 1)
            self.team2.add_stat("game", "Wins", 1)
        else:
            self.team1.add_stat("game", "Ties", 1)
            self.team2.add_stat("game", "Ties", 1)
            
    def update_stats(self):
        """Update team and player stats from the game to the wider era.
        
        Args:
            None
        
        Returns:
            None
        """
        if self.era == "playoff":
            self.team1.update_stats("game", "playoff")
            self.team2.update_stats("game", "playoff")
            for player in self.team1.get_full_roster() + self.team2.get_full_roster():
                player.update_stats("game", "playoff")
        else:
            self.team1.update_stats("game", "season")
            self.team2.update_stats("game", "season")
            for player in self.team1.get_full_roster() + self.team2.get_full_roster():
                player.update_stats("game", "season")
    
    def play_game(self):
        """Play the game.
        
        Play three periods. If the game is tied, play overtime. Update the 
        stats.
        
        Args:
            None
            
        Returns:
            None
        """
        for i in range(3):
            self.play_period()
        if self.team1.get_stat("game", "Goals For") == self.team2.get_stat("game", "Goals For"):
            self.play_overtime()
        self.determine_game_result()
        self.update_stats()
        