import pygame

import socket as s
import pickle


from challengers.server.server import SERVER_IP, PORT, BUFSIZE
from challengers.client.gui import MenuScreen, BattleScreen
from challengers.client.gui.components import Interface
from challengers.client.gui.game import CardFront


class Client:
    def __init__(self, player_name: str = ""):
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
        self.server_address = (SERVER_IP, PORT)

        self.is_running = True

        self.is_ready: bool = False
        self.is_battling: bool = False
        self.is_connected: bool = False

        self.player_id: int = None
        self.opponent_id: int = None

        self.player_name = player_name

    def connect(self):
        if not self.is_connected:
            try:
                self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
                self.socket.connect(self.server_address)
                self.is_connected = True

                # Here we use decode() since the first message received is the player id
                self.player_id = int(self.socket.recv(BUFSIZE).decode())
                print("Successfully connected")

            except s.error as e:
                print(e)
                print("Failed to connect to server")
                return None

        return self.player_id

    def disconnect(self):
        if self.is_connected:
            self.socket.shutdown(s.SHUT_RDWR)
            self.socket.close()
            self.is_connected = False
            self.player_id = None
            self.is_ready = False
            print("Successfully disconnected from server")
            return True
        print("Can't disconnect if not connected")
        return False

    def send(self, data):
        try:
            # serialization with str.encode() and str.decode() can be done for strings instead of pickle
            self.socket.send(str.encode(data))
            # TODO: Buffer size to small for entire server: what infos to send ?
            return pickle.loads(self.socket.recv(BUFSIZE))
        except s.error as e:
            print(e)

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

        if self.is_ready:
            self.opponent_id = self.send("get opponent")
            if self.opponent_id:
                self.is_ready = False
                self.gui = [self.battle_screen]
                self.is_battling = True

        # TODO: Request one action at a time to avoid instant change of the interface
        # TODO: Request only missing data to avoid reloading all the screen every frame
        if self.is_battling:
            self.battle_screen.park.reset_played_cards(1)
            self.battle_screen.park.reset_played_cards(2)

            self_bench = self.send("get player " + str(self.player_id) + " bench")
            i = 0
            for data in self_bench:
                self.battle_screen.park.reset_bench(1, i)
                card = CardFront(0, 0, card=data)
                self.battle_screen.park.add_bench_card(1, i, card)
                i += 1

            opponent_bench = self.send("get player " + str(self.opponent_id) + " bench")
            i = 0
            for data in opponent_bench:
                self.battle_screen.park.reset_bench(2, i)
                card = CardFront(0, 0, card=data)
                self.battle_screen.park.add_bench_card(2, i, card)
                i += 1

            self_played_cards = self.send("get player " + str(self.player_id) + " played")
            for data in self_played_cards:
                card = CardFront(0, 0, card=data)
                self.battle_screen.park.add_played_card(1, card)

            opponent_played_cards = self.send("get player " + str(self.opponent_id) + " played")
            for data in opponent_played_cards:
                card = CardFront(0, 0, card=data)
                self.battle_screen.park.add_played_card(2, card)

    def ready(self):
        if self.is_connected and not self.is_ready:
            self.player_name = self.menu_screen.player_name_text_field.text
            self.send("ready " + self.player_name)
            self.is_ready = True

    def play_card(self):
        if self.is_connected:
            self.send("play")

    def assign_functions(self):
        self.menu_screen.enter_server_button.on_click(self.connect)
        self.menu_screen.leave_server_button.on_click(self.disconnect)
        self.menu_screen.ready_button.on_click(self.ready)
        self.battle_screen.draw_card_button.on_click(self.play_card)

    def run(self):
        clock = pygame.time.Clock()

        self.assign_functions()

        while self.is_running:
            clock.tick(60)

            self.update()
            self.draw()


if __name__ == "__main__":
    client = Client("TestName")
    client.run()
