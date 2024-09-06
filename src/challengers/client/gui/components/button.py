import pygame

from challengers.client.gui.util import BLACK, render_text_rect
from .gui_element import GUIElement


class Button(GUIElement):
    """A GUI element with a text that is clickable"""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        text: str = "",
        font_color: pygame.Color = BLACK,
        font: str = "comicsans",
        font_size: str = 20,
        **kwargs,
    ):
        """Instantiation method

        :param text: a Text object to draw on the button, defaults to None
        """
        super().__init__(x=x, y=y, **kwargs)
        self.text = text

        self.font_color = font_color
        self.font_name = font
        self.font_size = font_size
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

    def draw(self, window: pygame.Surface):
        """Draws button background, then the text on it if any

        :param window: screen to draw the button on
        """
        super().draw(window)
        if self.text and self.is_drawn:
            rendered_text = render_text_rect(
                self.text, self.font, self.rect, self.font_color, self.background_color
            )
            window.blit(rendered_text, self.rect)
