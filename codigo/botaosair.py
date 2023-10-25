import pygame
from constantes import *

class Botao_sair():
    pygame.init()
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 1920, 1080)

    def desenha_rect_sair(self, janela):
        pygame.draw.rect(janela, VERMELHO, self.rect)
