from classe_jogo import *
from tela_inicio import *
from pause import *

if __name__ == "__main__":
    pygame.init()
    tela_inicio = Tela_inicio()
    tela_inicio.run()

    jogo = Jogo()
    # Agora passamos tanto a janela quanto o jogo para TelaPausa
    tela_pausa = TelaPausa(jogo.janela, jogo)

    while True:
        jogo.handle_events()
        jogo.update()
        jogo.render()
        jogo.render_timer()
        jogo.janela.blit(pygame.transform.scale(jogo.display, jogo.janela.get_size()), (0, 0))
        pygame.display.update()
        jogo.clock.tick(60)
        
