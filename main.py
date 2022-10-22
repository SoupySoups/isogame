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

# from states.build import build
from states.game import game

logs.createLogger(logging.DEBUG)

gm = GraphicsManager(size=(320, 180), windowName="Soup Engine")
um = UIManager(gm)
sm = ScreenManager(um)
em = EntityManager()
lm = LevelManager(em)
rm = RenderManager(em, gm)

level = lm.load("maps/test.yuck")

# level = lm.createNew(em, 10, 10, 5, 'assets/tileset.png')
# for y in range(10):
#     for x in range(10):
#         level.addTile(x, y, 0, 0)
# lm.activeLevel = level
# lm.save(level, "maps/test.yuck")

# b = build(gm, um, em, lm, rm)
g = game(gm, um, em, lm, rm)
# sm.addScreen(b, "build")
sm.addScreen(g, "game")

rm.camera = (-150, -50)

def main():
    # active = 'build'

    for dt, events in gm.run():
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                gm.toggleFps()
                um.toggleDebugDraw()
                # b.toggleDebugDraw()
            
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            #     sm.setScreenById(active)
            #     if active == 'build':
            #         active = 'game'
            #     elif active == 'game':
            #         active = 'build'

        sm.run(events)

if __name__ == "__main__":
    main()
