import pgzrun
from pygame import Rect
import os

# Configurações da tela
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer Game"

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
GREEN = (100, 255, 100)

# Estado do jogo
menu_active = True
music_on = True

# Personagem principal
player = Actor("actor_stop", (100, 500))  # Carrega a imagem "actor_stop.png" da pasta "images"
player.speed = 5  # Velocidade de movimento
player.vy = 0  # Velocidade vertical (para gravidade)
player.on_ground = False  # Verifica se o jogador está no chão
player.direction = "right"  # Direção inicial do personagem

# Sprites para animação
player_sprites = {
    "parado": "actor_stop2",
    "andando_direita": ["actor_right2"],  # Lista de sprites para andar para a direita
    "andando_esquerda": ["actor_left2"],  # Lista de sprites para andar para a esquerda
}
player.current_sprite = 0  # Índice do sprite atual
player.animation_speed = 10  # Velocidade da animação
player.animation_counter = 0  # Contador para controlar a animação

# Plataformas
platforms = [
    Rect((0, 550), (800, 50)),  # Chão
    Rect((200, 400), (200, 20)),  # Plataforma 1
    Rect((500, 300), (200, 20)),  # Plataforma 2
]

# Função para desenhar o menu
def draw_menu():
    screen.fill(WHITE)
    screen.draw.text("Main Menu", center=(WIDTH/2, 100), fontsize=60, color=BLACK)

    btn_start = Rect((WIDTH/2 - 100, 200), (200, 50))
    btn_music = Rect((WIDTH/2 - 100, 300), (200, 50))
    btn_exit = Rect((WIDTH/2 - 100, 400), (200, 50))

    screen.draw.filled_rect(btn_start, BLUE)
    screen.draw.filled_rect(btn_music, BLUE)
    screen.draw.filled_rect(btn_exit, BLUE)

    screen.draw.text("Start Game", center=btn_start.center, fontsize=40, color=WHITE)
    screen.draw.text("Music: " + ("On" if music_on else "Off"), center=btn_music.center, fontsize=40, color=WHITE)
    screen.draw.text("Exit", center=btn_exit.center, fontsize=40, color=WHITE)

    return btn_start, btn_music, btn_exit

# Função principal de desenho
def draw():
    if menu_active:
        draw_menu()
    else:
        screen.fill(BLUE)
        for platform in platforms:
            screen.draw.filled_rect(platform, GREEN)
        player.draw()  # Desenha o personagem

# Função para lidar com cliques do mouse
def on_mouse_down(pos):
    global menu_active, music_on

    if menu_active:
        btn_start, btn_music, btn_exit = draw_menu()

        if btn_start.collidepoint(pos):
            menu_active = False
        elif btn_music.collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.unpause()  # Retoma a música
            else:
                music.pause()  # Pausa a música
        elif btn_exit.collidepoint(pos):
            exit()

# Função para atualizar o estado do jogo
def update():
    global menu_active, music_on

    if menu_active:
        if music_on:
            if not music.is_playing("background_music"):  # Verifica se a música não está tocando
                music.play("background_music")  # Toca a música (sem a extensão .mp3)
        else:
            if music.is_playing("background_music"):  # Verifica se a música está tocando
                music.pause()  # Pausa a música
    else:
        # Movimento do personagem
        if keyboard.left:
            player.x -= player.speed
            player.direction = "left"
            animate_player("andando_esquerda")
        elif keyboard.right:
            player.x += player.speed
            player.direction = "right"
            animate_player("andando_direita")
        else:
            animate_player("parado")  # Personagem parado

        # Gravidade
        player.vy += 1  # Aumenta a velocidade vertical (simula gravidade)
        player.y += player.vy  # Aplica a velocidade vertical

        # Verifica colisão com as plataformas
        player.on_ground = False
        for platform in platforms:
            # Verifica se o personagem está caindo e se a parte inferior do personagem está prestes a ultrapassar o topo da plataforma
            if player.vy > 0 and player.colliderect(platform) and player.bottom >= platform.top:
                player.y = platform.top - player.height  # Ajusta a posição do personagem para ficar em cima da plataforma
                player.vy = 0  # Zera a velocidade vertical
                player.on_ground = True

        # Pulo
        if player.on_ground and keyboard.space:
            player.vy = -15  # Velocidade do pulo

# Função para animar o personagem
def animate_player(state):
    global player

    if state == "parado":
        player.image = player_sprites["parado"]
    else:
        player.animation_counter += 1
        if player.animation_counter >= player.animation_speed:
            player.animation_counter = 0
            player.current_sprite = (player.current_sprite + 1) % len(player_sprites[state])
            player.image = player_sprites[state][player.current_sprite]

# Inicializa a música
music.play("background_music")  # Toca a música (sem a extensão .mp3)

# Inicia o jogo
pgzrun.go()
