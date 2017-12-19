import random
import Game

class League(object):
    
    """The League class.
    
    This is the class that represents a league. It contains teams, tracks their
    schedule, and contains league-wide measures like standings and team stats. 
    It also contains seasons and playoffs.
    
    Class Attributes:
        conf_names: The list of strings which are conference names in a leauge
            (American and National).
        div_names: The list of strings which are division names in a conference
            (North, South, East, West).
        
    Attributes:
        teams: The list of Teams in the league (we expect exactly 32).
        team_align: A dictionary in the form {Conf: {Div: [Teams in the Div]}}
        schedule: The regular season Schedule object for the current season.
        date: A three-element list of integers representing the current year,
            day, and game (all 0-based).
            
    Future:
        Year over year records saved
        Awards
        Drafts
        Retirement
        Contracts/Free Agency
        Injuries
        Player Records
        Team Records
        Dates to Match IRL Schedules
        Team Stats in Standings
        Tiebreakers
        Malleable Conferences/Divisions
        Schedules for different sizes of league
    """

    conf_names = ["American", "National"]
    div_names = ["North", "South", "East", "West"]
    
    def __init__(self, teams):
        """Inits a League class.
        
        Args:
            teams: A list of 32 Team objects.
            
        Returns:
            None
        """
        self.teams = teams
        self.team_align = self.get_team_alignment()
        self.date = [0, 0, 0] #year, day, game
        self.season = Season(self.teams)
        self.playoff = None
        
        
    def get_team_alignment(self):
        """Take the list of teams and get the dictionary of conferences and
        divisions.
        
        Args:
            None
            
        Returns:
            A list of teams in their divisions in their conferences.
        """
        team_align = {
            "American": {
                "North": self.teams[:4], 
                "South": self.teams[4:8],
                "East": self.teams[8:12],
                "West": self.teams[12:16] },
            "National": {
                "North": self.teams[16:20],
                "South": self.teams[20:24],
                "East": self.teams[24:28],
                "West": self.teams[28:] }
                }
        return team_align
        
    def start_new_season(self):
        """Get a new regular season.
        
        Args:
            None
        Returns:
            None
        """
        self.season = Season(self.teams)
    
    def advance_date(self):
        """Move the date one game forward.
        
        We assume 16 games per regular season day (day < 80). We assume 8 games
        per playoff rd 1 day (day < 88), 4 per playoff rd 2 day (day < 96), 2
        per playoff rd 3 day (day < 104), and 1 per playoff rd 4 day 
        (day < 112).
        
        Args:
            None
            
        Returns:
            None
        """
        d = self.date
        if d[1] < 80:
            if d[2] < 15:
                d[2] += 1
            else:
                d[2] = 0
                d[1] += 1
                if d[1] == 80:
                    print("start playoff rd 1")
                    self.start_playoffs()
        elif d[1] < 87:
            if d[2] < 7:
                d[2] += 1
            else:
                d[2] = 0
                d[1] += 1
                if d[1] > 83:
                    self.update_playoffs()
                if d[1] == 87:
                    print("start playoff rd 2")
                    self.start_next_playoff_round()
        elif d[1] < 94:
            if d[2] < 3:
                d[2] += 1
            else:
                d[2] = 0
                d[1] += 1
                if d[1] > 90:
                    self.update_playoffs()
                if d[1] == 94:
                    print("start playoff rd 3")
                    self.start_next_playoff_round()
        elif d[1] < 101:
            if d[2] == 0:
                d[2] += 1
            else:
                d[2] = 0
                d[1] += 1
                if d[1] > 97:
                    self.update_playoffs()
                if d[1] == 101:
                    print("start playoff rd 4")
                    self.start_next_playoff_round()
        elif d[1] < 108:
            d[1] += 1
            if d[1] > 104:
                self.update_playoffs()
            if d[1] == 108:
                self.end_season()
        
    def get_next_game(self):
        """Get a list of two teams to play in the next game.
        
        Args:
            None
        
        Returns:
            A list of two teams that are scheduled to play next.
        """
        if self.date[1] < 80:
            return self.season.get_next_game(self.date)
        else:
            return self.playoff.get_next_game(self.date)
        
    def play_next_game(self):
        """Simulate the next game on the schedule and advance the day.
        
        Args:
            None
        
        Returns:
            None
        """
        matchup = self.get_next_game()
        if matchup != [None, None]:
            if self.date[1] < 80:
                g = Game.Game(matchup[0], matchup[1])
            else:
                g = Game.Game(matchup[0], matchup[1], era = "playoff")
            g.play_game()
        self.advance_date()
        
    def compare_dates(self, date1, date2):
        """Get the boolean if date1 is larger than date2.
        
        Args:
            date1: A list of three integers representing a year, day, and game.
            date2: A list of three integers representing a year, day, and game.
            
        Returns:
            True if date1 > date2, False if date1 < date2, None if date1
            == date2.
        """
        if date1[0] > date2[0]:
            return True
        elif date1[0] < date2[0]:
            return False
        else:
            if date1[1] > date2[1]:
                return True
            elif date1[1] < date2[1]:
                return False
            else:
                if date1[2] > date2[2]:
                    return True
                elif date1[2] < date2[2]:
                    return False
                else:
                    return None
        
    def simulate_to_day(self, enddate):
        """Simulate games and offseason until enddate.
        
        Args:
            enddate: A list of three integers representing the year, day, and
                game to simulate until.
        
        Returns:
            None
        """
        while self.compare_dates(enddate, self.date):
            self.play_next_game()
            
    def get_playoff_teams(self, conf):
        """For the given conference, get the ordered list of playoff teams.
        
        We take the division winners as the top four seeds, then the next four
        teams from the conference. There is no tie breaker.
        
        Args:
            conf: The conference to get playoff teams for.
            
        Returns:
            A list of Teams in their playoff seed rankings,
        """
        div_winners = []
        non_div_winners = []
        for div in League.div_names:
            r = self.order_teams_by_record(self.team_align[conf][div])
            div_winners.append(r.pop(0))
            non_div_winners += r
        seeds = self.order_teams_by_record(div_winners)
        wildcard_rank = self.order_teams_by_record(non_div_winners)
        seeds += wildcard_rank[:4]
        return seeds
        
    def start_playoffs(self):
        """Finish regular season tasks and initiate the playoffs.
        
        For v1, there are no regular season tasks to finish.
        
        Args:
            None
            
        Returns:
            None
        """
        am_teams = self.get_playoff_teams("American")
        na_teams = self.get_playoff_teams("National")
        self.playoff = Playoff(am_teams, na_teams)
        
    def update_playoffs(self):
        """Determine if any of the scheduled playoff games for this round are
        now unnecessary.
        
        Any unnecessary games remain on the schedule but as [None, None].
        
        Args:
            None
        
        Returns:
            None
        """
        self.playoff.update_playoffs(self.date)
        
    def start_next_playoff_round(self):
        """Start the next playoff round.
        
        Args:
            None
            
        Returns:
            None
        """
        self.playoff.get_next_round()
        
    def order_teams_by_record(self, teams):
        #TODO: v2 - order by points
        """Take a list of Teams and order them by their regular season record.
        
        Specifically, we order them by number of regular season wins.
        
        Args:
            teams: A list of Teams
            
        Returns:
            The list of Teams sorted by number of regular season wins.
        """
        ranking = sorted(teams, 
                        key = lambda x: x.get_stat("season", "Wins"), 
                        reverse = True)
        return ranking
        
    def show_standings(self):
        """Get a printable string of the standings for the league.
        
        Args:
            None
        
        Returns:
            A printable string of the standings for every team in the league
            in order of Wins, sorted by conference and division.
        """
        s = ""
        for conf in League.conf_names:
            s += conf + "\n"
            for div in League.div_names:
                s += div + "\n"
                div_rank = self.order_teams_by_record(self.team_align[conf][div])
                for team in div_rank:
                    s += team.name.ljust(14) 
                    s += str(team.get_stat("season", "Wins"))
                    s += "-"
                    s += str(team.get_stat("season", "Losses"))
                    s += "-"
                    s += str(team.get_stat("season", "Ties"))
                    s += "\n"
                s += "\n"
        return s
        
    def get_league_leaders(self, era, stat):
        """Get a list of the Players on a team in order from most to least of 
        the given stat for the given era.
        
        Note that we do not filter out skaters for goalie stats.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to get the leaders for:
                v1: Goals, Assists, Minutes, Shots, Saves, and Goals Allowed
                
        Returns:
            A list of Players in order from most to least of the given stat for
            the given era.
        """
        players = []
        for team in self.teams:
            players += team.get_full_roster()
        ranking = sorted(players, 
                        key = lambda x: x.get_stat(era, stat), 
                        reverse = True)
        return ranking
        
    def show_league_leaders(self, era, stat, n):
        """Get a printable string showing the top n players for the given
        era in the given stat.
        
        Note that we only consider players on a team for v1. Note that we do
        not filter out skaters for goalie stats. Neither do we label the line
        numbers.
        
        Args:
            era: A string for the era to get statistics for:
                game, season, playoff, career
            stat: The statistic to get the leaders for:
                v1: Goals, Assists, Minutes, Shots, Saves, and Goals Allowed
            n: The number of players to show.
            
        Returns:
            A printable string showing the n leaders' name, team, and amount of
            the given stat.
        """
        ranking = self.get_league_leaders(era, stat)
        if n == float('inf'):
            leaders = ranking
        else:
            leaders = ranking[:n]
        s = "Player".ljust(25)
        s += "Team".rjust(14)
        s += stat.rjust(8)
        s += "\n"
        for player in leaders:
            s += player.name.ljust(25)
            s += str(player.team).rjust(14)
            s += str(player.get_stat(era, stat)).rjust(8)
            s += "\n"
        return s
        
    def show_league_stats(self):
        #TODO: v2
        pass
        
    def end_season(self):
        """Perform end of season tasks.
        
        For v1, there is no awards/offseason. So we only age year and start a
        new season.
        
        Args:
            None
        
        Returns:
            None
        """
        for team in self.teams:
            team.age_year()
        self.date[0] += 1
        self.date[1] = 0
        self.date[2] = 0
        self.playoff = None
        print("Ending season " + str(self.date[0]))
        self.start_new_season()
        

class Season(object):
    
    """The Season class.
    
    This class is a container around a season. It keeps track of the schedule
    and has season-specific items in it.
    
    Class Attributes:
        conf_names: The list of strings which are conference names in a leauge
            (American and National).
        div_names: The list of strings which are division names in a conference
            (North, South, East, West).
            
    Attributes:
        team_align: A dictionary in the form {Conf: {Div: [Teams in the Div]}}
        schedule: A list of lists (days) of lists (matchups) of two Teams.
        
    Future:
        Arbitrary conferences/divisions
        Arbitrary number of teams
        Year-over-year stats
        All star game
        Awards
        Player of the week/month
        Realistic dates
    """
    
    conf_names = ["American", "National"]
    div_names = ["North", "South", "East", "West"]
    
    def __init__(self, teams):
        """Inits a Season class.
        
        Args:
            team_align: A dictionary in the form 
                {Conf: {Div: [Teams in the Div]}}
                
        Returns:
            None
        """
        self.teams = teams
        self.schedule = self.get_schedule()
        
    def get_schedule(self):
        """Gets a new schedule.
        
        We assume 32 teams in 2 conferences in 4 divisions each. We play
        2 inter-conference games, 3 intra-conference games, and 4 
        intra-division games, for 80 total.
        
        Args:
            None
            
        Returns:
            A list of lists of lists, representing the season; the inner list
            is the day, the inner inner list is the matchup: two teams.
        """
        numsched = RegularSeasonSchedule()
        schedule = []
        for numday in numsched:
            schedule.append([])
            for nummatch in numday:
                schedule[-1].append([self.teams[nummatch[0]], self.teams[nummatch[1]]])
        random.shuffle(schedule)
        return schedule
        
    def get_next_game(self, date):
        """Get a list of two Teams that play on date.
        
        Args:
            date: A list of three integers, the first representing the year,
                the second the day, and the third the number game.
        
        Returns:
            A list of two Teams that play on the given date.
        """
        return self.schedule[date[1]][date[2]]
        
        
class Playoff(object):
    
    """The Playoff class.
    
    This class is a container around a playoff. It keeps track of the schedule
    and has playoff-specific items in it.
    
    Class Attributes:
        conf_names: The list of strings which are conference names in a leauge
            (American and National).
        div_names: The list of strings which are division names in a conference
            (North, South, East, West).
            
    Attributes:
        am_teams: A list of Teams in seeded order from the American conference.
        na_teams: A list of Teams in seeded order from the National conference.
        round: An integer, 1 thru 4, representing the current playoff round.
        schedule: The schedule of games for the current round.    
    """
    
    conf_names = ["American", "National"]
    div_names = ["North", "South", "East", "West"]
    
    def __init__(self, am_teams, na_teams):
        """Inits a Playoff class.
        
        Args:
            am_teams: A list of Teams in seeded order from the American 
                conference.
            na_teams: A list of Teams in seeded order from the National 
                conference.
                
        Returns:
            None
        """
        self.am_teams = am_teams
        self.na_teams = na_teams
        self.round = 1
        self.schedule = self.get_rd1_schedule()
        
    def get_rd1_schedule(self):
        """Get the schedule for the first round of the playoffs.
        
        We assume am_teams and na_teams are in seeded order. We include 'if 
        necessary' games and use a 7 game series.
        
        Args:
            None
            
        Returns:
            A list of lists of lists; the each item in the list represents a
            day and each day's lists is a two-element list of Teams to 
            represent a game.
        """
        day = [
            [self.am_teams[0], self.am_teams[7]], 
            [self.am_teams[1], self.am_teams[6]],
            [self.am_teams[2], self.am_teams[5]],
            [self.am_teams[3], self.am_teams[4]],
            [self.na_teams[0], self.na_teams[7]],
            [self.na_teams[1], self.na_teams[6]],
            [self.na_teams[2], self.na_teams[5]],
            [self.na_teams[3], self.na_teams[4]]]
        rd1 = [list(day) for i in range(7)]
        return rd1
        
    def get_rd2_schedule(self):
        """Get the schedule for the second round of the playoffs.
        
        We assume am_teams and na_teams are in seeded order and 4 Teams long
        each. We include 'if necessary' games and use a 7 game series.
        
        Args:
            None
        
        Returns:
            A list of lists of lists; the each item in the list represents a
            day and each day's lists is a two-element list of Teams to 
            represent a game.
        """
        day = [
            [self.am_teams[0], self.am_teams[3]],
            [self.am_teams[1], self.am_teams[2]],
            [self.na_teams[0], self.na_teams[3]],
            [self.na_teams[1], self.na_teams[2]]]
        rd2 = [list(day) for i in range(7)]
        return rd2
        
    def get_rd3_schedule(self):
        """Get the schedule for the third round of the playoffs.
        
        We assume am_teams and na_teams are in seeded order and 2 Teams long
        each. We include 'if necessary' games and use a 7 game series.
        
        Args:
            None
        
        Returns:
            A list of lists of lists; the each item in the list represents a
            day and each day's lists is a two-element list of Teams to 
            represent a game.
        """
        day = [
            [self.am_teams[0], self.am_teams[1]],
            [self.na_teams[0], self.na_teams[1]]]
        rd3 = [list(day) for i in range(7)]
        return rd3
        
    def get_rd4_schedule(self):
        """Get the schedule for the fourth round of the playoffs.
        
        We assume am_teams and na_teams are one Team each. We include 
        'if necessary' games and use a 7 game series.
        
        Args:
            None
        
        Returns:
            A list of lists of lists; the each item in the list represents a
            day and each day's lists is a two-element list of Teams to 
            represent a game.
        """
        day = [
            [self.am_teams[0], self.na_teams[0]]]
        rd4 = [list(day) for i in range(7)]
        return rd4
        
    def get_next_game(self, date):
        """Get a list of two teams representing the next matchup to be played.
        
        We keep the entire playoff schedule in the Playoff's schedule, so we 
        only have to subtract 80 to get the correct day.
        
        Args:
            date: A list of three integers, the first representing the year 
                (not relevant here), the second representing the day, and the
                third representing the game of the day.
                
        Returns:
            A list of two Teams that play on the given date.
        """
        return self.schedule[date[1] - 80][date[2]]
        
    def get_next_round(self):
        """Add the next playoff round's schedule to this object's schedule.
        
        Args:
            None
        
        Returns:
            None
        """
        self.round += 1
        if self.round == 2:
            self.schedule += self.get_rd2_schedule()
        elif self.round == 3:
            self.schedule += self.get_rd3_schedule()
        else:
            self.schedule += self.get_rd4_schedule()
        
    def get_matchup_score(self, team1, team2):
        """Get a dictionary of the form {team: current playoff round wins} for
        the given teams, who are assumed to be matched up against each other.
        
        Args:
            team1: The Team paired against team2 in the current playoff round.
            team2: The Team paired against team1 in the current playoff round.
            
        Returns:
            A dictionary of the form {team: current round wins} for the given
            teams.
        """
        expected_wins = 4 * (self.round - 1)
        team1_cur_wins = team1.get_stat("playoff", "Wins") - expected_wins
        team2_cur_wins = team2.get_stat("playoff", "Wins") - expected_wins
        score = {team1: team1_cur_wins, team2: team2_cur_wins}
        return score
        
    def update_playoffs(self, date):
        """Check each matchup in the current round to see if the rest of the
        games are unnecessary.
        
        If the games are unnecessary, we replace the teams in them with None.
        We use the given date to know to replace all teams following it.
        
        Args:
            date: A list of three integers, the first representing the year 
                (not relevant here), the second representing the day, and the
                third representing the game of the day.
            
        Returns:
            None
        """
        playoff_day = date[1] - 80
        games = self.schedule[-1]
        losers = []
        games_to_remove = []
        for game in games:
            if game != [None, None]:
                score = self.get_matchup_score(game[0], game[1])
                print(str(score))
                if score[game[0]] == 4:
                    losers.append(game[1])
                    games_to_remove.append(game)
                elif score[game[1]] == 4:
                    losers.append(game[0])
                    games_to_remove.append(game)
        for team in losers:
            print('lost: ' + str(team))
            if team in self.am_teams:
                self.am_teams.remove(team)
            elif team in self.na_teams:
                self.na_teams.remove(team)
        for team in self.am_teams + self.na_teams:
            print('still in: ' + str(team))
        for i in range(date[1] - 80, len(self.schedule)):
            for game in games_to_remove:
                self.schedule[i][self.schedule[i].index(game)] = [None, None]
        
    def end_playoff(self):
        """Perform end of playoff tasks.
        
        For v1, there are no awards, etc. for this. We don't even update stats.
        
        Args:
            None
        
        Returns:
            None
        """
        pass
        

def RegularSeasonSchedule():
    """Get a numeric regular season schedule for 32 teams in 4 divisions in
    two conferences.
    
    We set it so each team plays:
        4 games against teams in their division
        3 games against teams in their conference
        2 games against teams in the other conference.
    
    Args:
        None
        
    Returns:
        A list of lists of lists; the middle list represents days, and the 
        innermost list represents matchups on that day, in integers.
    """
    def get_intradiv(d):
        """Get the schedule for an intradivisional round for a division.
        
        That is, for four items, get a list of lists of lists; each middle
        list represents a day, and each innermost list represents a matchup.
        
        Args:
            d: A list of four items to be matched up.
            
        Returns:
            A list of lists of lists representing three days, each of which
            has two matchups.
        """
        s = [
            [[d[0], d[1]], [d[2], d[3]]], 
            [[d[0], d[2]], [d[1], d[3]]],
            [[d[0], d[3]], [d[1], d[2]]]
            ]
        return s
    
    def get_intradiv_round():
        """Get the schedule for an intravidisional round for the league.
        
        Args:
            None
            
        Returns:
            All of the matches for an intradivisional round for the league in
            the form of a list of lists (days) of lists (games) - two integers
            representing the matchup.
        """
        t = [i for i in range(32)]
        s = [[] for i in range(3)]
        i = 0
        while i < 32:
            games = get_intradiv(t[i:i+4])
            for j in range(3):
                s[j] += games[j]
            i += 4
        return s
        
    def get_interdiv(d1, d2):
        """Get the schedule for an interdivisional round for two divisions.
        
        That is, for the two lists of four items, get a list of lists; each
        middle list represents a day, and each innermost list represents a
        matchup.
        
        Args:
            d1: A list of four items to be matched up against d2.
            d2: A list of four items to be matched up against d1.
        
        Returns:
            A list of lists of lists representing four days, each of which has
            four matchups.
        """
        s = [
            [[d1[0], d2[0]], [d1[1], d2[1]], [d1[2], d2[2]], [d1[3], d2[3]]],
            [[d1[0], d2[1]], [d1[1], d2[2]], [d1[2], d2[3]], [d1[3], d2[0]]],
            [[d1[0], d2[2]], [d1[1], d2[3]], [d1[2], d2[0]], [d1[3], d2[1]]],
            [[d1[0], d2[3]], [d1[1], d2[0]], [d1[2], d2[1]], [d1[3], d2[2]]]
            ] 
        return s
        
    def get_interdiv_round():
        """Get the schedule for an interdivisional round for the league.
        
        Args:
            None
            
        Returns:
            All the matches for an interdivisional round for the league in the
            form of a list of lists (days) of lists (games) - two integers 
            representing the matchup.
        """
        s = [[] for i in range(12)]
        divs = [list(range(0 + 4*i, 4 + 4*i)) for i in range(8)]
        am_div_matchups = get_intradiv([0,1,2,3])
        na_div_matchups = get_intradiv([4,5,6,7])
        div_matchups = [am_div_matchups[i] + na_div_matchups[i] for i in range(3)]
        counter = 0
        for div_matchup in div_matchups:
            for pair in div_matchup:
                matches = get_interdiv(divs[pair[0]], divs[pair[1]])
                for i in range(4):
                    s[i + (4 * counter)] += matches[i]
            counter += 1
        return s
        
    def get_interconf_round():
        """Get the schedule for an interconference round for the league.
        
        Args:
            None
            
        Returns:
            All the matches for an interconference round for the league in the
            form of a list of lists (days) of lists (games) - two integers 
            representing the matchup.
        """
        s = [[] for i in range(16)]
        divs = [list(range(0 + 4*i, 4 + 4*i)) for i in range(8)]
        div_matchups = get_interdiv([0,1,2,3], [4,5,6,7])
        counter = -1
        for matchup in div_matchups:
            counter += 1
            for pair in matchup:
                matches = get_interdiv(divs[pair[0]], divs[pair[1]])
                for i in range(4):
                    s[i + (4 * counter)] += matches[i]
        return s
        
    schedule = []
    intradiv_round = get_intradiv_round()
    interdiv_round = get_interdiv_round()
    interconf_round = get_interconf_round()
    for i in range(4):
        schedule += intradiv_round
    for i in range(3):
        schedule += interdiv_round
    for i in range(2):
        schedule += interconf_round
    return schedule
    
    
def create_random_league():
    """Create a random league.
    
    This creates a random 32 team league.
    
    Args:
        None
        
    Returns:
        A league consisting of 32 randomly-generated teams consisting of 
        randomly-generated players.
    """
    import Team
    teams = [Team.create_random_team() for i in range(32)]
    l = League(teams)
    return l