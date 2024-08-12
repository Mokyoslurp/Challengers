import pygame

from network import Network
from player import Player

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redraw_window(player1: Player, player2: Player):
    win.fill((255, 255, 255))
    player1.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    network = Network()

    player1 = network.get_player()

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        player2 = network.send(player1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()
        redraw_window(player1, player2)


if __name__ == "__main__":
    main()
