import socket as s
import threading
from pathlib import Path
from typing import Callable

from challengers.game.data import TELEMETRY
from challengers.game import Tournament, Player
from challengers.server import (
    send_message,
    receive_message,
    Command,
)

SERVER_IP = "localhost"
PORT = 5050


class Server:
    def __init__(self, tournament: Tournament):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)

        self.tournament_thread: threading.Thread
        self.client_threads: list[threading.Thread] = []

        self.execution_queue: list[Callable] = []

        self.is_running: bool = False
        self.is_ready: bool = False

        self.player_count: int = 0
        # Client sockets are keys to get players ids, other dict have ids as keys
        self.players_ids: dict[s.socket, int] = {}
        self.players_names: dict[int, str] = {}

        self.tournament = tournament

    def add_player(self, player_id: int, player_name: str):
        player = Player(player_id, player_name)
        self.tournament.add_player(player)

        return player

    def run(self):
        try:
            self.socket.bind((SERVER_IP, PORT))
        except s.error as e:
            print(e)

        # Argument is the number of client that can connect
        self.socket.listen(self.tournament.number_of_players)

        if TELEMETRY:
            print("Waiting for connection, server started!")

        self.is_running = True
        while self.is_running:
            while self.is_running and not self.is_ready:
                client_socket, address = self.socket.accept()

                if TELEMETRY:
                    print("Connected to:", address)

                self.players_ids[client_socket] = self.player_count

                client_thread = threading.Thread(target=self.client_thread, args=(client_socket,))
                client_thread.start()
                self.client_threads.append(client_thread)

                self.player_count += 1

                if self.player_count == self.tournament.number_of_players:
                    self.is_ready = True

            if self.player_count != self.tournament.number_of_players:
                self.is_ready = False

            # TODO: PB because of robot players
            if self.tournament.check_all_players_ready():
                while not self.tournament.is_ended():
                    if len(self.execution_queue) > 0:
                        function_to_execute = self.execution_queue.pop(0)
                        function_to_execute()

                if TELEMETRY and self.tournament.winner:
                    print(f"Winner is {self.tournament.winner}")
                    self.tournament.print_scores()

                for client_thread in self.client_threads:
                    client_thread.join()

    def client_thread(self, socket: s.socket):
        player_connected = True
        address = socket.getsockname()

        player_id = self.players_ids[socket]
        while player_connected:
            try:
                command, data = receive_message(socket)
                reply = 0

                if TELEMETRY:
                    print(f"From {address} : {command}, {data}")

                match command:
                    case Command.FORCE_END:
                        self.tournament.ended.set()
                        for duel in self.tournament.duels:
                            duel.ended.set()
                        player_connected = False

                        reply = 1

                    case Command.CONNECT:
                        if self.tournament.status == Tournament.Status.NONE:
                            if player_id not in self.players_names:
                                # TODO: Change player_name acquisition to use with data:
                                # player_name = data
                                player_name = f"P{player_id}"
                                player = self.add_player(player_id, player_name)

                                self.players_names[player_id] = player_name

                                if TELEMETRY:
                                    print(f"{player} connected\n")

                                reply = 1

                    case Command.READY:
                        if self.tournament.status == Tournament.Status.NONE:
                            if not player.is_ready:
                                player.is_ready = True

                                if TELEMETRY:
                                    print(f"{player} is ready\n")

                                if (
                                    self.tournament.check_all_players_connected()
                                    and self.tournament.check_all_players_ready()
                                ):
                                    self.execution_queue.append(self.tournament.prepare)

                                reply = 1

                    case Command.PLAY_CARD:
                        if (
                            self.tournament.status == Tournament.Status.ROUND
                            or self.tournament.status == Tournament.Status.FINAL
                        ):
                            if not player.has_played:
                                card = player.play()
                                if card:
                                    reply = card.id

                    case Command.DRAW_CARD:
                        if self.tournament.status == Tournament.Status.DECK:
                            if not player.has_managed_cards and not player.has_drawn:
                                tray_choice = data
                                draw_levels = list(self.tournament.available_draws.keys())

                                if tray_choice < len(draw_levels):
                                    draw_level = draw_levels[tray_choice]
                                    cards = self.tournament.make_draw(player, draw_level)

                                    if cards:
                                        reply = [card.id for card in cards]

                    case Command.DISCARD_CARD:
                        if self.tournament.status == Tournament.Status.DECK:
                            if not player.has_managed_cards and player.has_drawn:
                                card_id = data
                                if card_id in self.tournament.unique_cards_list:
                                    card = self.tournament.unique_cards_list[card_id]
                                    if card in player.deck:
                                        player.deck.remove(card)

                                        reply = 1

                    case Command.GET_SELF_DECK:
                        if self.tournament.status == Tournament.Status.DECK:
                            cards_ids = [card.id for card in player.deck]

                            if cards_ids:
                                reply = cards_ids

                    case Command.GET_SELF_BENCH:
                        if self.tournament.status == Tournament.Status.ROUND:
                            cards_ids = [card.id for card in player.bench]

                            if cards_ids:
                                reply = cards_ids

                    case Command.GET_SELF_PLAYED_CARDS:
                        if self.tournament.status == Tournament.Status.ROUND:
                            cards_ids = [card.id for card in player.played_cards]

                            if cards_ids:
                                reply = cards_ids

                    case Command.GET_OPPONENT_BENCH:
                        if self.tournament.status == Tournament.Status.ROUND:
                            opponent = self.tournament.get_opponent(player)
                            if opponent:
                                cards_ids = [card.id for card in opponent.bench]
                                if cards_ids:
                                    reply = cards_ids

                    case Command.GET_OPPONENT_PLAYED_CARDS:
                        if self.tournament.status == Tournament.Status.ROUND:
                            opponent = self.tournament.get_opponent(player)
                            if opponent:
                                cards_ids = [card.id for card in opponent.played_cards]

                                if cards_ids:
                                    reply = cards_ids

                    case Command.GET_STATUS:
                        reply = self.tournament.status.value

                    case Command.END_CARD_MANAGEMENT:
                        if self.tournament.status == Tournament.Status.DECK:
                            if not player.has_managed_cards:
                                player.has_managed_cards = True

                                if TELEMETRY:
                                    print(f"Player {player} managed cards\n")

                                reply = 1

                    case Command.LEAVE:
                        player_connected = False

                        reply = 1

                    case _:
                        break

                send_message(socket, Command.RESPONSE, reply)

            except:  # noqa: E722
                break

        if TELEMETRY:
            print("Lost connection to:", address)
        socket.close()
        self.player_count -= 1


if __name__ == "__main__":
    GAME_DATA_PATH = Path(__file__).parent.parent / "game" / "data"
    CARD_DATA_FILE = "cards.json"
    TROPHY_DATA_FILE = "trophies.json"

    CARD_DATA_FILE_PATH = GAME_DATA_PATH / CARD_DATA_FILE
    TROPHY_DATA_FILE_PATH = GAME_DATA_PATH / TROPHY_DATA_FILE

    tournament = Tournament(1)
    tournament.load_game_cards(CARD_DATA_FILE_PATH)
    tournament.load_game_trophies(TROPHY_DATA_FILE_PATH)

    server = Server(tournament)
    server.run()
