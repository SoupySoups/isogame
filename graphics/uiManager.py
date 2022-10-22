import pygame
import logging
import utils.logs as logs


class UIManager:
    @logs.logBeforeAndAfter(
        before="Setting up UI manager...",
        after="UI manager successfully set up.",
        level=logging.DEBUG,
    )
    def __init__(self, gm):
        self.containers = []
        self.active_container = None
        self.debug_draw = False
        self.gm = gm

    def add(self, child):
        """Adds the given child to the container list.

        Args:
            child (_type_): The child to add.
        """
        self.containers.append(child)
        return child

    def remove(self, child):
        """Removes the given child from the container list.

        Args:
            child (_type_): The child to remove.
        """
        self.containers.remove(child)

    def setContainers(self, containers):
        self.containers = containers

    def draw(self, screen: pygame.Surface, events, clear=False):
        w, h = screen.get_size()

        if clear:
            screen.fill((0, 0, 0))

        for container in self.containers:
            rect = container.genRect(
                container.x, container.y, container.width, container.height, screen.get_size()
            )

            mcolid = rect.collidepoint(self.gm.windowToScreen(pygame.mouse.get_pos()))
            if mcolid or container == self.active_container:
                container.draw(
                    screen.subsurface(rect),
                    events,
                    rect,
                    rect.x,
                    rect.y,
                    container == self.active_container,
                    self.gm,
                    self.debug_draw,
                )
                if mcolid and pygame.mouse.get_pressed()[0]:
                    self.active_container = container
            else:
                container.draw(
                    screen.subsurface(rect),
                    [],
                    rect,
                    rect.x,
                    rect.y,
                    container == self.active_container,
                    self.gm,
                    self.debug_draw,
                )

            if self.debug_draw:
                pygame.draw.line(
                    screen, (255, 255, 0), (rect.x, 0), (rect.x, h), 2
                )  # Yellow
                pygame.draw.line(
                    screen,
                    (255, 255, 0),
                    (rect.x + rect.width - 1, 0),
                    (rect.x + rect.width - 1, h),
                    2,
                )  # Yellow
                pygame.draw.line(
                    screen, (0, 255, 0), (0, rect.y), (w, rect.y), 2
                )  # Green
                pygame.draw.line(
                    screen,
                    (0, 255, 0),
                    (0, rect.y + rect.height - 1),
                    (w, rect.y + rect.height - 1),
                    2,
                )  # Green

                if self.active_container == container:
                    pygame.draw.rect(screen, (255, 0, 255), rect, 2)  # Purple
                else:
                    pygame.draw.rect(screen, (0, 255, 255), rect, 2)  # Cyan

    def toggleDebugDraw(self):
        self.debug_draw = not self.debug_draw

    def clear(self):
        self.containers = []
        self.active_container = None

CENTERED = 0.5
CENTER = 0.5
LEFT = 0
RIGHT = 1
TOP = 0
BOTTOM = 1
