import pygame, sys
from constantes import *
from pygame.locals import Rect
from class_tela import *
from class_jogador import *

class TelaJogo(Tela):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.player = Jogador(largura // 2, altura // 2)
        self.clock = pygame.time.Clock()

    def atualizar(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        self.player.atualizar()

        return self

    def desenhar(self):
        self.jogo.janela.fill((255, 255, 255))
        self.player.desenhar(self.jogo.janela)
        pygame.display.update()
        self.clock.tick(60)