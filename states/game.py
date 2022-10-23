import pygame
from states.state import state
import graphics.ui.gui as gui


class game(state):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.crtShader = None

    def onStart(self):
        self.crtShader = self.gm.loadShader(frag="graphics/shaders/crt.frag.glsl")

    def onUpdate(self, events, dt):
        for e in events:
            pass

        player = self.em.entityById("player")
        player.vel.x = 0
        player.vel.y = 0

        if player is not None:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.vel.y -= 0.01
                player.vel.x += 0.01
            if keys[pygame.K_s]:
                player.vel.y += 0.01
                player.vel.x -= 0.01
            if keys[pygame.K_a]:
                player.vel.y += 0.01
                player.vel.x += 0.01
            if keys[pygame.K_d]:
                player.vel.y -= 0.01
                player.vel.x -= 0.01

        if player.vel.x != 0 or player.vel.y != 0 or player.vel.z != 0:
            player.vel.normalize()

        self.am.animate(self.em.entities, dt)
        self.rm.render(self.lm.activeLevel, self.gm.screen)

        self.um.draw(self.gm.screen, events)
