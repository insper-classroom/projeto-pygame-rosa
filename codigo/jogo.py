import pygame, sys
from constantes import *
from pygame.locals import Rect
from class_telainicial import *
from class_telajogo import *
from class_jogador import *
from class_jogo import *
from class_tela import *

if __name__ == '__main__':
    largura = 640
    altura = 480
    jogo = Jogo()
    jogo.executar()