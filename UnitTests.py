'''
Unit tests for all modules.
'''
 
def player_tests():
    '''
    Tests for the Player module.
    '''
    print("Starting Player Tests")
   
    import Player
    #initialize p1
    p1 = Player.Player("p1", 23, "C", 75)
    #check initial stats
    assert p1.stats.stats["Goals"] == 0
    assert p1.stats.stats["Assists"] == 0
    assert p1.stats.stats["Minutes"] == 0
    assert p1.stats.stats["Shots"] == 0
    #check add_stat for each stat
    p1.stats.add_stat("Goals", 2)
    assert p1.stats.stats["Goals"] == 2
    p1.stats.add_stat("Assists", 3)
    assert p1.stats.stats["Assists"] == 3
    p1.stats.add_stat("Minutes", 18)
    assert p1.stats.stats["Minutes"] == 18
    p1.stats.add_stat("Shots", 5)
    assert p1.stats.stats["Shots"] == 5
    #check age_year
    p1.age_year()
    assert p1.age == 24
    assert p1.rating in range(70,81)
    #create random player
    p2 = Player.create_random_player()
    
    print("Player Tests Passed")
    
def team_tests():
    '''
    Tests for the Team module.
    '''
    print("Starting Team Tests")
    
    import Team
    #initialize t1
    t1 = Team.Team("t1")
    #check initial stats
    assert t1.stats.stats["Wins"] == 0
    assert t1.stats.stats["Losses"] == 0
    assert t1.stats.stats["Ties"] == 0
    assert t1.stats.stats["Goals For"] == 0
    assert t1.stats.stats["Goals Against"] == 0
    #check add_stat for each stat
    t1.stats.add_stat("Wins", 5)
    assert t1.stats.stats["Wins"] == 5
    t1.stats.add_stat("Losses", 2)
    assert t1.stats.stats["Losses"] == 2
    t1.stats.add_stat("Ties", 3)
    assert t1.stats.stats["Ties"] == 3
    t1.stats.add_stat("Goals For", 17)
    assert t1.stats.stats["Goals For"] == 17
    t1.stats.add_stat("Goals Against", 21)
    assert t1.stats.stats["Goals Against"] == 21
    
    
    print("Team Tests Passed")
    

def __main__():
    player_tests()
    team_tests()
    
__main__()