import socket

from server import SERVER, PORT


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (SERVER, PORT)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()

        except:  # noqa: E722
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


if __name__ == "__main__":
    network = Network()
    print(network.send("hello"))
    print(network.send("tout marche bien navette"))
