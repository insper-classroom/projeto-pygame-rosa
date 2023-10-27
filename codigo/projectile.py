class Projectile:
    def __init__(self, x, y, direction, speed=5):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
