import pygame
from pathlib import Path
import socket as s

from challengers.server import (
    build_request,
    decode_response,
    RESPONSE_LENGTH,
    Command,
)
from challengers.client.gui import MenuScreen, BattleScreen
from challengers.client.gui.components import Interface
from challengers.client.gui.game import CardFront
from challengers.game import CardList, Tournament
from challengers.game.data import TELEMETRY


GAME_DATA_PATH = Path(__file__).parent.parent / "game" / "data"
CARD_DATA_FILE = "cards.json"
CARD_DATA_FILE_PATH = GAME_DATA_PATH / CARD_DATA_FILE


class Client:
    def __init__(self):
        pygame.font.init()

        self.window_width = 1600
        self.window_height = 900

        self.window: pygame.Surface = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption("Client")

        self.menu_screen = MenuScreen()
        self.battle_screen = BattleScreen()
        self.gui: list[Interface] = [self.menu_screen]

        self.socket: s.socket
        self.server_address: tuple[str, int]

        self.is_running = False

        self.status: Tournament.Status = Tournament.Status.NONE
        self.is_connected: bool = False

        self.player_id: int
        self.opponent_id: int

        self.player_name: str

        self.unique_cards_list = CardList.get_unique_cards_list(CARD_DATA_FILE_PATH)

    def send(self, command: Command, data: int = 0):
        try:
            # Send the command
            self.socket.send(build_request(command, data))
            # Receive the length of the packet to come
            response_length = decode_response(self.socket.recv(RESPONSE_LENGTH))[0]
            # Send acknowledgement of the packet length
            self.socket.send(build_request(Command.BLANK, response_length))
            # Receive full response
            response = decode_response(self.socket.recv(response_length * 8))

            if TELEMETRY:
                print(f"Command {command.name} sent. Received {response}.")
            return response
        except s.error as e:
            print(e)

    def connect(self):
        if not self.is_connected:
            try:
                self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
                self.socket.connect(self.server_address)
                self.is_connected = True

                self.player_id = self.socket.recv(RESPONSE_LENGTH)

                if TELEMETRY:
                    print(f"Connected to : {self.server_address[0]}, {self.server_address[1]}")

                self.send(Command.CONNECT)

            except s.error as e:
                print(e)

                if TELEMETRY:
                    print("Failed to connect to server")

    def disconnect(self):
        if self.is_connected:
            self.send(Command.LEAVE)
            self.socket.shutdown(s.SHUT_RDWR)
            self.socket.close()
            self.is_connected = False
            self.player_id = None
            self.is_running = False

            if TELEMETRY:
                print("Successfully disconnected from server")

    def draw(self):
        self.window.fill((128, 128, 128))

        for element in self.gui:
            element.draw(self.window)

        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                pygame.quit()

            for interface in self.gui:
                interface.handle_event(event)

        new_status = self.get_tournament_status()

        # Changing status
        if self.status != Tournament.Status.ROUND and new_status == Tournament.Status.ROUND:
            self.gui = [self.battle_screen]
            self.status = new_status

        if self.status == Tournament.Status.ROUND:
            new_self_played_cards = self.get_self_played_cards()
            new_opponent_played_cards = self.get_opponent_played_cards()
            new_self_bench = self.get_self_bench()
            new_opponent_bench = self.get_opponent_bench()

            if new_self_played_cards != self.battle_screen.self_played_cards:
                self.battle_screen.self_played_cards = new_self_played_cards

                self.battle_screen.park.reset_played_cards(1)
                for data in self.battle_screen.self_played_cards:
                    card = CardFront(0, 0, card=data)
                    self.battle_screen.park.add_played_card(1, card)

            if new_opponent_played_cards != self.battle_screen.opponent_played_cards:
                self.battle_screen.opponent_played_cards = new_opponent_played_cards

                self.battle_screen.park.reset_played_cards(2)
                for data in self.battle_screen.opponent_played_cards:
                    card = CardFront(0, 0, card=data)
                    self.battle_screen.park.add_played_card(2, card)

            if new_self_bench != self.battle_screen.self_bench:
                self.battle_screen.self_bench = new_self_bench

                for i, data in enumerate(self.battle_screen.self_bench):
                    self.battle_screen.park.reset_bench(1, i)
                    card = CardFront(0, 0, card=data)
                    self.battle_screen.park.add_bench_card(1, i, card)

            if new_opponent_bench != self.battle_screen.opponent_bench:
                self.battle_screen.opponent_bench = new_opponent_bench

                for i, data in enumerate(self.battle_screen.opponent_bench):
                    self.battle_screen.park.reset_bench(2, i)
                    card = CardFront(0, 0, card=data)
                    self.battle_screen.park.add_bench_card(2, i, card)

    def ready(self):
        if self.is_connected:
            response = self.send(Command.READY)
            return response

    def get_tournament_status(self):
        if self.is_connected:
            return Tournament.Status(self.send(Command.GET_STATUS)[0])

    def play_card(self):
        if self.is_connected:
            card_id = self.send(Command.PLAY_CARD)[0]
            if card_id:
                return self.unique_cards_list[card_id]

    def draw_card(self, tray: int):
        if self.is_connected:
            return self.get_cards_list_from_ids(self.send(Command.DRAW_CARD, tray))

    def discard_card(self, card_id: int):
        if self.is_connected:
            return self.send(Command.DISCARD_CARD, card_id)

    def end_card_management(self):
        if self.is_connected:
            return self.send(Command.END_CARD_MANAGEMENT)

    def get_self_deck(self):
        if self.is_connected:
            return self.get_cards_list_from_ids(self.send(Command.GET_SELF_DECK))

    def get_self_bench(self):
        if self.is_connected:
            return self.get_cards_list_from_ids(self.send(Command.GET_SELF_BENCH))

    def get_self_played_cards(self):
        if self.is_connected:
            return self.get_cards_list_from_ids(self.send(Command.GET_SELF_PLAYED_CARDS))

    def get_opponent_bench(self):
        if self.is_connected:
            return self.get_cards_list_from_ids(self.send(Command.GET_OPPONENT_BENCH))

    def get_opponent_played_cards(self):
        if self.is_connected:
            return self.get_cards_list_from_ids(self.send(Command.GET_OPPONENT_PLAYED_CARDS))

    def get_cards_list_from_ids(self, cards_ids: list[int]):
        cards = []
        for card_id in cards_ids:
            if card_id:
                cards.append(self.unique_cards_list[card_id])
        return cards

    def assign_functions(self):
        self.menu_screen.enter_server_button.on_click(self.connect)
        self.menu_screen.leave_server_button.on_click(self.disconnect)
        self.menu_screen.ready_button.on_click(self.ready)
        self.battle_screen.draw_card_button.on_click(self.play_card)

    def run(self):
        clock = pygame.time.Clock()

        self.assign_functions()

        self.is_running = True
        while self.is_running:
            clock.tick(1)

            self.update()
            self.draw()


if __name__ == "__main__":
    from challengers.server.server import SERVER_IP, PORT

    client = Client()
    client.server_address = (SERVER_IP, PORT)
    client.run()
