from pathlib import Path

import threading

from challengers.game import Tournament, Player

GAME_DATA_PATH = Path(__file__).parent.parent / "game" / "data"
CARD_DATA_FILE = "cards.json"
TROPHY_DATA_FILE = "trophies.json"

CARD_DATA_FILE_PATH = GAME_DATA_PATH / CARD_DATA_FILE
TROPHY_DATA_FILE_PATH = GAME_DATA_PATH / TROPHY_DATA_FILE


def main():
    tournament = Tournament(1)
    tournament.load_game_cards(CARD_DATA_FILE_PATH)
    tournament.load_game_trophies(TROPHY_DATA_FILE_PATH)

    player = Player(0, "P0")
    tournament.add_player(player)

    tournament_thread = threading.Thread(target=tournament.play)
    tournament_thread.start()

    while not tournament.is_ended():
        command = input()

        if tournament.is_ended():
            break

        if command == "q":
            tournament.ended.set()
            for duel in tournament.duels:
                duel.is_ended()

        elif command == "deck":
            for player in tournament.players:
                print(player.to_string())

        else:
            command = int(command)
            player = tournament.players[command]
            match tournament.status:
                case Tournament.Status.PREPARE:
                    if not player.is_ready:
                        player.is_ready = True
                        print(f"{player} is ready\n")

                case Tournament.Status.ROUND:
                    if not player.has_played:
                        player.play()

                case Tournament.Status.FINAL:
                    if not player.has_played:
                        player.play()

                case Tournament.Status.DECK:
                    choice = int(input("Which tray to draw from ?"))
                    draw_level = list(tournament.available_draws.keys())[choice]

                    if not player.has_managed_cards:
                        tournament.make_draw(player, draw_level)
                        player.has_managed_cards = True
                        print(f"Player {player} managed cards\n")

    tournament_thread.join()

    winner = tournament.winner

    if winner:
        print(f"Winner is {winner}")

        tournament.print_scores()


if __name__ == "__main__":
    main()
