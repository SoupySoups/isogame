import pygame
from typing import Any
from entityManager import EntityManager
from graphics.graphicsManager import GraphicsManager
from graphics.renderManager import RenderManager
from graphics.uiManager import UIManager
from levelManager import LevelManager
import utils.logs as logs
import logging


class ScreenManager:
    @logs.logBeforeAndAfter(
        before="Setting up screen manager...",
        after="Screen manager successfully set up.",
        level=logging.DEBUG,
    )
    def __init__(self, um: UIManager):
        self._screens = []
        self._screens_index = 0
        self._first = True
        self.um = um

    def addScreen(
        self,
        callback: callable,
        identifier: str = None,
    ) -> str:
        """Adds as screen to the screen manager.

        Args:
            screen (pygame.Surface): The screen to add.
            id (str, optional): The id of the screen. Defaults to None.
            callback (callable, optional): Function that will run the screens contents. Defaults to lambda:None.
        """
        if identifier is None:
            identifier = f'{id("Its bad habit not to assign ids!"):x}'
        self._screens.append({"id": identifier, "callback": callback})

        return id

    def setScreenById(self, id: str):
        """Sets the current screen to the screen with the given id.

        Args:
            id (str): The id of the screen to set.

        Raises:
            KeyError: If the screen with the given id is not found.
        """
        for i, screen in enumerate(self._screens):
            if screen["id"] == id:
                self._screens_index = i
                self._screens[self._screens_index]["callback"].onStart()
                self._first = True
                self.um.clear()
                return True
        raise KeyError("Screen with id '{}' not found".format(id))

    def removeScreenById(self, id: str):
        """Removes the screen with the given id.

        Args:
            id (str): The id of the screen to remove.

        Raises:
            KeyError: If the screen with the given id is not found.
        """
        for i, screen in enumerate(self._screens):
            if screen["id"] == id:
                del self._screens[i]
                return True
        raise KeyError("Screen with id '{}' not found".format(id))

    def run(self, events, dt) -> Any:
        if self._first:
            self._screens[self._screens_index]["callback"].onStart()
            self._first = False

        self._screens[self._screens_index]["callback"].onUpdate(events, dt)

    @property
    def currentScreenId(self) -> str:
        """Returns the id of the current screen.

        Returns:
            str: The id of the current screen.
        """
        if len(self._screens) == 0:
            return None
        return self._screens[self._screens_index]["id"]
