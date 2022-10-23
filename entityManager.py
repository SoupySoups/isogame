from typing import List
import logging
import utils.logs as logs
import math
from pygame import Vector3
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

    def removeEntity(self, entity) -> None:
        self.entities.remove(entity)

    def getOnLayer(self, layer: int) -> List:
        for e in self.entities:
            if math.floor(e.z) == layer:
                yield e

    def entityById(self, f: int) -> object:
        for e in self.entities:
            if e.id == f:
                return e


class Entity:
    def __init__(self, id, x: int, y: int, z: int, yuckieId=None) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.vel = Vector3(0, 0, 0)
        self.frStart = time.time()
        self.yuckieId = yuckieId
        self.frCnt = 0

    def asSurface(self, level, am):
        if self.yuckieId is not None:
            return level.get_gid(am.getFrame(self.yuckieId, self.frCnt))
        else:
            return level.get_gid(self.id)
