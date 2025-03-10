import threading

from challengers.game import Player, Card, CardList, Level, Set, Duel


if __name__ == "__main__":
    player_1 = Player(1, "P1")
    player_2 = Player(2, "P2")

    deck = [
        Card("Abc", Set.CASTLE, Level.S, power=1),
        Card("Def", Set.CITY, Level.S, power=2),
        Card("Ijk", Set.SHIPWRECK, Level.S, power=3),
        Card("Lmn", Set.HAUNTED_HOUSE, Level.S, power=4),
    ]

    player_1.deck = CardList(deck)
    player_2.deck = CardList(deck)

    duel = Duel(player_1, player_2)

    duel_thread = threading.Thread(target=duel.play)
    duel_thread.start()

    print(f"First card by {duel.flag_owner.name}\n {duel.flag_owner.played_cards[-1]}")

    while not duel.ended.is_set():
        print(f"\nWaiting for {duel.attacking_player.name} to play\n")
        p = int(input())
        if p == 1:
            if player_1.play():
                print(f"P1 played \n{player_1.played_cards[-1]}")
        elif p == 2:
            if player_2.play():
                print(f"P2 played \n{player_2.played_cards[-1]}")

        elif p == 0:
            duel.ended.set()

    duel_thread.join()
    print(duel.winner.name)
