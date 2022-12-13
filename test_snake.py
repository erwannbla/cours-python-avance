import snakeClass

def test_snake_type():
    S=snakeClass.Snake
    assert type(S.getdirection())==list

def test_direction():
    S=snakeClass.Snake
    assert S.getdirection()== snakeClass.Game.Getdirection()

def test_change_direction():
    S = snakeClass.Snake
    S.NewDirection((1,0))
    assert S.getdirection()==(1,0) 

def test_avance_snake():
    S=snakeClass.Snake
    S_n= S.avance_snake
    assert len(S_n)==len(S)+1

def test_nouvelle_position_fruit():
    F=snakeClass.Fruit
    assert F.getposition() != snakeClass.Damier.position_fruit()

