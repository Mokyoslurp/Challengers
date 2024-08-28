import pygame

import socket as s
import pickle

from challengers.server.server import SERVER_IP, PORT, BUFSIZE
from challengers.client.gui import MenuScreen


class Client:
    def __init__(self):
        pygame.font.init()

        self.window_width = 800
        self.window_height = 800

        self.window: pygame.Surface = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption("Client")

        self.menu_screen = MenuScreen()

        self.socket: s.socket
        self.server_address = (SERVER_IP, PORT)

        self.is_running = True

        self.is_connected: bool = False
        self.player_id = None

    def connect(self):
        if not self.is_connected:
            try:
                self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
                self.socket.connect(self.server_address)
                self.is_connected = True

                # Here we use decode() since the first message received is the player id
                return int(self.socket.recv(BUFSIZE).decode())

            except s.error as e:
                print(e)
                return None

        return self.player_id

    def disconnect(self):
        if self.is_connected:
            self.socket.shutdown(s.SHUT_RDWR)
            self.socket.close()
            self.is_connected = False
            return True
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

        self.menu_screen.draw(self.window)

        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                if not self.is_connected:
                    if self.menu_screen.enter_server_button.click(mouse_position):
                        self.player_id = self.connect()
                        if self.player_id:
                            print("Successfully connected as P" + str(self.player_id))
                        else:
                            print("Failed to connect to server")

                else:
                    if self.menu_screen.test_button.click(mouse_position):
                        data = self.send("test")
                        print(data)

                    if self.menu_screen.leave_server_button.click(mouse_position):
                        if self.disconnect():
                            self.player_id = None
                            print("Successfully disconnected from server")
                        else:
                            print("Can't disconnect if not connected")

    def run(self):
        clock = pygame.time.Clock()

        while self.is_running:
            clock.tick(60)

            self.update()
            self.draw()


if __name__ == "__main__":
    client = Client()
    client.run()
