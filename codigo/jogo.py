import pygame
import sys
import math
import random
from constantes import *
from entidades import *
from utils import *
from tilemap import *


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
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)
        self.current_level = 0


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
        try:
            self.tilemap.load('data/maps/' + str(map_id) + '.json')
        except Exception as e:
            print(f"Erro ao carregar o mapa {map_id}.json: {e}")
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
                if event.key == pygame.K_e:
                    self.check_for_next_level()
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

    def load_next_level(self):
        self.current_level += 1
        self.load_level(self.current_level)

    def get_decor_8_positions(self):
        positions = []
        for tile in self.tilemap.offgrid_tiles:
            if tile['type'] == 'decor' and tile['variant'] == 8:
                positions.append((int(tile['pos'][0] // self.tilemap.tile_size), int(tile['pos'][1] // self.tilemap.tile_size)))
        return positions



    def check_for_next_level(self):        
        player_pos = (self.player.pos[0] + self.player.tamanho[0] / 2, 
                    self.player.pos[1] + self.player.tamanho[1] / 2)
        
        # Verificar se está perto de um tile offgrid decor variante 8
        for tile in self.tilemap.offgrid_tiles:
            if tile['type'] == 'decor' and tile['variant'] == 8:
                distance = math.sqrt((tile['pos'][0] - player_pos[0]) ** 2 + (tile['pos'][1] - player_pos[1]) ** 2)
                if distance < 100:  # Ajuste esse valor conforme necessário
                    self.load_next_level()
                    return


    def render(self):
        """Renderiza os elementos do jogo."""
        self.display.blit(self.assets['background'], (0, 0))
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
