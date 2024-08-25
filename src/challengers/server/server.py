import socket as s
import pickle
from threading import Thread


SERVER_IP = "192.168.1.79"
PORT = 5050

BUFSIZE = 4096


class Server:
    def __init__(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)

        self.threads: list[Thread] = []

        self.is_running: bool = True

        self.player_count: int = 0

    def run(self):
        try:
            self.socket.bind((SERVER_IP, PORT))
        except s.error as e:
            print(e)

        # Argument is the number of client that can connect
        self.socket.listen()
        print("Waiting for connection, server started!")

        while self.is_running:
            client, address = self.socket.accept()
            print("Connected to:", address)

            self.player_count += 1
            thread = Thread(target=self.client_thread, args=(client, address))
            thread.start()
            self.threads.append(thread)

            # TODO: Join threads after client disconnected

    def client_thread(self, socket: s.socket, address):
        socket.send(str(self.player_count).encode())
        reply = ""
        while True:
            try:
                # Argument is amount of information you want to receive (bits)
                data = socket.recv(BUFSIZE).decode()

                if not data:
                    break
                else:
                    if data == "test":
                        print("test")

                reply = "the game"
                socket.sendall(pickle.dumps(reply))

            except:  # noqa: E722
                break

        print("Lost connection to:", address)
        socket.close()
        self.player_count -= 1


if __name__ == "__main__":
    server = Server()
    server.run()
