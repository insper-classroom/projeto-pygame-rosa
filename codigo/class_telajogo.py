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
        self.map_file = "mapas/mapa_teste.txt"
        with open(self.map_file, "r") as file:
            self.map_data = [line.strip() for line in file]
        self.chao = pygame.image.load("img/cozinha/chao.png")
        self.parede_lado_d = pygame.image.load("img/cozinha/parede_lado_di.png")
        self.parede_lado_e = pygame.image.load("img/cozinha/parede_lado_es.png")
        self.parede_lado_c = pygame.image.load("img/cozinha/parede_lado_cima.png")
        self.parede_lado_b = pygame.image.load("img/cozinha/parede_lado_baixo.png")
        self.fundo = pygame.image.load('img/cozinha/fundo.png')
        self.canto_baixo_d = pygame.image.load('img/cozinha/canto_direito_baixo.png')
        self.canto_baixo_e = pygame.image.load('img/cozinha/canto_esquerdo_baixo.png')
        self.canto_cima_d = pygame.image.load('img/cozinha/canto_direito_cima.png')
        self.canto_cima_e = pygame.image.load('img/cozinha/canto_esquerdo_cima.png')
        self.parede_porta = pygame.image.load('img/cozinha/parede_porta.png')
        self.mesa_centro = pygame.image.load('img/cozinha/mesa_centro.png')
        self.mesa_direito = pygame.image.load('img/cozinha/mesa_lado_direito.png')
        self.mesa_esquerda = pygame.image.load('img/cozinha/mesa_lado_esquerda.png')
        self.parede_baixo = pygame.image.load('img/cozinha/parede_baixo-sen.png')
        self.demon = pygame.image.load('img/cozinha/demon.png')


    def atualizar(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        self.player.atualizar()

        return self
    
    def desenhar_mapa(self):
        for y, row in enumerate(self.map_data):
            for x, char in enumerate(row):
                if char == "c":
                    self.jogo.janela.blit(self.parede_lado_c, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == 'b':
                    self.jogo.janela.blit(self.parede_lado_b, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == "d":
                    self.jogo.janela.blit(self.parede_lado_d, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == 'e':
                    self.jogo.janela.blit(self.parede_lado_e, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == '.':
                    self.jogo.janela.blit(self.chao, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == 'f':
                    self.jogo.janela.blit(self.fundo, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == "1":
                    self.jogo.janela.blit(self.canto_baixo_e, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == '2':
                    self.jogo.janela.blit(self.canto_baixo_d, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == '3':
                    self.jogo.janela.blit(self.canto_cima_d, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == '4':
                    self.jogo.janela.blit(self.canto_cima_e, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == 'p':
                    self.jogo.janela.blit(self.parede_porta, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == ',':
                    self.jogo.janela.blit(self.mesa_centro, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == 'z':
                    self.jogo.janela.blit(self.parede_baixo, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == 'g':
                    self.jogo.janela.blit(self.mesa_direito, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == 'k':
                    self.jogo.janela.blit(self.mesa_esquerda, (x * self.jogo.block_size, y * self.jogo.block_size))
                if char == 'm':
                    self.jogo.janela.blit(self.demon, (x * self.jogo.block_size, y * self.jogo.block_size))
                

    def desenha_fps(self):
        self.fps = int(self.clock.get_fps())
        self.texto = self.fps_font.render(f'FPS: {self.fps}', True, (255, 255, 255))
        self.text_rect = self.texto.get_rect()
        self.text_rect.bottomright = (largura - 10, altura - 10)
        self.jogo.janela.blit(self.texto, self.text_rect)
 
    def desenhar(self):
        self.jogo.janela.fill((255, 255, 255))
        self.desenhar_mapa()
        self.player.desenhar(self.jogo.janela)
        self.desenha_fps() 
        pygame.display.update()
        self.clock.tick(60)