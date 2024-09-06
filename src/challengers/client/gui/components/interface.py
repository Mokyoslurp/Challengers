import pygame


from .gui_element import GUIElement


class Interface:
    def __init__(self, elements: list[GUIElement]):
        self.elements: list[GUIElement] = elements

    def draw(self, window: pygame.Surface):
        for element in self.elements:
            element.draw(window)

    def handle_event(self, event: pygame.event.Event):
        for element in self.elements:
            element.handle_event(event)

    def set_active(self):
        for element in self.elements:
            element.set_active()

    def unset_active(self):
        for element in self.elements:
            element.set_active()

    def show(self):
        for element in self.elements:
            element.show()

    def hide(self):
        for element in self.elements:
            element.hide()
