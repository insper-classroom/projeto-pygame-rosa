import pygame
from tilemap import *
import random
from spark import Spark
import math

class FisInimigo:
    def __init__(self, jogo, i_tipo, pos, tamanho):
        self.jogo = jogo
        self.type = i_tipo
        self.pos = list(pos)
        self.tamanho = tamanho
        self.vel = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.tamanho[0], self.tamanho[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.jogo.assets[self.type + '/' + self.action].copy()

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

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        self.vel[1] = min(5, self.vel[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.vel[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Enemy(FisInimigo):
    def __init__(self, jogo, pos, size):
        super().__init__(jogo, 'enemy', pos, size)

        self.walking = 0
    
    def atualizar(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.jogo.player.pos[0] - self.pos[0], self.jogo.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16):
                    if (self.flip and dis[0] < 0):
                        self.jogo.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                        for i in range(4):
                            self.jogo.sparks.append(Spark(self.jogo.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[0] > 0):
                        self.jogo.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                        for i in range(4):
                            self.jogo.sparks.append(Spark(self.jogo.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))

        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)


        super().atualizar(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
        

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

        if self.flip:
            surf.blit(pygame.transform.flip(self.jogo.assets['gun'], True, False), (self.rect().centerx - 4 - self.jogo.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.jogo.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))
 

class Player(FisInimigo):

    def __init__(self, jogo, pos, size):

        super().__init__(jogo, 'player', pos, size)

        self.air_time = 0

        self.jumps = 1




    def atualizar(self, tilemap, movement=(0, 0)):

        super().atualizar(tilemap, movement=movement)

        self.air_time += 1

        if self.air_time > 120:
            self.jogo.dead += 1

        if self.collisions['down']:

            self.air_time = 0

            self.jumps = 1

        if self.air_time > 4:

            self.set_action('jump')

        elif movement[0] != 0:

            self.set_action('run')

        else:

            self.set_action('idle')


    def jump(self):

        if self.jumps:

            self.vel[1] = -3

            self.jumps -= 1

            self.air_time = 5