import pygame
from typing import List
import logging
import utils.logs as logs
import time


class EntityManager:
    @logs.logBeforeAndAfter(
        before="Setting up entity manager...",
        after="Entity manager successfully set up.",
        level=logging.DEBUG,
    )
    def __init__(self) -> None:
        self.entities = []

    def addEntity(self, entity) -> None:
        self.entities.append(entity)

    def animate(self) -> None:
        for entity in self.entities:
            pass


class Entity:
    def __init__(self, x: int, y: int, z: int, image) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.image = image


class Player(Entity):
    def __init__(self) -> None:
        pass
