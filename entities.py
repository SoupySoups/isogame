class Entity:
    def __init__(self, x, y, z, image, collision=True, scale=1):
        import pygame

        self.x = x
        self.y = y
        self.z = z
        old_dim = image.get_size()
        self.image = pygame.transform.scale(
            image, (old_dim[0] * scale, old_dim[1] * scale)
        )
        self.collision = collision
        self.width = 0.5
        self.height = 1

    def get_scaled(self, scale: int):
        from pygame import transform

        return transform.scale(
            self.image,
            (self.image.get_width() * scale, self.image.get_height() * scale),
        )

    def is_in_layer(self, layer: int):
        if self.z >= layer and self.z < layer + 1:
            return True
        return False

    def as_tuple(self):
        return (self.x, self.y, self.image, self.z)


class EntityManager:
    def __init__(self, screen):
        import pymunk.pygame_util
        from pymunk.vec2d import Vec2d

        self.entities = []
        self.layers = []

        self.statics = []

        self.screen = screen

        self.horizSpace = pymunk.Space()
        self.horizSpace.gravity = Vec2d(0, 0)

    class Box:
        def e(self, space, p0=(10, 10), p1=(30, 30), d=1):
            import pymunk

            x0, y0 = p0
            x1, y1 = p1
            segs = []
            self.space = space
            pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            for i in range(4):
                segment = pymunk.Segment(
                    self.space.static_body, pts[i], pts[(i + 1) % 4], d
                )
                segment.elasticity = 1
                segment.friction = 1
                self.space.add(segment)
                segs.append(segment)

            return segs

    def update(self, layers):
        self.layers = [layers[1]]  # FIXME
        if len(self.statics) != 0:
            self.horizSpace.remove(*self.statics)
        self.statics = []
        for layer in self.layers:
            for i, tile in enumerate(layer):
                self.statics.append(
                    self.Box().e(
                        self.horizSpace,
                        (tile[0] * 10, tile[1] * 10),
                        ((tile[0] + 1) * 10, (tile[1] + 1) * 10),
                    )
                )

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)

    def search_for_entities_for_layer(self, layer: int):
        for entity in self.entities:
            if entity.is_in_layer(layer):
                yield entity

    def collide(self, physicsLevel=3):
        import pymunk

        for entity in self.entities:
            if entity.collision:
                entity.x = entity.rb.position.x / 10
                entity.y = entity.rb.position.y / 10

        self.horizSpace.debug_draw(pymunk.pygame_util.DrawOptions(self.screen))

        self.horizSpace.step(physicsLevel / 10)


class Player(Entity):
    def __init__(self, x, y, z, image, space, scale=1):
        import pymunk

        super().__init__(x, y, z, image, scale=scale)
        self.vel = 0.05
        self.rb = pymunk.Body(5, float("inf"))
        self.rb.position = self.x * 5, self.y * 10

        self.rbf = pymunk.Circle(self.rb, self.width * 5, (0, 0))

        self.rbf.collision_type = 1

        space.add(self.rb, self.rbf)

    def keys(self, keys, dt):
        import pygame
        from pymunk import Vec2d

        target_vx = 0
        target_vy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            target_vx -= self.vel
        if keys[pygame.K_RIGHT]:
            target_vx += self.vel
        if keys[pygame.K_DOWN]:
            target_vy += self.vel
        if keys[pygame.K_UP]:
            target_vy -= self.vel

        self.rb.position += Vec2d(target_vx, target_vy) * dt
