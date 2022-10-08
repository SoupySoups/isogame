import utils.logs as logs
import logging
import pygame
from entityManager import Entity
import pickle


@logs.logBeforeAndAfter(
    before="Setting up level manager...",
    after="Level manager successfully set up.",
    level=logging.DEBUG,
)
class LevelManager:
    @logs.logBeforeAndAfter(
        before="Setting up level manager...",
        after="Level manager successfully set up.",
        level=logging.DEBUG,
    )
    def __init__(self, entityManager: Entity) -> None:
        """Initializes the level manager."""
        self.em = entityManager
        self.activeLevel = None

    def save(self, level, filename: str):
        with open(filename, "wb") as f:
            pickle.dump({'name': level.name, 'width': level.width, 'height': level.height, 'layers': level.layers, 'tileset_path': level.tileset_path, 'objects': level.objects}, f)
            return filename

    def load(self, filename: str):
        with open(filename, "rb") as f:
            res = pickle.load(f)
            self.activeLevel = Level(res['name'], res['width'], res['height'], self.em, res['tileset_path'], res['layers'], res['objects'])
            return self.activeLevel

class Level:
    def __init__(self, name, width, height, entityManager, tileset_path, layers=None, objects=None) -> None:
        self.name = name

        self.tileset_path = tileset_path

        if layers is None:
            self.layers = []
        else:
            self.layers = layers
        if objects is None:
            self.objects = []
        else:
            self.objects = objects

        self.width = width
        self.height = height

        for object in self.objects:
            entityManager.addEntity(object)

        self.tiles = []
        self.load(tileset_path)

    def load(self, path):
        img = pygame.image.load(path).convert_alpha()
        y = 0
        for y in range(0, img.get_height(), 15):
            for x in range(0, img.get_width(), 14):
                self.tiles.append(img.subsurface((x, y, 14, 15)))

    def get_gid(self, gid):
        return self.tiles[gid]

    def getLayer(self, z: int):
        for layer in self.layers:
            if layer.z == z:
                return layer

    def addTile(self, x, y, z, gid):
        self.getLayer(z).addTile(x, y, gid)

    def getTile(self, x, y, z):
        return self.getLayer(z).getTile(x, y)
    
    def removeTile(self, x, y, z):
        self.getLayer(z).removeTile(x, y)

class Layer:
    def __init__(self, width, height, z, tiles=None) -> None:
        self.z = z
        self.height = height
        self.width = width

        if tiles is None:
            self.tiles = []
        else:
            self.tiles = tiles

    def addTile(self, x, y, gid):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                tile.gid = gid
                return True
            
        self.tiles.append(Tile(x, y, self.z, gid))

    def getTile(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
        return None

    def removeTile(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                assert self.z == tile.z
                self.tiles.remove(tile)
                return True
        return False

class Tile:
    def __init__(self, x, y, z, gid, solid=False) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.gid = gid
        self.solid = solid
