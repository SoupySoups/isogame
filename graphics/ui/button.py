import pygame
from graphics.ui.container import Container


class Button(Container):
    def __init__(
        self,
        *args,
        leftClickCallback=None,
        rightClickCallback=None,
        hoverCallback=None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.hoverCallback = hoverCallback
        self.leftClickCallback = leftClickCallback
        self.rightClickCallback = rightClickCallback

    def _render(self, screen: pygame.Surface, events, rect):
        if self.hovered and self.hoverCallback is not None:
            self.hoverCallback()
        elif self.left_clicked and self.leftClickCallback is not None:
            self.leftClickCallback()
        elif self.right_clicked and self.rightClickCallback is not None:
            self.rightClickCallback()
