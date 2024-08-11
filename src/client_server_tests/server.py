import socket
from _thread import start_new_thread

# Set here your local ip address
SERVER = "192.168.0.102"
# Set here an unused port
PORT = 5050


positions = [(0, 0), (100, 100)]


def read_position(string: str):
    string = string.split(",")
    return int(string[0]), int(string[1])


def make_position(position: tuple[int, int]):
    return str(position[0]) + "," + str(position[1])


def threaded_client(connection: socket.socket, player_id: int):
    connection.send(
        str.encode(
            make_position(positions[player_id]),
        )
    )
    reply = ""
    while True:
        try:
            # Argument is amount of information you want to receive (bits)
            data = read_position(connection.recv(2048).decode())
            positions[player_id] = data

            if not data:
                print("Disconnected")
                break
            else:
                # Replies the other player's position
                reply = positions[abs(player_id - 1)]

                print("Received: ", reply)
                print("Sending: ", reply)

            connection.sendall(str.encode(make_position(reply)))
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
