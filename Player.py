import random
import Stats
 
class Player(object):
    
    """The Player class.
    
    Player(name, age, position, rating, team = None)
    
    This is the class representing a hockey player. For v1, it includes
    all positions, skaters and goalies. There is a single skill rating.
    Players age, but do not retire. All names are in the used_names class
    variable.
    
    Class Attributes:
        used_names: A set containing each player name ever used.
        
    Attributes:
        name: A string representing the player's first and last name, separated
            by a space.
        age: An integer representing the player's age.
        position: A string representing the player's position; should be one of
            C, LW, RW, D, G (not enforced here).
        rating: An integer in [0, 100) (not enforced here) representing the
            player's skill.
        team: A Team object (or None) representing the team the player is on;
            this is unused in v1.
        stats: A PlayerStats object containing the statistics the player has
            accumulated for each 'era': Season, Playoff, Career.
            
    Future:
        Keep playoff stats year over year
        Keep season stats year over year
        Note which team stats were with
        Awards
        Better aging
        Retirement
        More ratings
        Separate Goalies and Skaters/All positions
    """
   
    used_names = set()
   
    def __init__(self, name, age, position, rating, team = None):
        """Inits Player with name, age, position, rating.
        
        Initializes a Player with blank stats.
        
        Args:
            name: A string representin the player's first and last name 
                separated by a space.
            age: An integer representing the player's age.
            position: A string we expect to contain one of C, LW, RW, D, or G
                that represents the player's position.
            rating: An integer we expect to be in [0,100) representing the
                player's skill.
            team: A Team object or None representing the team the player is on.
            stats: A Stats.PlayerStats object containing the player's
                statistics for each 'era' (season, playoff, career).
        
        Returns:
            None
        """
        while name in Player.used_names:
            name += " Jr"
        self.name = name
        Player.used_names.add(name)
        self.age = age
        self.position = position
        self.rating = rating
        self.team = team
        self.stats = Stats.PlayerStats()
        
    def __repr__(self):
        """Repr of the Player.
        
        Returns a representation of the Player, with its name.
        
        Args:
            None
            
        Returns:
            A string containing the class and the Player's name.
        """
        return "%s(%r)" % (self.__class__, self.name)
        
    def show_profile(self):
        """Get a printable summary of the player's information.
        
        This shows the player's attributes and all of their statistics.
        
        Args:
            None
            
        Returns:
            A printable string displaying all of the player's attributes,
            including their statistics for the season and career.
        """
        s = ""
        s += "Player: " + self.name + ", " + str(self.age) + ", " + self.position
        s += "\nTeam: " + str(self.team)
        s += "\nRating: " + str(self.rating)
        s += "\n\nSeason: "
        s += "\n" + self.show_stats("season")
        s += "\n\nCareer: "
        s += "\n" + self.show_stats("career")
        return s
        
    def add_stat(self, era, stat, amount):
        """Adds to the accumulated statistics for the player.
        
        Adds the given amount of the given stat to the player's statistics for
        the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to be adjusted:
                v1: Goals, Assists, Minutes, Shots, Saves, Goals Allowed
            amount: The amount to add to the statistic. Note that if an amount
                is to be removed (no use case in v1), then amount should be
                negative.
                
        Returns:
            None
        """
        self.stats.add_stat(era, stat, amount)
        
    def get_stat(self, era, stat):
        """Get the amount of the given stat the player has for the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to be adjusted:
                v1: Goals, Assists, Minutes, Shots, Saves, Goals Allowed
        
        Returns:
            The amount of the given stat the player has for the given era.
        """
        return self.stats.get_stat(era, stat)
    
    def show_stats(self, era):
        """Get a printable version of the player's statistics for the given era.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
        
        Returns:
            A printable string displaying the player's statistics for the given
            era.
        """
        return self.stats.show_stats(era)
        
    def get_statline(self, era):
        """A summary of the player's statistics for the given era.
        
        This is called by the Team object when generating a team-level summary
        of the team's statistics.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
                
        Returns:
            A string displaying a summary version of the player's statistics for
            the given era.
        """
        return self.stats.get_statline(era)
        
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
        self.stats.update_stats(fromera, toera)
       
    def age_year(self):
        """Completes the year for the player.
        
        This adds a year to the player's age, adjusts the player's rating by
        a random amount in [-5, 6) (capped by [0, 100)), and updates the 
        player's stats - this adds their season stats to their career stats and 
        resets their season stats.
        
        Args:
            None
            
        Returns:
            None
        """
        self.age += 1
        self.rating += random.randrange(-5,6)
        if self.rating < 0:
            self.rating = 0
        if self.rating > 99:
            self.rating = 99
        self.update_stats("season", "career")

 
def get_possible_names():
    """Generate the list of player names.
    
    This opens the file PlayerNames.txt and uses the names inside to create a
    global variable, player_name_list. We expect PlayerNames.txt to have one
    name per line, each of which is suitable for a first name. This is called
    when this module is imported or ran.
    
    Args:
        None
        
    Returns:
        None
       
    Raises:
        FileNotFoundError: the file PlayerNames.txt was not in the directory
    """
    global player_name_list
    try:
        with open('PlayerNames.txt', 'r') as f:
            player_name_list = [line.rstrip() for line in f]
    except FileNotFoundError:
        print("PlayerNames.txt not found - random players cannot be created")
       
def generate_name():
    """Create a random name for a new player.
    
    This chooses two names from the global variable player_name_list and 
    combines them to generate a new name for a player.
    
    Args:
        None
        
    Returns:
        A string meant to be used as a player's name (first name and last name
        separated by a space).
    """
    global player_name_list
    fn = random.choice(player_name_list)
    ln = random.choice(player_name_list)
    name = fn + " " + ln
    return name
           
def create_random_player(pos = None):
    """Create a random player.
    
    This generates a random player with a random position unless one is 
    specified. The age will be in [18, 40] and the rating in [40, 90).
    
    Args:
        pos = None: This is a string representing the player's position; if none
        is given, a random position is chosen. Positions are: C, LW, RW, D, G.
        
    Returns:
        A Player object.
    """
    age = random.randrange(18,40)
    if not pos:
        pos = random.choice(["C", "LW", "RW", "D", "G"])
    rating = random.randrange(40, 90)
    name = generate_name()
    player = Player(name, age, pos, rating)
    return player
   
get_possible_names()