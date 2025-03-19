import socket as s

from challengers.server import (
    build_request,
    decode_response,
    RESPONSE_LENGTH,
    Command,
)


class Client:
    def __init__(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.player_id: int

    def get_player(self):
        return self.player_id

    def connect(self, server_address: tuple[str, int]):
        try:
            self.socket.connect(server_address)

            # Here we use decode() since the first message received is the player id
            self.player_id = self.socket.recv(RESPONSE_LENGTH)
            print(f"Connected to : {server_address[0]}, {server_address[1]}")

        except:  # noqa: E722
            pass

    def send(self, command: Command, data: int = 0):
        try:
            # Send the command
            self.socket.send(build_request(command, data))
            # Receive the length of the packet to come
            response_length = decode_response(self.socket.recv(RESPONSE_LENGTH))[0]
            # Send acknowledgement of the packet length
            self.socket.send(build_request(Command.BLANK, response_length))
            # Receive full response
            response = decode_response(self.socket.recv(response_length * 8))
            return response
        except s.error as e:
            print(e)


if __name__ == "__main__":
    from pathlib import Path

    from challengers.server.server import SERVER_IP, PORT
    from challengers.game.card import CardList

    GAME_DATA_PATH = Path(__file__).parent.parent / "game" / "data"
    CARD_DATA_FILE = "cards.json"
    CARD_DATA_FILE_PATH = GAME_DATA_PATH / CARD_DATA_FILE

    client = Client()
    client.connect((SERVER_IP, PORT))

    cards = CardList.get_unique_cards_list(CARD_DATA_FILE_PATH)

    is_running = True

    commands = {
        "c": Command.CONNECT,
        "r": Command.READY,
        "p": Command.PLAY_CARD,
        "d": Command.DRAW_CARD,
        "t": Command.DISCARD_CARD,
        "m": Command.END_CARD_MANAGEMENT,
        "q": Command.LEAVE,
        "x": Command.FORCE_END,
    }

    while is_running:
        try:
            command = commands[input()]
            option = 0

            if command == Command.DRAW_CARD:
                option = int(input("Tray ?"))
            elif command == Command.FORCE_END or command == Command.LEAVE:
                is_running = False
            elif command == Command.DISCARD_CARD:
                option = int(input("Card id ?"))

            reply = client.send(command, option)
            print(f"Command {command.name} sent. Received {reply}.")

            if reply:
                if command == Command.PLAY_CARD:
                    print(cards[reply[0]])

                if command == Command.DRAW_CARD:
                    for id in reply:
                        print(cards[id])

        except Exception as e:
            print(e)
