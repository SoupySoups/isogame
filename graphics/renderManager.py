from typing import Tuple
from graphics.graphicsManager import GraphicsManager
from levelManager import Level
import pygame
from entityManager import EntityManager
import logging
import utils.logs as logs
from pygame._sdl2 import video


class RenderManager:
    @logs.logBeforeAndAfter(
        before="Setting up render manager...",
        after="Render manager successfully set up.",
        level=logging.DEBUG,
    )
    def __init__(self, em: EntityManager, gm: GraphicsManager) -> None:
        self.camera = (10, 0)

        self.em = em
        self.gm = gm

        self.cachedLayers = {}

    def render(self, level: Level, screen: pygame.Surface, active_layer: int = -1, plane=False) -> None:
        l = []

        unused = list(self.cachedLayers.keys())
        tempZ = 0
        for z, layer in enumerate(self.sort(level, extras=list(self.em.getOnLayer(tempZ+1)))):
            tempZ = z
            lid = level.getLayer(z).id
            lmf = level.getLayer(z).modified
            if lid in unused and not lmf:
                l.append(self.cachedLayers[lid])
                unused.remove(lid)
            else:
                layerSurf = self.gm.identical
                for element in layer:
                    point = self.addCameraOffset(
                            self.worldToScreen((element.x, element.y, element.z))
                        )
                    if screen.get_rect().inflate(20, 20).collidepoint(point):
                        if element.z > active_layer:
                            layerSurf.blit(element.asSurface(level), point)
                        else:
                            layerSurf.blit(element.asSurface(level), point)

                self.cachedLayers[lid] = layerSurf
                l.append(layerSurf)

        # Remove cached layers that are no longer used
        for key in unused:
            del self.cachedLayers[key]

        top = self.gm.identical
        for z, layer in enumerate(l):
            if z > active_layer and active_layer != -1:
                top.blit(layer, (0, 0))
            else:
                self.gm.screen.blit(layer, (0, 0))

        top.set_alpha(70)
        self.gm.screen.blit(top, (0, 0))

        if plane:
            al = level.getLayer(active_layer)
            plane = self.drawPlane(self.gm.identical, pygame.Rect(2, 1, al.width, al.height), active_layer-0.5)
            plane.set_alpha(128)
            self.gm.screen.blit(plane, (0, 0))

    def sort(self, level: Level, extras=None):
        """Mixes static and dynamic tiles together and sorts them by their index score.

        Args:
            level (Level): The level to sort.

        Yields:
            _type_: The sorted level.
        """
        if extras is None:
            extras = []

        to_sort = level.objects
        for z, layer in enumerate(level.layers):
            elements = layer.tiles
            for object in to_sort:
                if object.z >= z and object.z < z + 1:
                    elements.append(object)
                    to_sort.remove(object)

            yield sorted(
                elements + extras, key=lambda x: self.calculateIndexScore((x.x, x.y, x.z))
            )

    def calculateIndexScore(self, worldPos: Tuple[int, int, int]) -> int:
        """Calculates the index score of a world position.

        Args:
            worldPos (Tuple[int, int, int]): The world position. (X, Y, Z)
            width (int): The width of the level.
            height (int): The height of the level.

        Returns:
            int: The score.
        """
        return (worldPos[0] + worldPos[1]) * 5

    def worldToScreen(self, point: Tuple[int, int, int]) -> Tuple[int, int, int]:
        screenX = (point[0] - point[1]) * 6
        screenY = (point[0] + point[1]) * 3 - point[2] * 8
        return screenX, screenY

    def screenToWorld(
        self, screenPos: Tuple[int, int], world_z: int
    ) -> Tuple[int, int, int]:
        """Converts a screen position to a world position.

        Due to the nature of isometric rendering, the Z coordinate needs to be specified.

        Args:
            screenPos (Tuple[int, int]): Screen X and Y coordinates.
            world_z (int): The Z coordinate of the world position.

        Returns:
            Tuple[int, int, int]: The calculated world position.
        """
        deZefied_screen_y = (screenPos[1] + world_z * 8) / 3
        x6 = screenPos[0]/6
        world_x = (x6 + deZefied_screen_y) / 2
        world_y = (deZefied_screen_y - x6) / 2

        return world_x, world_y, world_z

    def addCameraOffset(self, screen: Tuple[int, int]) -> Tuple[int, int]:
        """Adds the camera offset to a screen position.

        Args:
            screen (Tuple[int, int]): The screen position.

        Returns:
            Tuple[int, int]: The offset screen position.
        """
        return screen[0] - self.camera[0], screen[1] - self.camera[1]

    def removeCameraOffset(self, screen: Tuple[int, int]) -> Tuple[int, int]:
        """Removes the camera offset from a screen position.

        Args:
            screen (Tuple[int, int]): The screen position.

        Returns:
            Tuple[int, int]: The "de-offset" screen position.
        """
        return screen[0] + self.camera[0], screen[1] + self.camera[1]

    def drawBounds(
        self,
        screen: pygame.Surface,
        bounds: Tuple[int, int, int, int, int, int],
        color: Tuple[int, int, int],
    ) -> None:
        """Draws the bounds of a rectangle.

        Args:
            screen (pygame.Surface): The screen to draw on.
            bounds (Tuple[int, int, int, int, int, int]): The bounds of the rectangle. (X, Y, Z, Length, Width, Height)
            color (Tuple[int, int, int]): The color of the rectangle.
        """
        tbl = self.addCameraOffset(
            self.worldToScreen((bounds[0] - 1, bounds[1] - 2, bounds[2] - 1))
        )  # Top-Back-Left
        tfl = self.addCameraOffset(
            self.worldToScreen((bounds[0] - 1 + bounds[3], bounds[1] - 2, bounds[2] - 1))
        )  # Top-Front-Left
        tbr = self.addCameraOffset(
            self.worldToScreen((bounds[0] - 1, bounds[1] - 2 + bounds[4], bounds[2] - 1))
        )  # Top-Back-Right
        tfr = self.addCameraOffset(
            self.worldToScreen(
                (bounds[0] - 1 + bounds[3], bounds[1] - 2 + bounds[4], bounds[2] - 1)
            )
        )  # Top-Front-Right

        tbl = (tbl[0], tbl[1]+1)
        tfl = (tfl[0], tfl[1]+1)
        tbr = (tbr[0], tbr[1]+1)
        tfr = (tfr[0], tfr[1]+1)

        bbl = (tbl[0], tbl[1] + (8 * bounds[5]))  # Bottom-Back-Left
        bfl = (tfl[0], tfl[1] + (8 * bounds[5]))  # Bottom-Front-Left
        bbr = (tbr[0], tbr[1] + (8 * bounds[5]))  # Bottom-Back-Right
        bfr = (tfr[0], tfr[1] + (8 * bounds[5]))  # Bottom-Front-Right

        pygame.draw.line(screen, color, tbl, tfl)
        pygame.draw.line(screen, color, tbl, tbr)
        pygame.draw.line(screen, color, tfl, tfr)
        pygame.draw.line(screen, color, tbr, tfr)

        pygame.draw.line(screen, color, bbl, bfl)
        pygame.draw.line(screen, color, bbl, bbr)
        pygame.draw.line(screen, color, bfl, bfr)
        pygame.draw.line(screen, color, bbr, bfr)

        pygame.draw.line(screen, color, tbl, bbl)
        pygame.draw.line(screen, color, tfl, bfl)
        pygame.draw.line(screen, color, tbr, bbr)
        pygame.draw.line(screen, color, tfr, bfr)

        return screen

    def drawPlane(self, screen: pygame.Surface, plane: pygame.rect, z: int) -> None:
        """Renders a plane.

        Args:
            screen (pygame.Surface): The screen to render on.
            plane (List[Tile]): The plane to render.
        """

        for y in range(plane.height + 1):
            pygame.draw.line(screen,
                (255, 255, 255, 100),
                self.addCameraOffset(self.worldToScreen((plane.x, y + plane.y, z + 0.5))),
                self.addCameraOffset(self.worldToScreen((plane.x + plane.width, y + plane.y, z + 0.5)))
            )
        for x in range(plane.width + 1):
            pygame.draw.line(screen,
                (255, 255, 255, 100),
                self.addCameraOffset(self.worldToScreen((x + plane.x, plane.y, z + 0.5))),
                self.addCameraOffset(self.worldToScreen((x + plane.x, plane.height + plane.y, z + 0.5)))
            )

        return screen
        
    def snapPointToGrid(self, point: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Snaps a point to the grid.

        Args:
            point (Tuple[int, int, int]): The point to snap.

        Returns:
            Tuple[int, int, int]: The snapped point.
        """
        return (round(point[0]), round(point[1]), round(point[2]))

    def limitPoint(self, width, height, point: Tuple[int, int]) -> Tuple[int, int]:
        """Limits a point to the world bounds.

        Args:
            point (Tuple[int, int, int]): The point to limit.

        Returns:
            Tuple[int, int, int]: The limited point.
        """
        return (
            max(0, min(point[0], width - 1)),
            max(0, min(point[1], height - 1))
        )
