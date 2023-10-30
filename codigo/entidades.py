import pygame
from tilemap import *
import random
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
 

class Player(FisInimigo):

    def __init__(self, jogo, pos, size):
        super().__init__(jogo, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.x = pos[0]
        self.y = pos[1]
        self.score = 0
        self.pulando = -0.5
                
    def atualizar(self, tilemap, movement=(0, 0)):
        super().atualizar(tilemap, movement=movement)
        self.tilemap = tilemap
        # Obter a posição em tiles
        top_left_tile = [int(self.pos[0] // self.jogo.tilemap.tile_size), int(self.pos[1] // self.jogo.tilemap.tile_size)]
        bottom_right_tile = [int((self.pos[0] + self.tamanho[0]) // self.jogo.tilemap.tile_size), int((self.pos[1] + self.tamanho[1]) // self.jogo.tilemap.tile_size)]
        
        # Verificar todos os tiles sob o jogador
        for x in range(top_left_tile[0], bottom_right_tile[0] + 1):
            for y in range(top_left_tile[1], bottom_right_tile[1] + 1):
                tile_loc = str(x) + ';' + str(y)
                current_tile = self.jogo.tilemap.tilemap.get(tile_loc)

                if current_tile and current_tile['type'] == 'stone' and current_tile['variant'] == 0:
                    self.respawn()
                    return
                
                if current_tile and current_tile['type'] == 'decor' and current_tile['variant'] == 3:
                    self.tilemap.remove_tile(current_tile['pos'])
                    self.score += 1

                if current_tile and current_tile['type'] == 'stone' and current_tile['variant'] == 3:
                    self.trampolim()
                    self.pulando -= 0.1


        self.air_time += 1
        if self.air_time > 160:
            self.respawn()

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

    def trampolim(self):
        if self.jumps:
            self.vel[1] = -4 + self.pulando
            self.jumps -= 1
            self.air_time = 0

    def respawn(self):
        # Obtendo a posição do tile onde o jogador estava
        tile_x = int(self.pos[0] // self.jogo.tilemap.tile_size)
        tile_y = int(self.pos[1] // self.jogo.tilemap.tile_size)
        
        # Adicionando a stone variante 1 no tilemap
        self.jogo.tilemap.tilemap[str(tile_x) + ';' + str(tile_y)] = {
            'type': 'stone',
            'variant': 1,
            'pos': [tile_x, tile_y]
        }
        
        # Redefinindo a posição do jogador para a posição inicial (ou qualquer outra posição de respawn desejada)
        self.pos = [50, 130]
        self.vel = [0, 0]
        self.air_time = 0



def normalize_vector(vector):
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
    if magnitude == 0:
        return (0, 0)
    return (vector[0] / magnitude, vector[1] / magnitude)

