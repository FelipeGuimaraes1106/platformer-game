import pgzrun

# Configurações da tela
WIDTH = 800
HEIGHT = 600
# Título
TITLE = "Meu Jogo Platformer"

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Opções do Jogo
menu_on = True
music_on = False

# Função para desenhar o menu
def draw_menu():
    screen.fill(WHITE)  # Preenche a tela com a cor branca
    
    # Desenha o título do menu
    screen.draw.text("Menu Principal", center=(WIDTH/2, 100), fontsize=60, color=BLACK)
    
    # Desenha os botões
    btn_start = Rect((WIDTH/2 - 100, 200), (250, 50))  # Botão "Começar Jogo"
    btn_music = Rect((WIDTH/2 - 100, 300), (250, 50))   # Botão "Música"
    btn_exit = Rect((WIDTH/2 - 100, 400), (250, 50))     # Botão "Sair"
    
    screen.draw.filled_rect(btn_start, BLUE)  # Desenha o botão "Começar Jogo"
    screen.draw.filled_rect(btn_music, BLUE)   # Desenha o botão "Música"
    screen.draw.filled_rect(btn_exit, BLUE)     # Desenha o botão "Sair"
    
    # Adiciona texto dentro dos botões
    screen.draw.text("Começar Jogo", center=btn_start.center, fontsize=40, color=WHITE)

    screen.draw.text("Música:" + ("Ligada" if music_on else "Desligada"), 
    center=btn_music.center, fontsize=40, color=WHITE)

    screen.draw.text("Sair", center=btn_exit.center, fontsize=40, color=WHITE)

    return btn_start, btn_music, btn_exit 
"""" Função principal de desenho. """
def draw():
    if menu_on: 
        draw_menu()  # Desenha o menu
    else:
        # Aqui você pode desenhar o jogo principal
        screen.fill(BLACK)
        screen.draw.text("Jogo em andamento...", center=(WIDTH/2, HEIGHT/2),
        fontsize=60, color=WHITE)

"""lida com cliques do mouse. """    
def on_mouse_down(pos):
    global menu_on, music_on

    if menu_on:  # Se o menu estiver ativo
        btn_comecar, btn_musica, btn_sair = draw_menu()  # Obtém os retângulos dos botões

        if btn_comecar.collidepoint(pos):  # Verifica se clicou no botão "Começar Jogo"
            menu_on = False  # Fecha o menu e inicia o jogo
        elif btn_musica.collidepoint(pos):  # Verifica se clicou no botão "Música"
            music_on = not music_on  # Alterna o estado da música
        elif btn_sair.collidepoint(pos):  # Verifica se clicou no botão "Sair"
            exit()  # Fecha o jogo

# Inicia o jogo
pgzrun.go()
