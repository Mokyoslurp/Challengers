import socket
import pickle
from _thread import start_new_thread

from player import Player

# Set here your local ip address
SERVER = "192.168.0.102"
# Set here an unused port
PORT = 5050

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 255, 0))]


def threaded_client(connection: socket.socket, player_id: int):
    connection.send(pickle.dumps(players[player_id]))
    reply = ""
    while True:
        try:
            # Argument is amount of information you want to receive (bits)
            data = pickle.loads(connection.recv(2048))
            players[player_id] = data

            if not data:
                print("Disconnected")
                break
            else:
                # Replies the other player's data
                reply = players[abs(player_id - 1)]

                print("Received: ", data)
                print("Sending: ", reply)

            connection.sendall(pickle.dumps(reply))
        except:  # noqa: E722
            break

    print("Lost connection")
    connection.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((SERVER, PORT))
    except socket.error as e:
        print(e)

    current_players = 0

    # Argument is the number of client that can connect
    s.listen(2)
    print("Waiting for connection, server started!")

    while True:
        connection, address = s.accept()
        print("Connected to: ", address)

        start_new_thread(threaded_client, (connection, current_players))
        current_players += 1
