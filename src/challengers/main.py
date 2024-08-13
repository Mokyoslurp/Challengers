from game import (
    Card,
    Level,
    Set,
    Tray,
    Player,
    Park,
)


def load_cards():
    cards1 = Card.create(1, "Test1", Set.CITY, Level.A, power=3, amount=4)
    cards2 = Card.create(2, "Test2", Set.HAUNTED_HOUSE, Level.A, power=5, amount=2)
    cards3 = Card.create(3, "Test3", Set.OUTER_SPACE, Level.A, power=4, amount=3)
    cards4 = Card.create(4, "Test4", Set.SHIPWRECK, Level.A, power=1, amount=5)
    cards5 = Card.create(5, "Test5", Set.CASTLE, Level.A, power=2, amount=2)
    cards6 = Card.create(6, "Test6", Set.FILM_STUDIO, Level.A, power=2, amount=1)
    cards7 = Card.create(7, "Test7", Set.FUNFAIR, Level.A, power=3, amount=1)
    cards8 = Card.create(8, "Test8", Set.SHIPWRECK, Level.A, power=4, amount=2)
    # cards9 = Card.create(9, "Test8", Set.CITY, Level.A, power=4, amount=2)
    # cards10 = Card.create(10, "Test8", Set.CASTLE, Level.A, power=2, amount=5)
    # cards11 = Card.create(11, "Test8", Set.OUTER_SPACE, Level.A, power=2, amount=3)
    # cards12 = Card.create(12, "Test8", Set.OUTER_SPACE, Level.A, power=3, amount=2)
    # cards13 = Card.create(13, "Test8", Set.FILM_STUDIO, Level.A, power=5, amount=1)
    # cards14 = Card.create(14, "Test8", Set.FUNFAIR, Level.A, power=6, amount=1)
    print(cards1[0])
    print(cards2[0])
    print(cards3[0])
    print(cards4[0])
    print(cards5[0])
    print(cards6[0])
    print(cards7[0])
    print(cards8[0])
    # print(cards9[0])
    # print(cards10[0])
    # print(cards11[0])
    # print(cards12[0])
    # print(cards13[0])
    # print(cards14[0])


def initialize_trays():
    trays: dict[Level, Tray] = {}
    for level in [Level.A, Level.B, Level.C]:
        tray = Tray(level)
        tray.prepare()
        trays[level] = tray
    return trays


if __name__ == "__main__":
    load_cards()
    trays = initialize_trays()

    for tray in trays.values():
        print(tray)

    player1 = Player(0, "P1")
    player2 = Player(1, "P2")

    print(player1)
    print(player2)

    for _ in range(10):
        player1.draw_card(trays[Level.A])
        player2.draw_card(trays[Level.A])

    player1.shuffle_deck()
    player2.shuffle_deck()

    print(player1)
    print(player2)

    park = Park(0)
    park.assign_players(player1, player2)

    print("\n\nGame started\n")
    winner = park.play_game()

    print(player1)
    print(player2)
