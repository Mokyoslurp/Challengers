import socket
import pickle

from server import SERVER, PORT
from player import Player


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (SERVER, PORT)
        self.player: Player = self.connect()

    def get_player(self) -> Player:
        return self.player

    def connect(self):
        try:
            self.client.connect(self.address)
            # serialization with str.encode() and str.decode() can be done for strings instead of pickle
            return pickle.loads(self.client.recv(2048))

        except:  # noqa: E722
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
