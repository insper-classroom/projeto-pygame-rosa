import pygame, sys
from constantes import *
from pygame.locals import Rect
from class_tela import *
from class_jogador import *

class TelaJogo(Tela):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.player = Jogador(largura // 2, altura // 2)
        self.fps_font = pygame.font.Font('font/PressStart2P.ttf', 20)
        self.clock = pygame.time.Clock()

    def atualizar(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        self.player.atualizar()

        return self

    
    def desenha_fps(self):
        self.fps = int(self.clock.get_fps())
        self.texto = self.fps_font.render(f'FPS: {self.fps}', True, (255, 255, 255))
        self.text_rect = self.texto.get_rect()
        self.text_rect.bottomright = (largura - 10, altura - 10)
        self.jogo.janela.blit(self.texto, self.text_rect)
 
    def desenhar(self):
        self.jogo.janela.fill((255, 255, 255))
        self.player.desenhar(self.jogo.janela)
        self.desenha_fps()
        pygame.display.update()
        self.clock.tick(60)