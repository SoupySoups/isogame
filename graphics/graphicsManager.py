import logging
from typing import Tuple
import utils.logs as logs
import pygame
from graphics.modernGLwindow import window
from pygame._sdl2 import video


class GraphicsManager(window):
    @logs.logBeforeAndAfter(
        before="Setting up graphics manager...",
        after="Graphics manager successfully set up.",
        level=logging.DEBUG,
    )
    def __init__(self, size: Tuple[int, int], windowName: str = "Soup Engine") -> None:
        """Initializes the graphics manager.

        Args:
            size (Tuple[int, int]): The size of the window.
            windowName (str, optional): The name of the window. Defaults to "Soup Engine".
        """

        super().__init__((1280, 720), windowName, size)
        self._showFps = False

        logging.debug(
            "Successfully initialized %s pygame modules, %s failed." % pygame.init()
        )

        self.font = pygame.font.SysFont("Arial", 20)

        self._clock = pygame.time.Clock()

    def windowToScreen(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Converts a position from window coordinates to screen coordinates.

        Args:
            pos (Tuple[int, int]): The position.

        Returns:
            Tuple[int, int]: The converted position.
        """
        return (
            int(pos[0] / self.window.width * self.render_size[0]),
            int(pos[1] / self.window.height * self.render_size[1]),
        )

    def run(self, showFps: bool = False) -> None:
        """Main loop.
        Yields:
            int: Delta time.
            List[pygame.event.Event]: List of events.
        """
        self._showFps = showFps

        while self.running:
            dt = self._clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    events.remove(event)
                    self.close()
                    pygame.quit()
                    return
            yield dt, events

            if self._showFps:
                msg = f"Fps: {int(self._clock.get_fps())}"
                fpsText = self.font.render(msg, False, (255, 255, 255), (0, 0, 0))
                text_inv = fpsText.convert()
                pos = (0, 0)
                text_inv.blit(
                    self.screen, (-pos[0], -pos[1]), special_flags=pygame.BLEND_RGB_SUB
                )
                self.screen.blit(fpsText, pos, special_flags=pygame.BLEND_RGB_SUB)
                self.screen.blit(text_inv, pos, special_flags=pygame.BLEND_RGB_ADD)

            self.update()

            self.screen.fill((0, 0, 0))

        pygame.quit()

    def showFps(self) -> None:
        """Shows the fps."""
        self._showFps = True

    def hideFps(self) -> None:
        """Hides the fps."""
        self._showFps = False

    def toggleFps(self) -> None:
        """Toggles the fps."""
        self._showFps = not self._showFps

    @property
    def identical(self):
        """Creates a screen like object.

        Returns:
            pygame.Surface: The surface.
        """
        return pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

    @property
    def width(self):
        """Returns the width.

        Returns:
            int: The width.
        """
        return self._size[0]

    @property
    def height(self):
        """Returns the height.

        Returns:
            int: The height.
        """
        return self._size[1]
