import pygame
import sys

class Tela_inicio():
    def __init__(self):
        pygame.init()

        self.janela = pygame.display.set_mode((680, 480))
        pygame.display.set_caption('Guaxiis')
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()

        bg_st = pygame.image.load('data/images/telas/Guaxiis_start.png')
        self.bg_st = pygame.transform.scale(bg_st, (680, 480), self.janela)

        self.menu = True 

    def desenha(self):
        self.janela.blit(self.bg_st, (0, 0))

    def verifica_colisao_mouse(self):
        self.retangulo = pygame.Rect(248, 208, 184, 40)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        return self.retangulo.collidepoint(self.mouse_x, self.mouse_y)

    def run(self):
        while self.menu:
            self.desenha()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.verifica_colisao_mouse():
                        self.menu = False





