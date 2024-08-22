import pygame

from challengers.client import Network
from challengers.game import Tournament


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


def redraw_window(game: Tournament, player_id: int):
    window.fill((128, 128, 128))

    pygame.display.update()


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        window.fill((128, 128, 128))

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to play", 1, (255, 0, 0))
        window.blit(text, (100, 200))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


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
            print(game)
        except:  # noqa: E722
            run = False
            print("Couldn't get into game")
            break


if __name__ == "__main__":
    while True:
        menu_screen()
