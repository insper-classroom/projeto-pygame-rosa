import pygame
import sys
import math
import random
from constantes import *
from entidades import *
from utils import *
from tilemap import *
from fundo_espaco import *
from particle import *


class Jogo:
    def __init__(self):
        pygame.font.init()  
        
        # Inicializando a tela e configurações básicas
        self.janela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption('Guaxis')
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]  # Define a direção do movimento

        # Carregando assets do jogo
        self.load_assets()

        # Inicializando componentes do jogo
        self.clouds = Desenhos(self.assets['clouds'], count=16)
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)


        # Carregando o nível inicial
        self.load_level(0)

        self.render_scroll = [0, 0]


    def load_assets(self):
        """Carrega todos os recursos necessários para o jogo."""
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/shot': Animation(load_images('particles/particle'), img_dur=4, loop=False),
            'gun':load_image('gun.png'),
            'projectile':load_image('projectile.png'),
        }

    def load_level(self, map_id):
        """Carrega um nível com base no ID do mapa."""
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        self.initialize_entities_from_tilemap()

        # Inicializando componentes variáveis
        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.scroll = [0, 0]
        self.dead = 0

    def initialize_entities_from_tilemap(self):
        """Extrai as entidades do tilemap."""
        self.leaf_spawner = [pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13) 
                             for tree in self.tilemap.extract([('large_decor', 2)], keep=True)]
        
    def handle_events(self):
        """Lida com os eventos de entrada."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True
                if event.key == pygame.K_UP:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False

    def update(self):
        """Atualiza o estado do jogo."""
        self.render_scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.render_scroll[0]) / 30
        self.render_scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.render_scroll[1]) / 30

        # Atualização do jogador
        if not self.dead:
            self.player.atualizar(self.tilemap, (self.movement[1] - self.movement[0], 0))

        # Atualização de projéteis
        for projectile in self.projectiles:
            projectile.x += projectile.direction.x * projectile.speed
            projectile.y += projectile.direction.y * projectile.speed

    def render(self):
        """Renderiza os elementos do jogo."""
        self.display.blit(self.assets['background'], (0, 0))
        self.clouds.update()
        self.clouds.render(self.display, offset=self.render_scroll)
        self.tilemap.render(self.display, offset=self.render_scroll)





        if not self.dead:
            self.player.render(self.display, offset=self.render_scroll)

    def run(self):
        """Loop principal do jogo."""
        while True:
            self.handle_events()
            self.update()
            self.render()

            # Atualizando a tela
            self.janela.blit(pygame.transform.scale(self.display, self.janela.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Jogo().run()
