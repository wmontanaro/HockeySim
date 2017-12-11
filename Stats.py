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

class ParentStats(object):
    
    """The Stats class.
    
    This is the class that contains statistics. It is a parent to PlayerStats
    and TeamStats.
    
    Class Attributes:
        None
        
    Attributes:
        game_stats: A dictionary whose keys are strings with stat names and
            whose values are the integer amounts of those for the game.
        season_stats: A dictionary whose keys are strings with stat names
            and whose values are the integer amounts of those for the season.
        playoff_stats: A dictionary whose keys are strings with stat names
            and whose values are the integer amounts of those for the playoff.
        career_stats: A dictionary whose keys are strings with stat names
            and whose values are the integer amounts of those for the 
            career.
        stats: A list with game_stats, season_stats, playoff_stats, and 
            career_stats.
            
    Future:
        Career playoff stats
        Stats season over season
    """
    
    def __init__(self):
        """Inits a Stats class.
        
        Args:
            None
            
        Returns:
            None
        """
        self.game_stats = self.get_blank_stats()
        self.season_stats = self.get_blank_stats()
        self.playoff_stats = self.get_blank_stats()
        self.career_stats = self.get_blank_stats()
        self.stats = {
            "game": self.game_stats, 
            "season": self.season_stats, 
            "playoff": self.playoff_stats,
            "career": self.career_stats
            }
            
    def get_blank_stats(self):
        """Get an empty stats dictionary.
        
        This is an abstract method; it must be implemented by the child
        class, as children all have different stats.
        
        Args:
            None
            
        Returns:
            A stats dictionary whose keys are strings for the stats kept
            and whose values are 0.
        
        Raises:
            NotImplementedError: This method must be overridden in the child
            class.
        """
        raise NotImplementedError("Must be implemented in child class.")
            
    def add_stat(self, era, stat, amount):
        """Add the given amount to the given stat for the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to be adjusted:
                v1: Goals, Assists, Minutes, Shots, Saves, and Goals Allowed
            amount: The amount to add to the statistic. Note that if an amount
                is to be removed (no use case in v1), then amount should be
                negative.
        
        Returns:
            None
        """
        self.stats[era][stat] += amount
            
    def get_stat(self, era, stat):
        """Get the amount of the given stat for the given era.
        
        Args:   
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to be returned.
                players: Goals, Assists, Minutes, Shots, Saves, Goals Allowed
                teams: Wins, Losses, Ties, Goals For, Goals Against
                
        Returns:
            An integer representing the amount of the given stat for the 
            given era.
        """
        return self.stats[era][stat]
        
    def show_stats(self, era):
        """Get a printable string of the team's stats for the given era.
        
        This is an abstract method; it must be implemented by the child
        class, as children all have different stats.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
                
        Returns:
            A printable string showing the statistics for the given era.
            
        Raises:
            NotImplementedError: This method must be overridden in the child
            class.
        """
        raise NotImplementedError("Must be implemented in child class.")
        
    def get_statline(self):
        """Get a string summary of the stats for the given era.
        
        This is an abstract method; it must be implemented by the child
        class, as children all have different stats.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
        
        Returns:
            A string summary of the stats for the given era.
        
        Raises:
            NotImplementedError: This method must be overridden in the child
            class.
        """
        raise NotImplementedError("Must be implemented in child class.")
        
    def zero_stats(self, era):
        for stat in self.stats[era]:
            self.stats[era][stat] = 0
            
    def update_stats(self, fromera, toera):
        """Add stats in the given fromera to the given toera.
        
        Args:
            fromera: A string for the era to get statistics from:
                game, season, playoff, career
            toera: A string for the era to add statistics to:
                game. season, playoff, career
        
        Returns;
            None
        """
        for stat in self.stats[fromera]:
            self.add_stat(toera, stat, self.stats[fromera][stat])
        self.zero_stats(fromera)
        

class PlayerStats(ParentStats):
    
    """The PlayerStats class.
    
    This is the class that contains the statistics for a Player. For v1, it
    includes the eras season, playoff, and career. It includes the statistics
    Goals, Assists, Minutes, Shots, Saves, and Goals Allowed.
    
    Class Attributes:
        None
        
    Attributes:
        season_stats: A dictionary whose keys are strings with stat names
            and whose values are the integer amounts of those for the season.
        playoff_stats: A dictionary whose keys are strings with stat names
            and whose values are the integer amounts of those for the playoff.
        career_stats: A dictionary whose keys are strings with stat names
            and whose values are the integer amounts of those for the 
            player's career.
        stats: A list with season_stats, playoff_stats, and career_stats.
        
    Future:
        More stats
        Team the stats were gained with
        Career playoff stats
        Stats year over year
        Separate goalie and player stats
        Ability to get various derived stats
        Relevant stats for each era
    """
    
    def __init__(self):
        """Inits a PlayerStats class.
        
        Args:
            None
            
        Returns:
            None
        """
        super().__init__()
        
    def get_blank_stats(self):
        """Get a blank stats.
        
        For v1, the stats kept are Goals, Assists, Minutes, Shots, Saves,
        and Goals Allowed.
        
        Args:
            None
        
        Returns:
            A dictionary whose keys are strings that are stat names and whose
            values are 0.
        """
        stats = {"Goals": 0, "Assists": 0, "Minutes": 0, "Shots": 0, "Saves": 0, "Goals Allowed": 0}
        return stats
        
    def show_stats(self, era):
        """Get a printable string of the player's stats for the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
                
        Returns:
            A printable string showing the player's statistics for the given
            era.
        """
        cur_stats = self.stats[era]
        s = ""
        points = cur_stats["Goals"] + cur_stats["Assists"]
        s += "GAP: " + str(cur_stats["Goals"]) + "-" + str(cur_stats["Assists"]) + "-" + str(points)
        s += "\nShots: " + str(cur_stats["Shots"])
        s += "\nSaves: " + str(cur_stats["Saves"]) + "-" + str(cur_stats["Saves"] + cur_stats["Goals Allowed"])
        s += "\nMinutes: " + str(cur_stats["Minutes"])
        return s
        
    def get_statline(self, era):
        """Get a string summary of the player's stats for the given era.
        
        This is called by Team when generating the roster stats.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
        
        Returns:
            A string summary of the player's stats for the given era.
        """
        goals = self.stats[era]["Goals"]
        assists = self.stats[era]["Assists"]
        points = goals + assists
        s = str(goals).rjust(6)
        s += str(assists).rjust(6)
        s += str(points).rjust(6)
        s += str(self.stats[era]["Shots"]).rjust(6)
        s += str(self.stats[era]["Minutes"]).rjust(7)
        s += str(self.stats[era]["Saves"]).rjust(8)
        s += str(self.stats[era]["Goals Allowed"]).rjust(7)
        return s
        

class TeamStats(ParentStats):
    
    """The TeamStats class.
    
    This is the class that contains the statistics for a Team. For v1, it
    includes the eras season, playoff, and career. It includes the statistics
    Wins, Losses, Ties, Goals For, and Goals Against.
    
    Class Attributes:
        None
        
    Attributes:
        season_stats: A dictionary whose keys are strings with stat names
            and whose values are the integer amounts of those for the season.
        playoff_stats: A dictionary whose keys are strings with stat names
            and whose values are the integer amounts of those for the playoff.
        career_stats: A dictionary whose keys are strings with stat names
            and whose values are the integer amounts of those for the 
            player's career.
        stats: A list with season_stats, playoff_stats, and career_stats.
        
    Future:
        More stats
        Career playoff stats
        Stats year over year
        Ability to get various derived stats
        Relevant stats for each era
    """
    
    def __init__(self):
        """Inits a TeamStats class.
        
        Args:
            None
            
        Returns:
            None
        """
        super().__init__()
        
    def get_blank_stats(self):
        """Get a blank stats.
        
        For v1, the stats kept are Wins, Losses, Ties, Goals For, and Goals
        Against.
        
        Args:
            None
        
        Returns:
            A dictionary whose keys are strings that are stat names and whose
            values are 0.
        """
        stats = {"Wins": 0, 
            "Losses": 0, 
            "Ties": 0, 
            "Goals For": 0, 
            "Goals Against": 0}
        return stats
        
    def show_stats(self, era):
        """Get a printable string of the team's stats for the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
                
        Returns:
            A printable string showing the team's statistics for the given
            era.
        """
        s = ""
        s += "Record: " 
        s += str(self.stats[era]["Wins"])
        s += "-" 
        s += str(self.stats[era]["Losses"]) 
        s += "-" 
        s += str(self.stats[era]["Ties"])
        points = 2 * self.stats[era]["Wins"] + self.stats[era]["Ties"]
        s += "\nPoints: " + str(points)
        s += "\nGoals For: " + str(self.stats[era]["Goals For"])
        s += "\nGoals Against: " + str(self.stats[era]["Goals Against"])
        return s
        
    def get_statline(self):
        """Get a string summary of the team's stats for the given era.
        
        This is called by League when generating the league-wide stats.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
        
        Returns:
            A string summary of the team's stats for the given era.
        """
        pass #TODO: v2
                