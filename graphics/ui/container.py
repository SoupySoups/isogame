import pygame


class Container:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.active_container = None

        self.children = []

        self.hovered = False
        self.left_clicked = False
        self.right_clicked = False

    def add(self, child):
        """Adds the given child to the container.

        Args:
            child (_type_): The child to add.
        """
        self.children.append(child)
        return child

    def remove(self, child):
        """Removes the given child from the container.

        Args:
            child (_type_): The child to remove.
        """
        self.children.remove(child)

    def draw(
        self,
        screen: pygame.Surface,
        events,
        prect,
        x,
        y,
        is_active,
        gm,
        debug_draw=False,
    ):
        """Draws the container and all of its children to the given screen.

        Args:
            screen (pygame.Surface): Screen to draw to.
            events (list): List of pygame events.
            prect (pygame.Rect): The rect of the parent container.
            x (int): X position of the parent container.
            y (int): Y position of the parent container.
            is_active (bool): Whether or not the container is active.
            debug_draw (bool, optional): Whether or not to draw debug information. Defaults to False.
        """
        self._render(
            screen, events, self.genRect(0, 0, 1, 1, (prect.width, prect.height))
        )

        mrect = prect.copy()
        mrect.x, mrect.y = x, y

        self.hovered = mrect.collidepoint(gm.windowToScreen(pygame.mouse.get_pos()))
        self.left_clicked = self.hovered and pygame.mouse.get_pressed()[0]
        self.right_clicked = self.hovered and pygame.mouse.get_pressed()[2]

        if not is_active:
            self.active_container = None

        for child in self.children:
            rect = self.genRect(
                child.x, child.y, child.width, child.height, screen.get_size()
            )

            mcolid = rect.move(x, y).collidepoint(pygame.mouse.get_pos())

            if mcolid or child == self.active_container:
                child.draw(
                    screen.subsurface(rect),
                    events,
                    rect,
                    x + rect.x,
                    y + rect.y,
                    is_active and self.active_container == child,
                    gm,
                    debug_draw,
                )
                if mcolid and pygame.mouse.get_pressed()[0]:
                    self.active_container = child
            else:
                child.draw(
                    screen.subsurface(rect),
                    [],
                    rect,
                    x + rect.x,
                    y + rect.y,
                    is_active and self.active_container == child,
                    gm,
                    debug_draw,
                )

            if debug_draw:
                pygame.draw.line(
                    screen, (255, 255, 0), (rect.x, 0), (rect.x, prect.height), 2
                )  # Yellow
                pygame.draw.line(
                    screen,
                    (255, 255, 0),
                    (rect.x + rect.width, 0),
                    (rect.x + rect.width, prect.height),
                    2,
                )  # Yellow
                pygame.draw.line(
                    screen, (0, 255, 0), (0, rect.y), (prect.width, rect.y), 2
                )  # Green
                pygame.draw.line(
                    screen,
                    (0, 255, 0),
                    (0, rect.y + rect.height),
                    (prect.width, rect.y + rect.height),
                    2,
                )  # Green

                if self.active_container == child:
                    pygame.draw.rect(screen, (255, 0, 255), rect, 2)  # Purple
                else:
                    pygame.draw.rect(screen, (0, 255, 255), rect, 2)  # Cyan

    def percentToPixel(self, percent: float, size: float):
        """Converts a percentage to a pixel value.

        Args:
            percent (float): Percentage to convert.
            size (float): Size to convert to.

        Returns:
            float: Pixel value.
        """
        return size * percent

    def genRect(self, x, y, width, height, size):
        """Generates a pygame rect from the given values.

        Args:
            x (float): X position.
            y (float): Y position.
            width (float): Width.
            height (float): Height.
            size (tuple): Size of the screen.

        Returns:
            pygame.Rect: Rect.
        """
        return pygame.rect.Rect(
            self.percentToPixel(x, size[0]),
            self.percentToPixel(y, size[1]),
            self.percentToPixel(width, size[0]),
            self.percentToPixel(height, size[1]),
        )

    def _render(self, _: pygame.Surface, events, rect):
        del events, rect
