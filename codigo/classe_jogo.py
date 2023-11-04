import pygame
import sys
import math
import random
from constantes import *
from entidades import *
from utils import *
from tilemap import *
from pause import *
from game_over import *
from final import *

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
        self.player = Player(self, (50, 120), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)
        self.current_level = 0
        # Carregando o nível inicial
        self.load_level(0)
        self.render_scroll = [0, 0]
        self.game_time = 0
        self.paused = False 
        self.pause = TelaPausa(self.janela, self)
        self.gameover = Gameover(self.janela, self)
        self.final = final(self.janela, self)

        self.musica = pygame.mixer.music.load('data/sounds/musica_fundo.mp3')
        pygame.mixer.music.play(-1)



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
        }

    def load_level(self, map_id):
        """Carrega um nível com base no ID do mapa."""
        try:
            self.tilemap.load('data/maps/' + str(map_id) + '.json')
        except Exception as e:
            self.final.executa_final()
            self.musica_final.play()

        # Inicializando componentes variáveis
        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.scroll = [0, 0]
        self.player.pos = [50, 130]

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
                    self.paused = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True
                    self.paused = False
                if event.key == pygame.K_UP:
                    self.player.jump()
                    self.paused = False
                if event.key == pygame.K_e:
                    self.check_for_next_level()
                    self.paused = False
                if event.key == pygame.K_b:
                    self.check_botao()
                    self.paused = False
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                    self.pause.executa_menu_pausa()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                    self.paused = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False
                    self.paused = False


    def update(self):
        """Atualiza o estado do jogo."""
        if self.paused:
            self.game_time = self.game_time
        else:
            self.game_time += self.clock.get_time() / 1000.0
        self.render_scroll[0] += (self.player.rect().centerx - self.display.get_width() / 3 - self.render_scroll[0]) 
        self.render_scroll[1] += (self.player.rect().centery - self.display.get_height() / 3 - self.render_scroll[1]) / 30
        if not self.dead:
            self.player.atualizar(self.tilemap, (self.movement[1] - self.movement[0], 0))
        if self.game_time > 30:
            self.gameover.executa_gameover()

    def load_next_level(self):
        self.game_time = 0
        self.player.pos[0] = (10)
        self.player.pos[1] = (130)
        self.current_level += 1
        self.load_level(self.current_level)

    def espinho_posicao(self):
        positions = []
        for tile in self.tilemap.offgrid_tiles:
            if tile['type'] == 'decor' and tile['variant'] == 8:
                positions.append((int(tile['pos'][0] // self.tilemap.tile_size), int(tile['pos'][1] // self.tilemap.tile_size)))
        return positions
    
    def sorvete_posicao(self):
        positions_sorvete = []
        for tile in self.tilemap.offgrid_tiles:
            if tile['type'] == 'decor' and tile['variant'] == 3:
                positions_sorvete.append((int(tile['pos'][0] // self.tilemap.tile_size), int(tile['pos'][1] // self.tilemap.tile_size)))
        return positions_sorvete
    
    
    def check_for_next_level(self):        
        player_pos = (self.player.pos[0] + self.player.tamanho[0] / 2, 
                    self.player.pos[1] + self.player.tamanho[1] / 2)
        
        # Verificar se está perto de um tile offgrid decor variante 8
        for tile in self.tilemap.offgrid_tiles:
            if tile['type'] == 'decor' and tile['variant'] == 8:
                distance = math.sqrt((tile['pos'][0] - player_pos[0]) ** 2 + (tile['pos'][1] - player_pos[1]) ** 2)
                if distance < 100:
                    if self.player.score % 3 == 0:  # Ajuste esse valor conforme necessário
                        self.load_next_level()
                        return
                    else:
                        print('não pegou todos os sorvetes')
                        
    def check_botao(self):
        player_pos = (self.player.pos[0] + self.player.tamanho[0] / 2, 
                    self.player.pos[1] + self.player.tamanho[1] / 2)
        
        for tile in self.tilemap.offgrid_tiles:
            if tile['type'] == 'large_decor' and tile['variant'] == 0:
                distance = math.sqrt((tile['pos'][0] - player_pos[0]) ** 2 + (tile['pos'][1] - player_pos[1]) ** 2)
                if distance < 10:
                    tile['variant'] = 1
                    # Verificar tiles 'stone' variante 2 em offgrid_tiles
                    for a in self.tilemap.offgrid_tiles:
                        if a['type'] == 'stone' and a['variant'] == 2:
                            pos = a['pos']
                            tile_x = int(pos[0] // self.tilemap.tile_size)
                            tile_y = int(pos[1] // self.tilemap.tile_size)
                            self.tilemap.remove_parede((tile_x, tile_y))
                    # Verificar tiles 'stone' variante 2 em tilemap
                    tiles_to_remove = []
                    for loc, a in self.tilemap.tilemap.items():
                        if a['type'] == 'stone' and a['variant'] == 2:
                            tiles_to_remove.append(tuple(map(int, loc.split(";"))))
                    
                    # Remover os tiles após a conclusão do loop
                    for tile_pos in tiles_to_remove:
                        self.tilemap.remove_parede(tile_pos)
        return
    

    def render(self):
        """Renderiza os elementos do jogo."""
        self.display.blit(self.assets['background'], (0, 0))
        self.tilemap.render(self.display, offset=self.render_scroll)
        if not self.dead:
            self.player.render(self.display, offset=self.render_scroll)

    def reiniciar(self):
        """Reinicia o jogo para o estado inicial."""
        self.player.score = 0
        self.player.pos = [50, 130]
        
        self.load_level(self.current_level)
        self.dead = 0
        self.game_time = 0
        self.initialize_entities_from_tilemap()

    def render_timer(self):
            font = pygame.font.SysFont(None, 20)
            seconds = self.game_time
            timer_text = f'{int(seconds):02d}'
            text_surface = font.render(timer_text, True, (0, 0, 0))
            self.display.blit(text_surface, (10, 10))


    def run(self):
        """Loop principal do jogo."""
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.janela.blit(pygame.transform.scale(self.display, self.janela.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)