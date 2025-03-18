import socket as s
import pickle
from threading import Thread

from challengers.game import Tournament, Player, Level, TournamentPlan, CardList, Card


SERVER_IP = "localhost"
PORT = 5050

BUFSIZE = 1024 * 2


class Server:
    def __init__(self, tournament: Tournament):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)

        self.client_threads: list[Thread] = []

        self.is_running: bool = False
        self.is_ready: bool = False

        self.player_count: int = 0
        # Player address and id
        self.players_ids: dict[int, int] = {}
        self.players_names: dict[int, str] = {}
        self.player_ready: dict[int, bool] = {}

        self.tournament = tournament

    def run(self):
        try:
            self.socket.bind((SERVER_IP, PORT))
        except s.error as e:
            print(e)

        # Argument is the number of client that can connect
        self.socket.listen(self.tournament.number_of_players)
        print("Waiting for connection, server started!")

        self.is_running = True
        while self.is_running:
            while self.is_running and not self.is_ready:
                client, address = self.socket.accept()
                print("Connected to:", address)

                self.players_ids[address[1]] = self.player_count
                self.player_ready[self.player_count] = False

                client_thread = Thread(target=self.client_thread, args=(client, address))
                client_thread.start()
                self.client_threads.append(client_thread)

                self.player_count += 1

                if self.player_count == self.tournament.number_of_players:
                    self.is_ready = True

            if self.player_count != self.tournament.number_of_players:
                self.is_ready = False

            # TODO: PB because of robot players
            if len(self.tournament.players) == self.tournament.number_of_players:
                self.tournament.play()

                for client_thread in self.client_threads:
                    client_thread.join()

                tournament_copy = self.tournament
                print(tournament_copy + " ended.")

    def client_thread(self, socket: s.socket, address):
        socket.send(str(self.player_count).encode())
        reply = ""

        player_id = self.players_ids[address[1]]
        while True:
            try:
                # Argument is amount of information you want to receive (bits)
                data = socket.recv(BUFSIZE).decode().split(" ")

                print("From", address, ":", data)

                match data[0]:
                    case "ready":
                        if not self.player_ready[player_id]:
                            if len(data) > 1:
                                name = data[1]
                            else:
                                name = "Player " + str(self.player_count)
                            client_player = Player(player_id, name)
                            self.tournament.add_player(client_player)

                            self.players_names[player_id] = client_player.name
                            self.player_ready[player_id] = True

                            reply = "Ready"
                        else:
                            reply = "Already"

                    case "get":
                        if len(data) > 1:
                            match data[1]:
                                case "opponent":
                                    if self.tournament.round >= 0:
                                        duel_id = TournamentPlan.plans[client_player].duel_ids[
                                            self.tournament.round
                                        ]
                                        duel = self.tournament.duels[duel_id]
                                        if duel.player_1 and duel.player_2:
                                            players = [duel.player_1, duel.player_2]
                                            players.remove(client_player)
                                            reply = players[0].id

                                case "players":
                                    reply = self.players_names

                                case "player":
                                    if len(data) > 2:
                                        try:
                                            id = int(data[2])
                                        except ValueError:
                                            id = 0

                                        player = [
                                            player
                                            for player in self.tournament.players
                                            if player.id == id
                                        ][0]
                                        if len(data) > 3:
                                            match data[3]:
                                                case "deck":
                                                    reply = player.deck
                                                case "exhaust":
                                                    reply = player.exhaust
                                                case "played":
                                                    reply = player.played_cards
                                                case "used":
                                                    reply = player.used_cards
                                                case "bench":
                                                    reply = player.bench
                                                case "trophies":
                                                    reply = player.trophies
                                                case "fans":
                                                    reply = player.fans
                                                case "plan":
                                                    reply = TournamentPlan.plans[
                                                        client_player
                                                    ].duel_ids
                                                case _:
                                                    reply = player.name

                                case "winner":
                                    if len(data) > 2:
                                        try:
                                            round = int(data[2])
                                        except ValueError:
                                            round = 0

                                        if len(data) > 3:
                                            try:
                                                park_id = int(data[3])
                                            except ValueError:
                                                park_id = 0

                                            reply = self.tournament.winners[round][park_id].id
                                    else:
                                        if self.tournament.winner:
                                            reply = self.tournament.winner

                                case "round":
                                    reply = self.tournament.round

                                case "duel":
                                    reply = TournamentPlan.plans[client_player].duel_ids[
                                        self.tournament.round
                                    ]

                                case "flag":
                                    duel_id = TournamentPlan.plans[client_player].duel_ids[
                                        self.tournament.round
                                    ]
                                    duel = self.tournament.duels[duel_id]
                                    reply = duel.flag_owner

                                case "scores":
                                    scores = self.tournament.get_scores()
                                    scores_with_id = {
                                        player.id: scores[player] for player in scores
                                    }
                                    reply = scores_with_id

                    case "play":
                        card = client_player.play()
                        reply = card

                    case "draw":
                        if len(data) > 1:
                            match data[1]:
                                case "S":
                                    level = Level.S
                                case "A":
                                    level = Level.A
                                case "B":
                                    level = Level.B
                                case "C":
                                    level = Level.C
                                case _:
                                    level = Level.S

                            tray = self.tournament.trays[level]
                            number_of_cards = TournamentPlan.CARDS_TO_DRAW[self.tournament.round][
                                level
                            ]

                            cards = CardList()
                            for _ in range(number_of_cards):
                                cards.append(client_player.draw(tray))

                    case "remove":
                        # TODO: REMOVE "is Card" REPLACE WITH TRY EXCEPT
                        if len(data) > 1 and data[1] is Card:
                            card = data[1]
                            if len(data) > 2 and data[2] is Level:
                                level = data[2]
                                tray = self.tournament.trays[level]
                                client_player.discard(card, tray)

                                reply = True

                    case "done":
                        client_player.has_managed_cards = True
                        reply = True

                    case "leave":
                        break

                    case "test":
                        self.tournament.initialize_trays()
                        reply = self.tournament.trays[Level.A].draw()
                    case _:
                        break

                socket.send(pickle.dumps(reply))
                # socket.sendall(pickle.dumps(reply))

                print("To", address, ":", reply)

            except:  # noqa: E722
                break

        print("Lost connection to:", address)
        socket.close()
        self.player_count -= 1


if __name__ == "__main__":
    server = Server()
    server.run()
