import random
import Player, Stats

class Team(object):
    
    """The Team class.
    
    This is the class representing a team of players. It keeps statistics,
    the roster, and lines. All team names are in the teams class variable.
    
    Class Attributes:
        teams: A set containing each team name used.
        
    Attributes:
        name: A string representing the team's name.
        roster: A Roster object representing the players (and through it, the
            lines) on the team.
        stats: A TeamStats object containing the stats the player has
            accumulated for each 'era': Season, Playoffs, Career.
            
    Future:
        Awards
        Season Results
        Keep Season stats year over year
        Keep Playoff stats year over year
        Coaching
        Team Ratings
        Team Philosophy
    """
    
    teams = set()
    
    def __init__(self, name):
        """Inits a Team with a name.
        
        Initializes a team with blank stats and an empty roster.
        
        Args:
            name: A string representing the team's name.
            
        Returns:
            None
        """
        if name in Team.teams:
            raise NameError("Name already used")
        self.name = name
        Team.teams.add(name)
        self.roster = Roster()
        self.stats = Stats.TeamStats()
        
    def __repr__(self):
        """Repr of the Team.
        
        Returns a string representation of the Team, with its name.
        
        Args:
            None
            
        Returns:
            A String containing the class and the team's name.
        """
        return "%s(%r)" % (self.__class__, self.name)
        
    def add_player(self, player):
        """Adds the given player to the team's roster.
        
        Note that the player is added to the Scratch line. This also sets the 
        player's team attribute to this team.
        
        Args:
            player: The Player object to be added to the team's roster.
        
        Returns:
            None
        """
        self.roster.add_player(player)
        player.team = self
        
    def remove_player(self, player):
        """Removes the given player from the team's roster.
        
        Note that the player is also removed from any lines they are on, and 
        that the player's team attribute is set to None.
        
        Args:
            player: The Player object to be removed from the team's roster.
            
        Returns:
            None
        """
        self.roster.remove_player(player)
        player.team = None
        
    def get_full_roster(self):
        """Gets a list of the players on the team's roster.
        
        The list is sorted by position, C, LW, RW, D, G.
        
        Args:
            None
         
        Returns:
            A list of Player objects, sorted by position C, LW, RW, D, G.
        """
        return self.roster.get_full_roster()
        
    def show_roster(self):
        """Get a printable string showing the team's roster.
        
        The roster is sorted by position and shows player name, position, and
        rating.
        
        Args:
            None
        
        Returns:
            A string suitable for printing showing the name, position, and 
            rating of every player on the team's roster.
        """
        return self.roster.show_roster()
        
    def generate_default_lines(self):
        """Set naive lines.
        
        This sets the team's lines by ordering the positions by rating and 
        assigning the top C to L1, second C to L2, etc. If there are not enough   
        players at each position (4 C, LW, RW, 6 D, 2 G), it will print an 
        error message and return without altering the lines.
        
        Args:
            None
            
        Returns:
            None
        """
        self.roster.generate_default_lines()
        
    def set_line(self, line, players):
        """Set the given line to the given players.
        
        Args:
            line: A string containing the name of a line - L1, L2, L3, L4, D1, 
                D2, D3, G; for the offensive lines, we expect them to be in the
                order C, LW, RW (the players do not have to have these 
                positions, but that's where they will play on the line).
            players: A list containing the Player objects to be on the given
                line.
                
        Returns:
            None
        """
        self.roster.set_line(line, players)
        
    def get_line(self, line):
        """Get a list of the players on the given line.
        
        For offensive lines, the order is C, LW, RW.
        
        Args:
            line: A string for the line to get; L1, L2, L3, L4, D1, D2, D3, 
                G, Scratch
        
        Returns:
            The list of players assigned to the given line.
        """
        return self.roster.get_line(line)
        
    def show_lines(self):
        """Get a printable string showing the team's lines.
        
        This returns a string showing the offensive lines, then defensive lines,
        then goalies. For each player, it shows the player's name, position, 
        and rating.
        
        Args:
            None
        
        Returns:
            A printable string containing the team's lines.
        """
        return self.roster.show_lines()
        
    def add_stat(self, era, stat, amount):
        """Adds to the accumulated statistics for the team.
        
        Adds the given amount of the given stat to the team's statistics for
        the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to be adjusted:
                v1: Wins, Losses, Ties, Goals For, Goals Against
            amount: The amount to add to the statistic. Note that if an amount
                is to be removed (no use case in v1), then amount should be
                negative.
                
        Returns:
            None
        """
        self.stats.add_stat(era, stat, amount)
        
    def get_stat(self, era, stat):
        """Get the amount of the given stat the team has for the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to be adjusted:
                v1: Wins, Losses, Ties, Goals For, Goals Against
        
        Returns:
            The amount of the given stat the team has for the given era.
        """
        return self.stats.get_stat(era, stat)
        
    def show_team_stats(self, era):
        """Get a printable string showing the team stats for the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
        
        Return:
            A printable string showing the team's stats for the given era.
        """
        return self.stats.show_stats(era)
        
    def get_statline(self, era):
        """A summary of the team's statistics for the given era.
        
        This is called by the League object when generating a league-level 
        summary of the team's statistics.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
                
        Returns:
            A string displaying a summary version of the team's statistics for
            the given era.
        """
        return self.stats.get_statline(era) #TODO: v2
        
    def get_roster_total(self, era, stat):
        """Get the total number of the given stat in the given era for the 
        players on the roster.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to total.
                v1: Goals, Assists, Minutes, Shots, Saves, Goals Allowed
                
        Returns:
            An integer that is the total amount of the given stat that each 
            player on the roster has in the given era.
        """
        return self.roster.get_stat_total(era, stat)
        
    def get_roster_statline(self, era):
        """Get a string with roster totals for player statistics to include in
        show_roster_stats.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
        
        Returns:
            A string formatted to match show_rosters_stats containing totals for
            the player statistics on the roster.
        """
        s = self.name.ljust(33)
        goals = self.get_roster_total(era, "Goals")
        assists = self.get_roster_total(era, "Assists")
        points = goals + assists
        shots = self.get_roster_total(era, "Shots")
        minutes = self.get_roster_total(era, "Minutes")
        saves = self.get_roster_total(era, "Saves")
        goals_allowed = self.get_roster_total(era, "Goals Allowed")
        s += str(goals).rjust(6)
        s += str(assists).rjust(6)
        s += str(points).rjust(6)
        s += str(shots).rjust(6)
        s += str(minutes).rjust(7)
        s += str(saves).rjust(8)
        s += str(goals_allowed).rjust(7)
        return s
        
    def show_roster_stats(self, era):
        """Get a printable string showing the team's roster's stats for the 
        given era.
        
        This gets the statistics for each player, line by line, with the team's
        statistics following. For v1, what's shown is: name, rating, goals, 
        assists, points, shots, minutes played, saves, and goals allowed.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
                
        Returns:
            A printable string showing the statistics for each player on the 
            team's roster.
        """
        s = "Player".ljust(25)
        s += "Pos  Rat     G     A     P  Shots     Min     Saves     GA"
        for p in self.get_full_roster():
            s += "\n"
            s += p.name.ljust(25)
            s += p.position.rjust(3)
            s += str(p.rating).rjust(5)
            s += p.get_statline(era)
        s += "\n" + self.get_roster_statline(era)
        return s

    def age_year(self):
        self.stats.update_career_stats()
        for player in self.get_full_roster():
            player.age_year()
            
            
class Roster(object):
    
    """The Roster class.
    
    This is the class representing the collection of players on a team. It keeps
    the team's lines.
    
    Class Attributes:
        None
        
    Attributes:
        roster: A dictionary whose keys are strings representing positions (C, 
        LW, RW, D, G) and whose values are lists containing the players on the
        roster at that position. Those lists are sorted by player rating.
    """
    
    def __init__(self):
        """Inits a Roster with no players and empty lines.
        
        Args:
            None
            
        Returns:
            None
        """
        self.roster = self.get_initial_roster()
        self.lines = Lines()
        
    def get_initial_roster(self):
        """Get blank roster.
        
        Args:
            None
        
        Returns:
            A dictionary whose keys are strings representing positions (C, LW, 
            RW, D, G) and whose values are empty lists.
        """
        positions = ["C", "LW", "RW", "D", "G"]
        roster = {pos: [] for pos in positions}
        return roster
        
    def add_player(self, player):
        """Adds the given player to the roster.
        
        Note that the player is added to the Scratch line. This also sets the 
        player's team attribute to this team.
        
        Args:
            player: The Player object to be added to the team's roster.
        
        Returns:
            None
        """
        self.roster[player.position].append(player)
        self.sort_position(player.position)
        self.lines.update_scratches(self.get_full_roster())
        
    def remove_player(self, player):
        """Removes the given player from the roster.
        
        The player is also removed from any lines he is on.
        
        Args:
            player: The player to be removed.
            
        Returns:
            None
        """
        if player not in self.get_full_roster():
            print("Player not on roster; cannot remove")
            return
        self.roster[player.position].remove(player)
        self.lines.remove_player(player)
        
    def sort_position(self, position):
        """Sorts the given position by rating, highest to lowest.
        
        Args:
            position: A string representing the position to be sorted, of C, 
            LW, RW, D, G.
            
        Returns:
            None
        """
        self.roster[position].sort(key = lambda x: x.rating, reverse = True)
        
    def get_full_roster(self):
        """Get a sorted list of players on the roster.
        
        Args:
            None
        
        Returns:
            A list of players on the roster, in the order of rating by position
            in the position order C, LW, RW, D, G
        """
        positions = ["C", "LW", "RW", "D", "G"]
        r = []
        for pos in positions:
            r += self.roster[pos]
        return r
        
    def show_roster(self):
        """Get a printable string of the list of players on the roster.
        
        Shows the players' name, position, and rating, sorted by position.
        
        Args:
            None
            
        Returns:
            A string showing each player's name, position, and rating.
        """
        s = "Player".ljust(25)
        s += "Pos".rjust(5)
        s += "Rat".rjust(5)
        r = self.get_full_roster()
        for player in r:
            ps = "\n"
            ps += player.name.ljust(25)
            ps += player.position.rjust(5)
            ps += str(player.rating).rjust(5)
            s += ps
        return s
    
    def generate_default_lines(self):
        """Set naive lines.
        
        This sets the team's lines by ordering the positions by rating and 
        assigning the top C to L1, second C to L2, etc. If there are not enough   
        players at each position (4 C, LW, RW, 6 D, 2 G), it will print an 
        error message and return without altering the lines.
        
        Args:
            None
            
        Returns:
            None
        """
        self.lines.generate_default_lines(self.roster)
        
    def set_line(self, line, players):
        """Set the given line to the given players.
        
        Args:
            line: A string containing the name of a line - L1, L2, L3, L4, D1, 
                D2, D3, G; for the offensive lines, we expect them to be in the
                order C, LW, RW (the players do not have to have these 
                positions, but that's where they will play on the line).
            players: A list containing the Player objects to be on the given
                line.
                
        Returns:
            None
        """
        self.lines.set_line(line, players)
        self.lines.update_scratches(self.get_full_roster())
        
    def get_line(self, line):
        """Get a list of the players on the given line.
        
        For offensive lines, the order is C, LW, RW.
        
        Args:
            line: A string for the line to get; L1, L2, L3, L4, D1, D2, D3, 
                G, Scratch
        
        Returns:
            The list of players assigned to the given line.
        """
        return self.lines.get_line(line)
        
    def show_lines(self):
        """Get a printable string showing the team's lines.
        
        This returns a string showing the offensive lines, then defensive lines,
        then goalies. For each player, it shows the player's name, position, 
        and rating.
        
        Args:
            None
        
        Returns:
            A printable string containing the team's lines.
        """
        return self.lines.show_lines()
        
    def get_stat_total(self, era, stat):
        """Get the total of the roster's players' given stat in the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to total.
                v1: Goals, Assists, Minutes, Shots, Saves, Goals Allowed
        
        Returns:
            An integer representing the total of each player on the roster's
            given stat for the given era.
        """
        total = 0
        r = self.get_full_roster()
        for player in r:
            total += player.get_stat(era, stat)
        return total


class Lines(object):
    
    def __init__(self):
        """Inits a Lines with no players and empty lines.
        
        Args:
            None
            
        Returns:
            None
        """
        self.lines = self.get_initial_lines()
        
    def get_initial_lines(self):
        """Gets blank lines.
        
        The lines are a dictionary whose keys are strings for the lines:
        L1, L2, L3, L4, D1, D2, D3, G, Scratch
        and whose values are lists. For the D and G, order is irrelevant. For 
        the offensive lines, the order is C, LW, RW.
        
        Args:
            None
            
        Returns:
            A dictionary whose keys are strings for lines and whose values are
            lists (in C, LW, RW order for the offense).
        """
        lines = {"L1": [], "L2": [], "L3": [], "L4": [], "D1": [], "D2": [], "D3": [], "G": [], "Scratch": []}
        return lines
        
    def generate_default_lines(self, roster):
        """Sets the lines with the given roster as the default.
        
        The default for offense is L1 is the top C, LW, RW, then similar for 
        L2, L3, L4. For defense, the top 2 are D1, then similar for D2, D3.
        For G, it is the top goalie.
        
        Args:
            roster: The list of players to be put into lines.
            
        Returns:
            None
        """
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
        self.lines["G"] = [roster["G"][0]]
        self.lines["Scratch"] = roster["C"][4:] + roster["LW"][4:] + roster["RW"][4:] + roster["D"][6:] + roster["G"][1:]
        
    def remove_player(self, player):
        """Remove the given player from all lines.
        
        If the player is found in a line, replace him with None. If the player
        is not in any lines, there is no problem.
        
        Args:
            player: The Player to be removed.
            
        Returns:
            None
        """
        for line in self.lines:
            for p in self.lines[line]:
                if p == player:
                    self.lines[line][self.lines[line].index(p)] = None
        
    def set_line(self, line, players):
        """Set the given line to the given list of players.
        
        For an offensive line, the players will be put in positions C, LW, RW
        in that order. Order is irrelevant for defensive lines or the goalie.
        
        Args:
            line: A string representing the line to be changed. The lines are
                L1, L2, L3, L4, D1, D2, D3, G.
            players: A list of Players to be put on the line. For offense,
                the players will be put in C, LW, RW.
                
        Returns:
            None
        """
        self.lines[line] = players
        
    def update_scratches(self, players):
        """Put any players on roster but not on any other line in Scratch.
        
        Args:
            players: The list of {layers to be put checked.
            
        Returns:
            None
        """
        to_remove = set()
        for line in self.lines:
            if line != "Scratch":
                if (type(self.lines[line])) == "Player":
                    print(line)
                for p in self.lines[line]:
                    to_remove.add(p)
        for p in to_remove:
            players.remove(p)
        self.lines["Scratch"] = players
        
    def get_line(self, line):
        """Get a list of the players on the given line.
        
        For offensive lines, the order is C, LW, RW.
        
        Args:
            line: A string for the line to get; L1, L2, L3, L4, D1, D2, D3, 
                G, Scratch
        
        Returns:
            The list of players assigned to the given line.
        """
        return self.lines[line]
        
    def show_lines(self):
        """Get a printable string showing each line.
        
        The lines are in the order L1, L2, L3, L4, D1, D2, D3, G, Scratch.
        
        Args:
            None
        
        Returns:
            A printable string showing the players on each line.
        """
        line_ids = ["L1", "L2", "L3", "L4", "D1", "D2", "D3", "G", "Scratch"]
        s = ""
        for l in line_ids:
            s += "\n" + l
            for p in self.lines[l]:
                s += "\n"
                s += p.name.ljust(25)
                s += p.position.ljust(5)
                s += str(p.rating)
        return s


def get_team_names():
    """Generate the list of team names.
    
    This opens the file TeamNames.txt and uses the names inside to create a
    global variable, team_name_list. We expect TeamNames.txt to have one
    name per line, each of which is a plural team name. This is called
    when this module is imported or ran.
    
    Args:
        None
        
    Returns:
        None
       
    Raises:
        FileNotFoundError: the file TeamNames.txt was not in the directory
    """
    global team_name_list
    try:
        with open('TeamNames.txt', 'r') as f:
            team_name_list = [line.rstrip() for line in f]
    except FileNotFoundError:
        print("TeamNames.txt not found - random teams cannot be created")
        return
    random.shuffle(team_name_list)
       
def generate_name():
    """Pop a team name from team_name_list.
    
    This is expected to be used to generate a random team name in 
    create_random_team. If there are no more team names remaining,
    then this will print that fact and return with no name.
    
    Args:
        None
    
    Returns:
        A string to be used as a random team name.
    """
    global team_name_list
    if len(team_name_list) == 0:
        print("No more team names found - random teams cannot be created")
        return
    tname = team_name_list.pop()
    return tname
           
def create_random_team():
    """Generate a random team.
    
    This creates a random team with 4 each of C, LW, RW, 6 D, and 2 G.
    
    Args:
        None
        
    Returns:
        A randomly generated Team.
    """
    name = generate_name()
    if name == None:
        return
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
   
get_team_names()