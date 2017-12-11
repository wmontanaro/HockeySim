"""
Unit tests for all modules.
"""
 
def player_tests():
    """
    Tests for the Player module.
    """
    print("Starting Player Tests")
   
    import Player
    p = Player.create_random_player()
    assert p.position in ["C", "LW", "RW", "D", "G"]
    s = p.show_profile()
    p.add_stat("game", "Goals", 10)
    assert p.get_stat("game", "Goals") == 10
    p.add_stat("season", "Assists", 5)
    assert p.get_stat("season", "Assists") == 5
    p.add_stat("playoffs", "Shots", 20)
    assert p.get_stat("playoffs", "Shots") == 20
    p.add_stat("career", "Saves", 30)
    assert p.get_stat("career", "Saves") == 30
    s = p.show_stats("game")
    s = p.show_stats("season")
    s = p.show_stats("playoffs")
    s = p.show_stats("career")
    s = p.get_statline("game")
    s = p.get_statline("season")
    s = p.get_statline("playoffs")
    s = p.get_statline("career")
    original_age = p.age
    p.age_year()
    assert p.age == original_age + 1
    assert p.rating in range(1, 100)
    assert p.get_stat("season", "Assists") == 0
    assert p.get_stat("career", "Assists") == 5
    
    print("Player Tests Passed")
    
def team_tests():
    """
    Tests for the Team module.
    """
    print("Starting Team Tests")
    
    import Team
    t = Team.create_random_team()
    r = t.get_full_roster()
    s = t.show_roster()
    t.generate_default_lines()
    s = t.show_lines()
    t.add_stat("game", "Goals For", 5)
    assert t.get_stat("game", "Goals For") == 5
    t.add_stat("season", "Wins", 10)
    assert t.get_stat("season", "Wins") == 10
    t.add_stat("playoffs", "Losses", 15)
    assert t.get_stat("playoffs", "Losses") == 15
    t.add_stat("career", "Goals Against", 20)
    assert t.get_stat("career", "Goals Against") == 20
    s = t.show_team_stats("game")
    s = t.show_team_stats("season")
    s = t.show_team_stats("playoffs")
    s = t.show_team_stats("career")
    assert t.get_roster_total("game", "Goals") == 0
    s = t.get_roster_statline("game")
    s = t.get_roster_statline("season")
    s = t.get_roster_statline("playoffs")
    s = t.get_roster_statline("career")
    s = t.show_roster_stats("season")
    t.age_year()
    assert t.get_stat("season", "Wins") == 0
    assert t.get_stat("career", "Wins") == 10
    
    import Player
    p = Player.create_random_player()
    assert len(t.get_line("Scratch")) == 1
    t.add_player(p)
    assert p.team == t
    assert len(t.get_line("Scratch")) == 2
    l = t.get_line("L1")
    l[0] = p
    t.set_line("L1", l)    
    t.remove_player(p)
    assert t.get_line("L1")[0] == None
    assert p.team == None
    
    print("Team Tests Passed")
    
def game_tests():
    """
    Tests for the Game module.
    """
    print("Starting Game Tests")
    
    import Game
    import Team
    
    #go through the tests without checking explicit results
    t1 = Team.create_random_team()
    t2 = Team.create_random_team()
    g = Game.Game(t1, t2)
    l = g.get_lines(g.team1, g.team2)
    s = g.simulate_shot(l[0], l[1])
    g.process_result(t1, t2, l[0], l[1], s)
    g.play_minute()
    g.play_period()
    g.play_overtime()
    
    #test an entire game
    t1 = Team.create_random_team()
    t2 = Team.create_random_team()
    g = Game.Game(t2, t2)
    g.play_game()
    
    #test specific results
    #TODO: player stats tracked correctly, season
    #TODO: team stats tracked correctly, season
    #TODO: overtime triggered correctly
    #TODO: player stats added to season total correctly
    #TODO: team stats added to season total correctly
    #TODO: player stats tracked correctly, playoff
    #TODO: team stats tracked correctly, playoff
    #TODO: player stats added to playoff total correctly
    #TODO: team stats added to playoff total correctly
    
    
    print("Game Tests Passed")


def __main__():
    player_tests()
    team_tests()
    
__main__()