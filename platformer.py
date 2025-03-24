import pgzrun
from pygame import Rect

# Configurações da tela
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer Game"

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)

# Estado do jogo
menu_active = True
music_on = True

# Posição fixa do chão
GROUND_Y = HEIGHT - 50  # Define a posição Y do chão

# Personagem principal
player = Actor("actor_stop", (100, GROUND_Y))  # Inicia o personagem no chão
player.speed = 5  # Velocidade de movimento
player.vy = 0  # Velocidade vertical (para gravidade)
player.on_ground = True  # Começa no chão
player.direction = "right"  # Direção inicial do personagem
player.is_jumping = False  # Estado de pulo

# Sprites para animação
player_sprites = {
    "parado": "actor_stop",  # Personagem parado
    "andando_direita": ["actor_right1", "actor_right2"],  # Animação andando para a direita
    "andando_esquerda": ["actor_left1", "actor_left2"],  # Animação andando para a esquerda
    "pulando_direita": "actor_jump_right",  # Personagem pulando para a direita
    "pulando_esquerda": "actor_jump_left",  # Personagem pulando para a esquerda
}
player.current_sprite = 0  # Índice do sprite atual
player.animation_speed = 10  # Velocidade da animação
player.animation_counter = 0  # Contador para controlar a animação

# Fator de escala para as plataformas
PLATFORM_SCALE = 2  # Aumenta o tamanho da plataforma em 2x

# Plataformas
platforms = [
    {"image": Actor("platform", (400, 550)), "rect": Rect(400 - 100 * PLATFORM_SCALE, 550 - 10, 200 * PLATFORM_SCALE, 20)},  # Plataforma 1
    {"image": Actor("platform", (200, 400)), "rect": Rect(200 - 100 * PLATFORM_SCALE, 400 - 10, 200 * PLATFORM_SCALE, 20)},  # Plataforma 2
    {"image": Actor("platform", (600, 300)), "rect": Rect(600 - 100 * PLATFORM_SCALE, 300 - 10, 200 * PLATFORM_SCALE, 20)},  # Plataforma 3
]

# Aplica o fator de escala às plataformas
for platform in platforms:
    platform["image"].scale = PLATFORM_SCALE

# Chão
ground = {"image": Actor("ground", (WIDTH // 2, GROUND_Y)), "rect": Rect(0, GROUND_Y - 10, WIDTH, 20)}
platforms.append(ground)

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
            platform["image"].draw()
        player.draw()

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
                music.unpause()
            else:
                music.pause()
        elif btn_exit.collidepoint(pos):
            exit()

# Função para verificar colisão com as plataformas
def check_collision():
    global player

    player.on_ground = False
    player_rect = Rect(player.x - player.width / 2, player.y - player.height / 2, player.width, player.height)

    for platform in platforms:
        if player_rect.colliderect(platform["rect"]):
            if player.vy > 0 and player_rect.bottom >= platform["rect"].top:
                player.y = platform["rect"].top - player.height / 2
                player.vy = 0
                player.on_ground = True
                player.is_jumping = False  # Personagem tocou o chão, não está mais pulando
            elif player.vy < 0 and player_rect.top <= platform["rect"].bottom:
                player.y = platform["rect"].bottom + player.height / 2
                player.vy = 0

# Função para atualizar o estado do jogo
def update():
    global menu_active, music_on

    if menu_active:
        if music_on:
            if not music.is_playing("background_music"):
                music.play("background_music")
        else:
            if music.is_playing("background_music"):
                music.pause()
    else:
        # Verifica se o personagem está no chão e a tecla de pulo foi pressionada
        if player.on_ground and keyboard.space:
            player.vy = -15
            player.is_jumping = True  # Personagem está pulando
            if player.direction == "right":
                animate_player("pulando_direita")
            else:
                animate_player("pulando_esquerda")
        
        # Movimento para a esquerda
        elif keyboard.left:
            player.x -= player.speed
            player.direction = "left"
            if not player.is_jumping:  # Só anima andar se não estiver pulando
                animate_player("andando_esquerda")
        
        # Movimento para a direita
        elif keyboard.right:
            player.x += player.speed
            player.direction = "right"
            if not player.is_jumping:  # Só anima andar se não estiver pulando
                animate_player("andando_direita")
        
        # Personagem parado (nenhuma tecla pressionada)
        else:
            if not player.is_jumping:  # Só anima parado se não estiver pulando
                animate_player("parado")

        # Aplica gravidade
        player.vy += 1
        player.y += player.vy

        # Verifica colisão com as plataformas
        check_collision()

        # Fixa o personagem no chão
        if player.y >= GROUND_Y - player.height / 2:
            player.y = GROUND_Y - player.height / 2
            player.vy = 0
            player.on_ground = True
            player.is_jumping = False  # Personagem tocou o chão, não está mais pulando

# Função para animar o personagem
def animate_player(state):
    global player

    if state == "parado":
        player.image = player_sprites["parado"]
    elif state == "pulando_direita":
        player.image = player_sprites["pulando_direita"]
    elif state == "pulando_esquerda":
        player.image = player_sprites["pulando_esquerda"]
    else:
        player.animation_counter += 1
        if player.animation_counter >= player.animation_speed:
            player.animation_counter = 0
            player.current_sprite = (player.current_sprite + 1) % len(player_sprites[state])
            player.image = player_sprites[state][player.current_sprite]

# Inicializa a música
music.play("background_music")

# Inicia o jogo
pgzrun.go()
