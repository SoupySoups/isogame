import utils.runAtStart as ras

del ras

import pygame
import logging
import utils.logs as logs
from graphics.graphicsManager import GraphicsManager
from levelManager import Layer, Level, LevelManager
from graphics.renderManager import RenderManager
from entityManager import EntityManager
from graphics.screenManager import ScreenManager
from graphics.uiManager import UIManager
import graphics.ui.gui as gui

from states.build import build

logs.createLogger(logging.DEBUG)

gm = GraphicsManager(size=(320, 180), windowName="Soup Engine")
sm = ScreenManager()
um = UIManager(gm)
em = EntityManager()
lm = LevelManager(em)
rm = RenderManager(em, gm)

level = lm.load("maps/test.yuck")

# level = Level('test', 10, 10, em, 'assets/tileset.png', [Layer(10, 10, 0), Layer(10, 10, 1), Layer(10, 10, 2), Layer(10, 10, 3)])
# for y in range(10):
#     for x in range(10):
#         level.addTile(x, y, 0, 0)
# lm.activeLevel = level
# lm.save(level, "maps/test.yuck")

sm.addScreen(build(gm, um, em, lm, rm), "build")

rm.camera = (-150, -50)

for dt, events in gm.run():
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            gm.toggleFps()
            um.toggleDebugDraw()

    sm.run(events)
