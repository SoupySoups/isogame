import pygame
from graphics.ui.container import Container
from graphics.uiManager import CENTER, TOP, BOTTOM, LEFT, RIGHT
from typing import Literal, Tuple


class Text(Container):
    def __init__(
        self,
        font: str,
        text: str,
        size: float,
        color: Tuple[int, int, int],
        bgColor: Tuple[int, int, int] = None,
        horizAlign: float = CENTER,
        vertAlign: float = CENTER
    ):
        super().__init__(0, 0, 1, 1)
        self.text = text
        self.font = font
        self.size = size
        self.font_color = color
        self.background_color = bgColor
        self.horizAlign = horizAlign
        self.vertAlign = vertAlign

    def _render(self, screen: pygame.Surface, events, rect):
        """Renders the text to the given screen.

        Args:
            screen (pygame.Surface): Surface to render to.
            events (list): List of events.
            prect (pygame.Rect): Rect of the this text.
        """
        font = pygame.font.SysFont(
            self.font, int(self.percentToPixel(self.size, rect.height))
        )
        text = font.render(self.text, False, self.font_color, self.background_color)

        if self.horizAlign == CENTER:
            x = rect.width / 2 - text.get_width() / 2
        elif self.horizAlign == RIGHT:
            x = rect.width - text.get_width()
        elif self.horizAlign == LEFT:
            x = 0

        if self.vertAlign == CENTER:
            y = rect.height / 2 - text.get_height() / 2
        elif self.vertAlign == BOTTOM:
            y = rect.height - text.get_height()
        elif self.vertAlign == TOP:
            y = 0

        screen.blit(text, (x, y))
