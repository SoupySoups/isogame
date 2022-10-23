import pygame
from states.state import state
import graphics.ui.gui as gui


class build(state):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.height = 0
        self.activeBlock = 0

        self.uiContainer = None
        self.crtShader = None
        self.saveButton = None

    def onStart(self):
        self.crtShader = self.gm.loadShader(frag="graphics/shaders/crt.frag.glsl")

        self.uiContainer = gui.Container(0.8, 0, 0.2, 1)
        self.saveButton = self.uiContainer.add(
            gui.Button(0.1, 0.7, 0.8, 0.2, leftClickCallback=self.save)
        )
        self.saveButton.add(gui.Text("Arial", "Save", 0.5, (255, 255, 255), (0, 0, 0)))
        self.um.add(self.uiContainer)

    def save(self):
        self.lm.save(self.lm.activeLevel, "maps/test.yuck")

    def onUpdate(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.height < len(self.lm.activeLevel.layers) - 1 and e.button == 4:
                    self.height += 1
                if self.height > 0 and e.button == 5:
                    self.height -= 1
            if e.type == pygame.KEYDOWN:
                if e.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5,
                    pygame.K_6,
                    pygame.K_7,
                    pygame.K_8,
                    pygame.K_9,
                    pygame.K_0,
                ]:
                    self.activeBlock = int(e.unicode)

        # Get the mouse position
        x, y, z = self.rm.snapPointToGrid(
            self.rm.screenToWorld(
                self.rm.removeCameraOffset(
                    self.gm.windowToScreen(pygame.mouse.get_pos())
                ),
                self.height,
            )
        )
        l = self.lm.activeLevel.getLayer(self.height)

        xyLimited = self.rm.limitPoint(l.width, l.height, (x, y))

        pressed = pygame.mouse.get_pressed()
        if (
            not self.uiContainer.hovered
        ):  # If the mouse is interacting with the UI, don't do anything to the level
            if pressed[0]:
                self.lm.activeLevel.addTile(*xyLimited, z, self.activeBlock)
            elif pressed[2]:
                self.lm.activeLevel.removeTile(*xyLimited, z)

        self.am.animate(self.em.entities)
        self.rm.render(
            self.lm.activeLevel,
            self.gm.screen,
            self.height,
            True,
        )

        self.rm.drawBounds(self.gm.screen, (*xyLimited, z, 1, 1, 1), (255, 0, 0))

        self.um.draw(self.gm.screen, events)
