import pygame

def game(inputs, screen=None):
    events = inputs['events']
    gm = inputs['graphicsManager']
    um = inputs['uiManager']
    em = inputs['entityManager']
    lm = inputs['levelManager']
    rm = inputs['renderManager']

    data = inputs['lastData'] if 'lastData' in inputs else {}

    screen.fill((0, 0, 0))
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            pass

    em.animate()
    rm.render(lm.activeLevel, screen, -1, False)

    return data