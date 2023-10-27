# Classe que representa uma partícula no jogo
class Particle:
    def __init__(self, jogo, p_type, pos, velocity=[0, 0], frame=0):
        self.jogo = jogo
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        
        # Obtém a animação associada à partícula
        self.animation = self.jogo.assets['particle/' + p_type].copy()
        self.animation.frame = frame

    def update(self):
        # Atualiza a posição da partícula
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        # Atualiza a animação da partícula
        self.animation.update()
        
        # Remove a partícula se a animação estiver concluída
        return self.animation.done

    def render(self, surf, offset=(0, 0)):
        img = self.animation.img()
        # Renderiza a imagem no centro da posição
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))
