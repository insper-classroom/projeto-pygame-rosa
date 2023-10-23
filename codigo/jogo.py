import pygame, sys
from constantes import *
from pygame.locals import Rect

class Jogo:
    def __init__(self):
        pygame.font.init()  # Initialize the font module
        self.janela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption('Nome do Jogo')
        self.estado = TelaInicial(self)

    def executar(self):
        while self.estado:
            self.estado = self.estado.atualizar()
            self.estado.desenhar()
        
        pygame.quit()

class Tela:
    def __init__(self, jogo):
        self.jogo = jogo

    def atualizar(self):
        pass

    def desenhar(self):
        pass

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
        self.jogo.janela.fill((0, 0, 0))
        self.player.desenhar(self.jogo.janela)
        self.desenha_fps()
        pygame.display.update()
        self.clock.tick(60) 

class Jogador:
    def __init__(self, x, y):
        self.image = pygame.image.load('img/heroes/knight/knight_idle_anim_f0.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_x = 0
        self.velocidade_y = 0


    def atualizar(self):
        keys = pygame.key.get_pressed()
        self.velocidade_x = 0
        self.velocidade_y = 0
        if keys[pygame.K_LEFT]:
            self.velocidade_x = -5
        if keys[pygame.K_RIGHT]:
            self.velocidade_x = 5
        if keys[pygame.K_UP]:
            self.velocidade_y = -5
        if keys[pygame.K_DOWN]:
            self.velocidade_y = 5
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        self.rect.x = max(0, min(largura - 50, self.rect.x))
        self.rect.y = max(0, min(altura - 50, self.rect.y))

    def desenhar(self, janela):
        janela.blit(self.image, self.rect.topleft)

if __name__ == '__main__':
    largura = 640
    altura = 480
    jogo = Jogo()
    jogo.executar()
