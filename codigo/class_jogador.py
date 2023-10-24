import pygame, sys
from constantes import *
from pygame.locals import Rect

class Jogador:
    def __init__(self, x, y):
        self.image = pygame.image.load('xinim/xinim_parado0.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_x = 0
        self.velocidade_y = 0

        self.animation = [pygame.image.load(f'xinim/xinim_andando{i}.png') for i in range(5)]
        for i in range(5):
            self.animation[i] = pygame.transform.scale(self.animation[i], (50, 50))

        self.animation_left = [pygame.image.load(f'xinim/xinim_andando_l{i}.png') for i in range(5)]
        for i in range(5):
            self.animation_left[i] = pygame.transform.scale(self.animation_left[i], (50, 50))

        self.animation_parado = [pygame.image.load(f'xinim/xinim_parado{i}.png') for i in range(8)]
        for i in range(8):
            self.animation_parado[i] = pygame.transform.scale(self.animation_parado[i], (50, 50))


        self.frame = 0
        self.is_walking = False
        self.animation_speed = 6
        self.direcao = "parado"  


    def atualizar(self):
        keys = pygame.key.get_pressed()
        self.velocidade_x = 0
        self.velocidade_y = 0

        if keys[pygame.K_LEFT]:
            self.velocidade_x = -5
            self.direcao = "left"
            self.is_walking = True
        elif keys[pygame.K_RIGHT]:
            self.velocidade_x = 5
            self.direcao = "right"
            self.is_walking = True

        if not any(keys):
            self.is_walking = False
            self.direcao = "parado"
            self.frame = (self.frame + 1) % (len(self.animation_parado) * self.animation_speed)
            index = self.frame // self.animation_speed
            self.image = self.animation_parado[index]
        elif self.direcao == "right":
            self.frame = (self.frame + 1) % (len(self.animation) * self.animation_speed)
            index = self.frame // self.animation_speed
            self.image = self.animation[index]
        elif self.direcao == "left":
            self.frame = (self.frame + 1) % (len(self.animation_left) * self.animation_speed)
            index = self.frame // self.animation_speed
            self.image = self.animation_left[index]


        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        self.rect.x = max(0, min(largura - 50, self.rect.x))
        self.rect.y = max(0, min(altura - 50, self.rect.y))

    def desenhar(self, janela):
        janela.blit(self.image, self.rect.topleft)