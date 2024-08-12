import pygame

from network import Network
from player import Player
from server import read_position, make_position

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


def redrawWindow(player1: Player, player2: Player):
    win.fill((255, 255, 255))
    player1.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    network = Network()
    start_position = read_position(network.get_position())

    player1 = Player(
        start_position[0],
        start_position[1],
        100,
        100,
        (0, 255, 0),
    )
    player2 = Player(
        0,
        0,
        100,
        100,
        (255, 0, 0),
    )

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        player2_position = read_position(network.send(make_position((player1.x, player1.y))))
        player2.x = player2_position[0]
        player2.y = player2_position[1]
        player2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()
        redrawWindow(player1, player2)


if __name__ == "__main__":
    main()
