import pygame

from network import Network
from game import Moves, Game


pygame.font.init()

width = 700
height = 700
window: pygame.Surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text: str, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 150

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        # Center text
        window.blit(
            text,
            (
                self.x + round(self.width / 2) - round(text.get_width() / 2),
                self.y + round(self.height / 2) - round(text.get_height() / 2),
            ),
        )

    def click(self, position):
        x1 = position[0]
        y1 = position[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + height:
            return True
        else:
            return False


def redraw_window(game: Game, player_id: int):
    window.fill((128, 128, 128))

    if not game.connected():
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Waiting for player...", 1, (255, 0, 0))
        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Your move", 1, (0, 255, 255))
        window.blit(text, (80, 200))

        text = font.render("Opponents move", 1, (0, 255, 255))
        window.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.both_played():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            text1 = font.render("Waiting", 1, (0, 0, 0))
            text2 = font.render("Waiting", 1, (0, 0, 0))
            if game.player1_played:
                if player_id == 0:
                    text1 = font.render(move1, 1, (0, 0, 0))
                else:
                    text1 = font.render("Locked in", 1, (0, 0, 0))
            elif game.player2_played:
                if player_id == 1:
                    text2 = font.render(move2, 1, (0, 0, 0))
                else:
                    text2 = font.render("Locked in", 1, (0, 0, 0))

        if player_id == 0:
            window.blit(text1, (100, 350))
            window.blit(text2, (400, 350))
        else:
            window.blit(text2, (100, 350))
            window.blit(text1, (400, 350))

        for button in buttons:
            button.draw(window)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    network = Network()
    player_id = int(network.get_player())
    print("You are player ", player_id)

    while run:
        clock.tick(60)

        try:
            game = network.send("get")
        except:  # noqa: E722
            run = False
            print("Couldn't get into game")
            break

        if game.both_played():
            redraw_window(game, player_id)
            pygame.time.delay(500)
            try:
                game = network.send("reset")
            except:  # noqa: E722
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 60)

            print(game.both_played())
            print(game.moves)

            winner = game.winner()
            print(winner)
            if winner == player_id:
                text = font.render("You won!", 1, (255, 0, 0))
            elif winner == -1:
                text = font.render("Tie!", 1, (255, 0, 0))
            else:
                text = font.render("You lost!", 1, (255, 0, 0))

            window.blit(
                text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2)
            )
            pygame.display.update()
            pygame.time.delay(3000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if game.connected():
                    for button in buttons:
                        if button.click(position):
                            if player_id == 0:
                                if not game.player1_played:
                                    network.send(button.text)
                            else:
                                if not game.player2_played:
                                    network.send(button.text)

        redraw_window(game, player_id)


if __name__ == "__main__":
    buttons = [
        Button(Moves.SCISSORS, 50, 500, (255, 0, 0)),
        Button(Moves.PAPER, 250, 500, (0, 255, 0)),
        Button(Moves.ROCK, 450, 500, (0, 0, 255)),
    ]

    main()
