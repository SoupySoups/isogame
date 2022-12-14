import utils.runAtStart as ras

del ras

import pygame
import logging
import utils.logs as logs
from graphics.graphicsManager import GraphicsManager
from levelManager import LevelManager
from graphics.renderManager import RenderManager
from entityManager import EntityManager, Entity
from graphics.screenManager import ScreenManager
from graphics.uiManager import UIManager
from graphics.animationManager import AnimationManager

# from states.build import build
from states.game import game

logs.createLogger(logging.DEBUG)

gm = GraphicsManager(size=(320, 180), windowName="Soup Engine")
um = UIManager(gm)
sm = ScreenManager(um)
em = EntityManager()
lm = LevelManager(em)
am = AnimationManager("assets/anims.yuckie")
rm = RenderManager(em, gm, am)

# level = lm.load("maps/test.yuck")
level = lm.createNew(em, 10, 10, 5, "assets/tileset.png")
em.addEntity(Entity("player", 0, 0, 3, "idle_front"))
lm.save(level, "maps/test.yuck")

# b = build(gm, um, em, lm, rm, am)
g = game(gm, um, em, lm, rm, am)
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
            #     b.toggleDebugDraw()

            # if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                # sm.setScreenById(active)
                # if active == 'build':
                #     active = 'game'
                # elif active == 'game':
                #     active = 'build'

        sm.run(events, dt)




if __name__ == "__main__":
    main()
