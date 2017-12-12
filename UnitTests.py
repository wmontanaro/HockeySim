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
    p.add_stat("playoff", "Shots", 20)
    assert p.get_stat("playoff", "Shots") == 20
    p.add_stat("career", "Saves", 30)
    assert p.get_stat("career", "Saves") == 30
    s = p.show_stats("game")
    s = p.show_stats("season")
    s = p.show_stats("playoff")
    s = p.show_stats("career")
    s = p.get_statline("game")
    s = p.get_statline("season")
    s = p.get_statline("playoff")
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
    t.add_stat("playoff", "Losses", 15)
    assert t.get_stat("playoff", "Losses") == 15
    t.add_stat("career", "Goals Against", 20)
    assert t.get_stat("career", "Goals Against") == 20
    s = t.show_team_stats("game")
    s = t.show_team_stats("season")
    s = t.show_team_stats("playoff")
    s = t.show_team_stats("career")
    assert t.get_roster_total("game", "Goals") == 0
    s = t.get_roster_statline("game")
    s = t.get_roster_statline("season")
    s = t.get_roster_statline("playoff")
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
    
    def setup_game():
        """Create a random Game for testing."""
        t1 = Team.create_random_team()
        t2 = Team.create_random_team()
        g = Game.Game(t1, t2)
        return g
    
    #go through the tests without checking explicit results
    g = setup_game()
    l = g.get_lines(g.team1, g.team2)
    s = g.simulate_shot(l[0], l[1])
    g.process_result(g.team1, g.team2, l[0], l[1], s)
    g.play_minute()
    g.play_period()
    g.play_overtime()
    
    #test an entire game
    g = setup_game()
    g.play_game()
    
    def setup_lines(g):
        """Get top lines for team1 (off) and team2 (def) in the given game.
        
        Args:
            g: A Game with team1 and team2.
        
        Returns:
            A tuple with two entries; the first is team1's L1 + D1 and the
            second is team2's L1, D1, and G.
        """
        l1 = g.team1.get_line("L1") + g.team1.get_line("D1")
        l2 = g.team2.get_line("L1") + g.team2.get_line("D1") + g.team2.get_line("G")
        return (l1, l2)
    
    #test specific results
    
    #checking: player, team stats tracked correctly, game, miss
    g = setup_game()
    lines = setup_lines(g)
    g.process_result(g.team1, g.team2, lines[0], lines[1], "Miss")
    for player in lines[0]:
        assert player.get_stat("game", "Minutes") == 1
        assert player.get_stat("game", "Shots") in (0, 1)
        assert player.get_stat("game", "Goals") == 0
    assert g.team1.get_roster_total("game", "Minutes") == 6
    assert g.team1.get_roster_total("game", "Shots") == 1
    assert g.team1.get_roster_total("game", "Goals") == 0
    for player in lines[1]:
        assert player.get_stat("game", "Minutes") == 1
        assert player.get_stat("game", "Saves") in (0, 1)
        assert player.get_stat("game", "Goals Allowed") == 0
    assert g.team2.get_roster_total("game", "Minutes") == 6
    assert g.team2.get_roster_total("game", "Saves") == 1
    assert g.team2.get_roster_total("game", "Goals Allowed") == 0
    #checking: player, team stats tracked correctly, game, goal
    g = setup_game()
    lines = setup_lines(g)
    g.process_result(g.team1, g.team2, lines[0], lines[1], "Goal")
    for player in lines[0]:
        assert player.get_stat("game", "Minutes") == 1
        assert player.get_stat("game", "Shots") in (0, 1)
        assert player.get_stat("game", "Goals") in (0, 1)
    assert g.team1.get_roster_total("game", "Minutes") == 6
    assert g.team1.get_roster_total("game", "Shots") == 1
    assert g.team1.get_roster_total("game", "Goals") == 1
    for player in lines[1]:
        assert player.get_stat("game", "Minutes") == 1
        assert player.get_stat("game", "Saves") == 0
        assert player.get_stat("game", "Goals Allowed") in (0, 1)
    assert g.team2.get_roster_total("game", "Minutes") == 6
    assert g.team2.get_roster_total("game", "Saves") == 0
    assert g.team2.get_roster_total("game", "Goals Allowed") == 1
    #checking: player, team stats tracked correctly, game, season
    #TODO:
    g = setup_game()
    lines = setup_lines(g)
    g.process_result(g.team1, g.team2, lines[0], lines[1], "Miss")
    for player in lines[0]:
        assert player.get_stat("game", "Minutes") == 1
        assert player.get_stat("game", "Shots") in (0, 1)
        assert player.get_stat("game", "Goals") == 0
    assert g.team1.get_roster_total("game", "Minutes") == 6
    assert g.team1.get_roster_total("game", "Shots") == 1
    assert g.team1.get_roster_total("game", "Goals") == 0
    for player in lines[1]:
        assert player.get_stat("game", "Minutes") == 1
        assert player.get_stat("game", "Saves") in (0, 1)
        assert player.get_stat("game", "Goals Allowed") == 0
    assert g.team2.get_roster_total("game", "Minutes") == 6
    assert g.team2.get_roster_total("game", "Saves") == 1
    assert g.team2.get_roster_total("game", "Goals Allowed") == 0
    #checking: player, team stats tracked correctly, game, playoff
    #TODO:
    g = setup_game()
    lines = setup_lines(g)
    g.process_result(g.team1, g.team2, lines[0], lines[1], "Miss")
    for player in lines[0]:
        assert player.get_stat("game", "Minutes") == 1
        assert player.get_stat("game", "Shots") in (0, 1)
        assert player.get_stat("game", "Goals") == 0
    assert g.team1.get_roster_total("game", "Minutes") == 6
    assert g.team1.get_roster_total("game", "Shots") == 1
    assert g.team1.get_roster_total("game", "Goals") == 0
    for player in lines[1]:
        assert player.get_stat("game", "Minutes") == 1
        assert player.get_stat("game", "Saves") in (0, 1)
        assert player.get_stat("game", "Goals Allowed") in (0, 1)
    assert g.team2.get_roster_total("game", "Minutes") == 6
    assert g.team2.get_roster_total("game", "Saves") == 1
    assert g.team2.get_roster_total("game", "Goals Allowed") == 0
    #TODO: overtime triggered correctly
    
    
    print("Game Tests Passed")


def __main__():
    player_tests()
    team_tests()
    game_tests()
    
__main__()