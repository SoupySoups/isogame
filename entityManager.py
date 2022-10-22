import pygame
from typing import List
import logging
import utils.logs as logs
import math
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

    def getOnLayer(self, layer: int) -> List:
        for e in self.entities:
            if math.floor(e.z) == layer:
                yield e

    def animate(self) -> None:
        for entity in self.entities:
            pass


class Entity:
    def __init__(self, id, x: int, y: int, z: int, gid) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.gid = gid


class Player(Entity):
    def __init__(self) -> None:
        pass
