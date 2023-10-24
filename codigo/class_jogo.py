import pygame, sys
from constantes import *
from pygame.locals import Rect
from class_telainicial import *

class Jogo:
    def __init__(self):
        pygame.font.init()  # Initialize the font module
        self.janela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption('Guaxis Cuccina')
        self.estado = TelaInicial(self)
        self.block_size = 32


    def executar(self):
        while self.estado:
            self.estado = self.estado.atualizar()
            self.estado.desenhar()
        
        pygame.quit()
