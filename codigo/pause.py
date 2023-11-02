import pygame
import sys
from classe_jogo import *

class TelaPausa:
    def __init__(self, janela, jogo):
        self.janela = janela
        self.jogo = jogo  
        self.menu_ativo = False
        self.bg_pausa = pygame.image.load('data/images/telas/guaxinim_pausa.png')
        self.bg_pausa = pygame.transform.scale(self.bg_pausa, self.janela.get_size())

        # Suponha que as opções do menu de pausa sejam retângulos que o usuário pode clicar
        self.opcoes_rects = [
            pygame.Rect(60, 150, 200, 70),  
            pygame.Rect(235, 50, 200, 70),  
            pygame.Rect(435, 150, 200, 70),  
        ]

    def desenha_menu_pausa(self):
        self.janela.blit(self.bg_pausa, (0, 0))


    def executa_menu_pausa(self):
        self.menu_ativo = True
        while self.menu_ativo:
            self.desenha_menu_pausa()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.verifica_clique(event.pos)

    def verifica_clique(self, pos):
        for indice, rect in enumerate(self.opcoes_rects):
            if rect.collidepoint(pos):
                self.menu_ativo = False  # Para desativar o menu de pausa
                self.seleciona_opcao(indice)
                break

    def seleciona_opcao(self, indice):
        if indice == 0:
            pygame.quit()
            sys.exit()
        elif indice == 1:
            self.jogo.reiniciar()
        elif indice == 2:
            pass
        else:
            pygame.quit()
