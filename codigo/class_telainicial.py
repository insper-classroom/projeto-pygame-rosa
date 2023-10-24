import pygame, sys
from constantes import *
from pygame.locals import Rect
from class_tela import *
from class_telajogo import *

class TelaInicial(Tela):
    def __init__(self, jogo):
        super().__init__(jogo)

    def atualizar(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return TelaJogo(self.jogo)
        return self

    def desenhar(self):
        self.jogo.janela.fill((0,0,0))
        pygame.display.update()