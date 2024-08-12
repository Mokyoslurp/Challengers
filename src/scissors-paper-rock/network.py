import socket
import pickle

from server import SERVER, PORT
from game import Game


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (SERVER, PORT)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.address)

            # Here we use decode() since the first message received is the player id
            return self.client.recv(2048).decode()

        except:  # noqa: E722
            pass

    def send(self, data) -> Game:
        try:
            # serialization with str.encode() and str.decode() can be done for strings instead of pickle
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
