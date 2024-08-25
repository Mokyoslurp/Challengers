import pygame

import socket
import pickle

from challengers.server.server import SERVER_IP, PORT
from challengers.client.gui import MenuScreen


BUFSIZE = 4096


class Client:
    def __init__(self):
        pygame.font.init()

        self.window_width = 700
        self.window_height = 700

        self.window: pygame.Surface = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption("Client")

        self.menu_screen = MenuScreen()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (SERVER_IP, PORT)

    def connect(self):
        try:
            self.socket.connect(self.server_address)

            # Here we use decode() since the first message received is the player id
            return self.socket.recv(BUFSIZE).decode()

        except:  # noqa: E722
            pass

    def send(self, data):
        try:
            # serialization with str.encode() and str.decode() can be done for strings instead of pickle
            self.socket.send(str.encode(data))
            return pickle.loads(self.socket.recv(BUFSIZE))
        except socket.error as e:
            print(e)

    def draw(self):
        self.window.fill((128, 128, 128))

        self.menu_screen.draw()

        pygame.display.update()

    def run(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)

            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    ...


if __name__ == "__main__":
    client = Client()
    client.run()
