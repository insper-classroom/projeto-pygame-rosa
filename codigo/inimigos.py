import pygame
from tilemap import *

class FisInimigo:
    def __init__(self, jogo, i_tipo, pos, tamanho):
        self.jogo = jogo
        self.type = i_tipo
        self.pos = list(pos)
        self.tamanho = tamanho
        self.vel = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.tamanho[0], self.tamanho[1])

    def atualizar(self, tilemap, movement=(0,0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.vel[0], movement[1] + self.vel[1])

        self.pos[0] += frame_movement[0]
        inimigo_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if inimigo_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    inimigo_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    inimigo_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = inimigo_rect.x

        self.pos[1] += frame_movement[1]
        inimigo_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if inimigo_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    inimigo_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    inimigo_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = inimigo_rect.y

        self.vel[1] = min(5, self.vel[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.vel[1] = 0

    def render(self, surf):
        surf.blit(self.jogo.assets['player'], self.pos)