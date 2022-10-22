import pygame
from states.state import state
import graphics.ui.gui as gui

class game(state):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.crtShader = None
    
    def onStart(self):
        self.crtShader = self.gm.loadShader(frag="graphics/shaders/crt.frag.glsl")

    def onUpdate(self, events):
        self.gm.screen.fill((0, 0, 0))
        for e in events:
            pass
        

        self.em.animate()
        self.rm.render(self.lm.activeLevel, self.gm.screen)

        self.um.draw(self.gm.screen, events)
