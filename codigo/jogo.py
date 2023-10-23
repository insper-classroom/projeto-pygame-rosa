import pygame, sys
from constantes import *
from pygame.locals import Rect
import math

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
        self.katana = Katana()  # Create a Katana instance (after initializing the game window)
        self.clock = pygame.time.Clock()


    def atualizar(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
        
        self.katana.atualizar()  # Update katana position
        self.katana.check_collision(self.player)
        self.player.atualizar() 
        return self
    
    def desenha_fps(self):
        self.fps = int(self.clock.get_fps())
        self.texto = self.fps_font.render(f'FPS: {self.fps}', True, (255, 255, 255))
        self.text_rect = self.texto.get_rect()
        self.text_rect.bottomright = (largura - 10, altura - 10)
        self.jogo.janela.blit(self.texto, self.text_rect)

    def desenhar(self):
        self.jogo.janela.fill((255, 255, 255))
        self.player.desenhar(self.jogo.janela)
        self.katana.draw(self.jogo.janela)  # Draw the katana
        self.desenha_fps()
        pygame.display.update()
        self.clock.tick(60)

class Jogador:
    def __init__(self, x, y):
        self.image = pygame.image.load('img/xinim/xinim_parado0.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.circular_mask = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.circular_mask, (255, 255, 255, 128), (25, 25), 25)
        self.equipped_katana = False  # Added to keep track of katana equipment

        self.animation = [pygame.image.load(f'img/xinim/xinim_andando{i}.png') for i in range(5)]
        for i in range(5):
            self.animation[i] = pygame.transform.scale(self.animation[i], (50, 50))

        self.animation_left = [pygame.image.load(f'img/xinim/xinim_andandol0-export{i}.png') for i in range(1, 6)]
        for i in range(5):
            self.animation_left[i] = pygame.transform.scale(self.animation_left[i], (50, 50))

        self.animation_up = [pygame.image.load(f'img/xinim/xinin_tras{i}.png') for i in range(8)]
        for i in range(8):
            self.animation_up[i] = pygame.transform.scale(self.animation_up[i], (50, 50))

        self.animation_down = [pygame.image.load(f'img/xinim/xinim_andandobaixo{i}.png') for i in range(1, 9)]
        for i in range(8):
            self.animation_down[i] = pygame.transform.scale(self.animation_down[i], (50, 50))

        self.animation_parado = [pygame.image.load(f'img/xinim/xinim_parado{i}.png') for i in range(9)]
        for i in range(9):
            self.animation_parado[i] = pygame.transform.scale(self.animation_parado[i], (50, 50))

        self.frame = 0
        self.is_walking = False
        self.animation_speed = 6
        self.direcao = "parado"  

        
    def atualizar(self):
        keys = pygame.key.get_pressed()
        self.velocidade_x = 0
        self.velocidade_y = 0

        if keys[pygame.K_LEFT]:
            self.velocidade_x = -5
            self.direcao = "left"
            self.is_walking = True
        elif keys[pygame.K_RIGHT]:
            self.velocidade_x = 5
            self.direcao = "right"
            self.is_walking = True
        if keys[pygame.K_UP]:
            self.velocidade_y = -5
            self.direcao = "up"
            self.is_walking = True
        elif keys[pygame.K_DOWN]:
            self.velocidade_y = 5
            self.direcao = "down"
            self.is_walking = True

        if not any(keys):
            self.is_walking = False
            self.direcao = "parado"
            self.frame = (self.frame + 1) % (len(self.animation_parado) * self.animation_speed)
            index = self.frame // self.animation_speed
            self.image = self.animation_parado[index]
        elif self.direcao == "right":
            self.frame = (self.frame + 1) % (len(self.animation) * self.animation_speed)
            index = self.frame // self.animation_speed
            self.image = self.animation[index]
        elif self.direcao == "left":
            self.frame = (self.frame + 1) % (len(self.animation_left) * self.animation_speed)
            index = self.frame // self.animation_speed
            self.image = self.animation_left[index]
        elif self.direcao == "up":
            self.frame = (self.frame + 1) % (len(self.animation_up) * self.animation_speed)
            index = self.frame // self.animation_speed
            self.image = self.animation_up[index]
        elif self.direcao == "down":
            self.frame = (self.frame + 1) % (len(self.animation_down) * self.animation_speed)
            index = self.frame // self.animation_speed
            self.image = self.animation_down[index]

        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        self.rect.x = max(0, min(largura - 50, self.rect.x))
        self.rect.y = max(0, min(altura - 50, self.rect.y))

    def desenhar(self, janela):
        janela.blit(self.circular_mask, self.rect.topleft)
        janela.blit(self.image, self.rect.topleft)

class Katana:
    def __init__(self):
        self.image = pygame.image.load('img/armas/katana.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (largura // 2, altura // 2)  # Set the initial position in the middle of the screen
        self.attached_to_player = False

    def atualizar(self):
        if not self.attached_to_player:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.x = mouse_x
            self.rect.y = mouse_y

    def check_collision(self, player):
        if not self.attached_to_player and not player.equipped_katana:
            # Calculate the center coordinates of the player's circular mask
            player_center_x = player.rect.x + player.rect.width // 2
            player_center_y = player.rect.y + player.rect.height // 2

            # Calculate the center coordinates of the katana image
            katana_center_x = self.rect.x + self.rect.width // 2
            katana_center_y = self.rect.y + self.rect.height // 2

            # Calculate the distance between the player's center and katana's center
            distance = math.sqrt((player_center_x - katana_center_x) ** 2 + (player_center_y - katana_center_y) ** 2)

            # Define a collision threshold (adjust as needed)
            collision_threshold = player.rect.width // 2  # Assuming circular mask radius equals half the player's width

            # If the distance is less than the collision threshold, equip the katana
            if distance < collision_threshold:
                self.attached_to_player = True
                player.equipped_katana = True

    def draw(self, janela):
        janela.blit(self.image, self.rect.topleft)

if __name__ == '__main__':
    largura = 640
    altura = 480
    jogo = Jogo()
    jogo.executar()