import pygame


class Client:
    def __init__(self):
        pygame.font.init()

        self.window_width = 700
        self.window_height = 700

        self.window: pygame.Surface = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption("Client")

    def draw(self):
        self.window.fill((128, 128, 128))

        pygame.display.update()

    def run(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)

            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    ...


if __name__ == "__main__":
    client = Client()
    client.run()
