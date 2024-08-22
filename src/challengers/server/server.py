import socket
import pickle
from threading import Thread


from challengers.game import Tournament


SERVER_IP = "192.168.0.102"
PORT = 5050


def threaded_client(connection: socket.socket, player_id: int, game_id: int):
    global id_count

    connection.send(str(player_id).encode())
    reply = ""
    while True:
        try:
            # Argument is amount of information you want to receive (bits)
            data = connection.recv(4096).decode()

            # Checks if the game still exists
            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_moves()
                    elif data != "get":
                        game.play(player_id, data)

                reply = game
                connection.sendall(pickle.dumps(reply))

            else:
                break
        except:  # noqa: E722
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing game: ", game_id)
    except:  # noqa: E722
        pass

    id_count -= 1
    connection.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((SERVER_IP, PORT))
    except socket.error as e:
        print(e)

    threads: list[Thread] = []

    games: dict[int, Tournament] = {}
    id_count = 0

    # Argument is the number of client that can connect
    s.listen()
    print("Waiting for connection, server started!")

    while True:
        connection, address = s.accept()
        print("Connected to: ", address)

        id_count += 1
        game_id = (id_count - 1) // 2

        player_id = 0

        # If odd player number, start a new game
        if id_count % 2 == 1:
            games[game_id] = Tournament(2)
            print("Created new game: ", game_id)
        else:
            player_id = 1

        thread = Thread(target=threaded_client, args=(connection, player_id, game_id))
        thread.start()
        threads.append(thread)

    # TODO: Join threads after client disconnected
