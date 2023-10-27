import random
import pygame
from tilemap import *


class Meteoro:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = (
            self.pos[0] - offset[0] * self.depth,
            self.pos[1] - offset[1] * self.depth
        )
        wrap_width = surf.get_width() + self.img.get_width()
        wrap_height = surf.get_height() + self.img.get_height()
        surf.blit(self.img, (render_pos[0] % wrap_width - self.img.get_width(), render_pos[1] % wrap_height - self.img.get_height()))


class Desenhos:
    def __init__(self, cloud_images, count=16):
        self.clouds = [
            Meteoro(
                (random.random() * 99999, random.random() * 99999),
                random.choice(cloud_images),
                random.random() * 0.05 + 0.05,
                random.random() * 0.6 + 0.2
            )
            for _ in range(count)
        ]
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)
