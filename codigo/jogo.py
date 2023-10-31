from classe_jogo import *
from tela_inicio import *

if __name__ == "__main__":
    tela_inicio = Tela_inicio()
    tela_inicio.run()

    # if not tela_inicio.menu():
    jogo = Jogo()
    while True:
        jogo.handle_events()
        jogo.update()
        jogo.render()

        jogo.janela.blit(pygame.transform.scale(jogo.display, jogo.janela.get_size()), (0, 0))
        pygame.display.update()
        jogo.clock.tick(60)

        



    
