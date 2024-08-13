from game import (
    Card,
    Level,
    Set,
    Tray,
    Player,
)


def load_cards():
    cards1 = Card.create(0, "Test1", Set.CITY, Level.A, amount=4)
    cards2 = Card.create(1, "Test2", Set.HAUNTED_HOUSE, Level.A, amount=2)
    print(cards1[0])
    print(cards2[0])


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

    for _ in range(3):
        player1.draw_card(trays[Level.A])
        player2.draw_card(trays[Level.A])

    player1.shuffle_deck()
    player2.shuffle_deck()

    print(player1)
    print(player2)
