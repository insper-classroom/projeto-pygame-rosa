import pygame

class Mouse:
    pygame.init()
    def __init__(self):
        self.x = 0
        self.y = 0

    def atualizar_posicao(self):
        self.x, self.y = pygame.mouse.get_pos()

    def clique_dentro_do_retangulo(self, retangulo):
        return retangulo.collidepoint(self.x, self.y)
