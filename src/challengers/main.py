from game import (
    Card,
    Level,
    Set,
    Player,
    Tournament,
)


PLAYERS = [
    Player(1, "P1"),
    Player(2, "P2"),
    Player(3, "P3"),
    Player(4, "P4"),
    Player(5, "P5"),
    Player(6, "P6"),
    Player(7, "P7"),
    Player(8, "P8"),
]


# 48 cards =  6*8
def load_cards():
    cards1 = Card.create(1, "Test1", Set.CITY, Level.A, power=3, amount=4)
    cards2 = Card.create(2, "Test2", Set.HAUNTED_HOUSE, Level.A, power=5, amount=4)
    cards3 = Card.create(3, "Test3", Set.OUTER_SPACE, Level.A, power=4, amount=3)
    cards4 = Card.create(4, "Test4", Set.SHIPWRECK, Level.A, power=1, amount=5)
    cards5 = Card.create(5, "Test5", Set.CASTLE, Level.A, power=2, amount=2)
    cards6 = Card.create(6, "Test6", Set.FILM_STUDIO, Level.A, power=2, amount=3)
    cards7 = Card.create(7, "Test7", Set.FUNFAIR, Level.A, power=3, amount=3)
    cards8 = Card.create(8, "Test8", Set.SHIPWRECK, Level.A, power=4, amount=4)
    cards9 = Card.create(9, "Test8", Set.CITY, Level.A, power=4, amount=2)
    cards10 = Card.create(10, "Test8", Set.CASTLE, Level.A, power=2, amount=7)
    cards11 = Card.create(11, "Test8", Set.OUTER_SPACE, Level.A, power=2, amount=3)
    cards12 = Card.create(12, "Test8", Set.OUTER_SPACE, Level.A, power=3, amount=2)
    cards13 = Card.create(13, "Test8", Set.FILM_STUDIO, Level.A, power=5, amount=3)
    cards14 = Card.create(14, "Test8", Set.FUNFAIR, Level.A, power=6, amount=3)
    print(cards1[0])
    print(cards2[0])
    print(cards3[0])
    print(cards4[0])
    print(cards5[0])
    print(cards6[0])
    print(cards7[0])
    print(cards8[0])
    print(cards9[0])
    print(cards10[0])
    print(cards11[0])
    print(cards12[0])
    print(cards13[0])
    print(cards14[0])


if __name__ == "__main__":
    load_cards()

    tournament = Tournament(8)

    for player in PLAYERS:
        tournament.set_new_player(player)

    tournament.initialize_trays()

    for player in tournament.players:
        for _ in range(6):
            player.draw_card(tournament.trays[Level.A])
            player.shuffle_deck()

    winner = tournament.play()

    tournament.print_scores()
