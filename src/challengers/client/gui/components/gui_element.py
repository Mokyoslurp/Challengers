import pygame

from typing import Callable

from challengers.client.gui.util import WHITE


class GUIElement:
    """A basic GUI rectangle element that can be clicked on"""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        height: int = 150,
        width: int = 150,
        background_color: pygame.Color = WHITE,
    ):
        """Instantiation method

        :param x: element left side position
        :param y: element top side position
        :param height: element height
        :param width: element width
        :param color: color of the element, defaults to WHITE
        """
        self.x = x
        self.y = y
        self.height = height
        self.width = width

        self.background_color = background_color

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.left = x
        self.rect.top = y
        self.rect.height = height
        self.rect.width = width

        self.is_active = True
        self.is_drawn = True

        self.on_click_function: Callable = None

    def draw(self, window: pygame.Surface):
        """Draws the element on the screen

        :param window: screen to draw the element on
        """
        if self.is_drawn:
            pygame.draw.rect(window, self.background_color, self.rect)

    def click(self, position) -> bool:
        """Checks if the element is clicked by the user using mouse position

        :param position: user mouse position
        :return: True if mouse position on the element, False otherwise
        """
        x1 = position[0]
        y1 = position[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            if self.on_click_function:
                self.on_click_function()
            return True
        else:
            return False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if self.is_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                return self.click(mouse_position)
        return False

    def set_active(self):
        self.is_active = True

    def unset_active(self):
        self.is_active = False

    def show(self):
        self.is_drawn = True

    def hide(self):
        self.is_drawn = False

    def on_click(self, function: Callable):
        self.on_click_function = function
