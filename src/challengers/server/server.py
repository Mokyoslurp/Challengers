import socket as s
import threading
from pathlib import Path
from typing import Union

from challengers.game import Tournament, Player
from challengers.server import (
    build_response,
    decode_request,
    REQUEST_LENGTH,
    Command,
)

SERVER_IP = "localhost"
PORT = 5050


class Server:
    def __init__(self, tournament: Tournament):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)

        self.tournament_thread: threading.Thread
        self.client_threads: list[threading.Thread] = []

        self.is_running: bool = False
        self.is_ready: bool = False

        self.player_count: int = 0
        # Player address and id
        self.players_ids: dict[int, int] = {}
        self.players_names: dict[int, str] = {}
        self.player_ready: dict[int, bool] = {}

        self.tournament = tournament

    def add_player(self, player_id: int, player_name: str):
        player = Player(player_id, player_name)
        self.tournament.add_player(player)

        return player

    def send(self, socket: s.socket, data: Union[int, list[int]]):
        if isinstance(data, list):
            length = len(data)
        else:
            length = 1

        try:
            pre_response, response = build_response(data, length)
            # Send length of packet to come
            socket.send(pre_response)
            # Wait for acknowledgment
            command, data = self.receive(socket)
            if command == Command.BLANK and data == length:
                # Send the data
                socket.send(response)
            else:
                # Send nothing if acknowledgement wrong
                _, response = build_response(0)
                socket.send(response)
        except s.error as e:
            print(e)

    def receive(self, socket: s.socket) -> tuple[Command, int]:
        request = socket.recv(REQUEST_LENGTH)
        command, data = decode_request(request)
        return command, data

    def run(self):
        try:
            self.socket.bind((SERVER_IP, PORT))
        except s.error as e:
            print(e)

        # Argument is the number of client that can connect
        self.socket.listen(self.tournament.number_of_players)
        print("Waiting for connection, server started!")

        self.is_running = True
        while self.is_running:
            while self.is_running and not self.is_ready:
                client, address = self.socket.accept()
                print("Connected to:", address)

                self.players_ids[address[1]] = self.player_count
                self.player_ready[self.player_count] = False

                client_thread = threading.Thread(target=self.client_thread, args=(client, address))
                client_thread.start()
                self.client_threads.append(client_thread)

                self.player_count += 1

                if self.player_count == self.tournament.number_of_players:
                    self.is_ready = True

            if self.player_count != self.tournament.number_of_players:
                self.is_ready = False

            # TODO: PB because of robot players
            if len(self.tournament.players) == self.tournament.number_of_players:
                self.tournament_thread = threading.Thread(target=self.tournament.play)
                self.tournament_thread.start()

                while not self.tournament.is_ended():
                    pass

                self.tournament_thread.join()

                if self.tournament.winner:
                    print(f"Winner is {self.tournament.winner}")
                    self.tournament.print_scores()

                for client_thread in self.client_threads:
                    client_thread.join()

    def client_thread(self, socket: s.socket, address):
        # Send player id to the player
        _, response = build_response(self.player_count)
        socket.send(response)
        player_connected = True

        player_id = self.players_ids[address[1]]
        while player_connected:
            try:
                command, data = self.receive(socket)
                reply = 0

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
                            if not self.player_ready[player_id]:
                                player_name = f"P{player_id}"
                                player = self.add_player(player_id, player_name)

                                self.players_names[player_id] = player_name
                                self.player_ready[player_id] = True

                                print(f"{player} connected\n")

                                reply = 1

                    case Command.READY:
                        if self.tournament.status == Tournament.Status.PREPARE:
                            if not player.is_ready:
                                player.is_ready = True
                                print(f"{player} is ready\n")

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
                            if not player.has_managed_cards:
                                tray_choice = data
                                draw_levels = list(self.tournament.available_draws.keys())

                                if tray_choice < len(draw_levels):
                                    draw_level = draw_levels[tray_choice]
                                    cards = self.tournament.make_draw(player, draw_level)
                                    # TODO: Return Card id (and implement cards ids)
                                    if cards:
                                        reply = [card.id for card in cards]

                    case Command.END_CARD_MANAGEMENT:
                        if self.tournament.status == Tournament.Status.DECK:
                            if not player.has_managed_cards:
                                player.has_managed_cards = True
                                print(f"Player {player} managed cards\n")

                                reply = 1

                    case Command.LEAVE:
                        player_connected = False

                        reply = 1

                    case _:
                        break

                self.send(socket, reply)
                print("To", address, ":", reply)

            except:  # noqa: E722
                break

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
