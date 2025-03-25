import pgzrun
from pygame import Rect


# Configurações principais
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer Game"
GROUND_Y = HEIGHT - 50  # Posição Y do chão

# Cores e UI
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
HEART_IMAGE = "heart"  # Imagem do coração para vidas
HEART_SPACING = 40     # Espaçamento entre corações

# Configurações de jogo
PLATFORM_WIDTH = 200    # Largura das plataformas
PLATFORM_HEIGHT = 20    # Altura das plataformas

# Estados do jogo
menu_active = True
music_on = True
game_over = False


class Player(Actor):
    """Classe do jogador principal."""
    
    def __init__(self):
        super().__init__("idle", (100, GROUND_Y))  # Sprite inicial
        self.speed = 5      # Velocidade horizontal
        self.vy = 0         # Velocidade vertical
        self.on_ground = True  # Controle de chão
        self.direction = "right"  # Direção inicial
        self.is_jumping = False   # Estado do pulo
        self.lives = 3       # Quantidade de vidas
        
        # Dicionário de sprites para animações
        self.sprites = {
            "idle": "idle",
            "walk_right": ["walk_right_1", "walk_right_2"],
            "walk_left": ["walk_left_1", "walk_left_2"],
            "jump_right": "jump_right",
            "jump_left": "jump_left"
        }
        
        self.current_sprite = 0      # Frame atual da animação
        self.animation_speed = 10    # Velocidade da animação
        self.animation_counter = 0   # Contador de frames

    def animate(self, state):
        """Controla as animações do jogador."""
        if state == "idle":
            self.image = self.sprites["idle"]
        elif state in ["jump_right", "jump_left"]:
            self.image = self.sprites[state]
        else:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.current_sprite = (self.current_sprite + 1) % len(
                    self.sprites[state]
                )
                self.image = self.sprites[state][self.current_sprite]


class Enemy(Actor):
    """Classe dos inimigos."""
    
    def __init__(self):
        super().__init__("enemy_idle", (600, GROUND_Y))
        self.speed = 2
        self.direction = "left"
        self.vy = 0
        self.on_ground = True
        self.alive = True
        
        self.sprites = {
            "idle": "enemy_idle",
            "right": "enemy_right",
            "left": "enemy_left",
            "dead": "enemy_dead"
        }

    def move(self):
        """Controla o movimento automático do inimigo."""
        if self.alive:
            if self.direction == "left":
                self.x -= self.speed
                self.image = self.sprites["left"]
            else:
                self.x += self.speed
                self.image = self.sprites["right"]

            self._check_bounds()

    def _check_bounds(self):
        """Mantém o inimigo dentro dos limites da tela."""
        if self.x < 100:
            self.direction = "right"
        elif self.x > WIDTH - 100:
            self.direction = "left"

    def apply_gravity(self, platforms):
        """Aplica gravidade ao inimigo."""
        if self.alive:
            self.vy += 1
            self.y += self.vy
            check_collision(self, platforms)


def setup_platforms():
    """Configura as plataformas do jogo."""
    platform_positions = [
        (400, 550),
        (200, 400),
        (550, 350)
    ]
    
    platforms = []
    for x, y in platform_positions:
        platforms.append({
            "image": Actor("platform", (x, y)),
            "rect": Rect(
                x - PLATFORM_WIDTH / 2,
                y - PLATFORM_HEIGHT / 2,
                PLATFORM_WIDTH,
                PLATFORM_HEIGHT
            )
        })
    
    platforms.append({
        "image": Actor("ground", (WIDTH // 2, GROUND_Y)),
        "rect": Rect(0, GROUND_Y - 10, WIDTH, 20)
    })
    
    return platforms


def setup_enemies():
    """Cria múltiplos inimigos."""
    enemies = []
    start_positions = [
        (600, GROUND_Y),
        (300, 400),
        (500, 250)
    ]
    for pos in start_positions:
        enemy = Enemy()
        enemy.x, enemy.y = pos
        enemies.append(enemy)
    return enemies


def check_collision(actor, platforms):
    """Verifica colisões entre atores e plataformas."""
    actor.on_ground = False
    actor_rect = Rect(
        actor.x - actor.width / 2,
        actor.y - actor.height / 2,
        actor.width,
        actor.height
    )

    for platform in platforms:
        if actor_rect.colliderect(platform["rect"]):
            _handle_collision(actor, platform)


def _handle_collision(actor, platform):
    """Processa os efeitos da colisão."""
    actor_rect = Rect(
        actor.x - actor.width / 2,
        actor.y - actor.height / 2,
        actor.width,
        actor.height
    )
    
    if actor_rect.bottom >= platform["rect"].top and actor.vy > 0:
        actor.y = platform["rect"].top - actor.height / 2
        actor.vy = 0
        actor.on_ground = True
        if isinstance(actor, Player):
            actor.is_jumping = False
    elif actor_rect.top <= platform["rect"].bottom and actor.vy < 0:
        actor.y = platform["rect"].bottom + actor.height / 2
        actor.vy = 0


def check_enemy_collisions():
    """Verifica colisões entre jogador e todos os inimigos."""
    for enemy in enemies:
        if not enemy.alive:
            continue
        
        player_rect = Rect(
            player.x - player.width / 2,
            player.y - player.height / 2,
            player.width,
            player.height
        )
        
        enemy_rect = Rect(
            enemy.x - enemy.width / 2,
            enemy.y - enemy.height / 2,
            enemy.width,
            enemy.height
        )

        if player_rect.colliderect(enemy_rect):
            _handle_enemy_collision(player_rect, enemy_rect, enemy)


def _handle_enemy_collision(player_rect, enemy_rect, enemy):
    """Processa colisão com um inimigo específico."""
    if player_rect.bottom >= enemy_rect.top + 10 and player.vy > 0:
        enemy.alive = False
        enemy.image = enemy.sprites["dead"]
        player.vy = -10
    else:
        player.lives -= 1
        _reset_player_position()
        if player.lives <= 0:
            global game_over
            game_over = True


def _reset_player_position():
    """Reinicia a posição do jogador após dano."""
    player.x = 100
    player.y = GROUND_Y - player.height / 2
    player.vy = 0
    player.on_ground = True


def update_game():
    """Atualiza a lógica do jogo a cada frame."""
    global game_over
    
    if player.lives <= 0:
        game_over = True
        return

    if player.on_ground and keyboard.space:
        player.vy = -15
        player.is_jumping = True
        if player.direction == "right":
            player.animate("jump_right")
        else:
            player.animate("jump_left")

    elif keyboard.left:
        player.x -= player.speed
        player.direction = "left"
        if not player.is_jumping:
            player.animate("walk_left")
        
    elif keyboard.right:
        player.x += player.speed
        player.direction = "right"
        if not player.is_jumping:
            player.animate("walk_right")
        
    else:
        if not player.is_jumping:
            player.animate("idle")

    player.vy += 1
    player.y += player.vy
    check_collision(player, platforms)

    for enemy in enemies:
        enemy.move()
        enemy.apply_gravity(platforms)
    
    check_enemy_collisions()

    if player.y >= GROUND_Y - player.height / 2:
        player.y = GROUND_Y - player.height / 2
        player.vy = 0
        player.on_ground = True


def draw_game():
    """Renderiza os elementos do jogo."""
    screen.fill(BLUE)
    
    for platform in platforms:
        platform["image"].draw()
    
    player.draw()
    
    for enemy in enemies:
        if enemy.alive:
            enemy.draw()
        else:
            screen.blit(
                "enemy_dead",
                (enemy.x - enemy.width / 2, enemy.y - enemy.height / 2)
            )
    
    for i in range(player.lives):
        screen.blit(HEART_IMAGE, (10 + i * HEART_SPACING, 10))


def draw_menu():
    """Renderiza o menu principal."""
    screen.fill(WHITE)
    screen.draw.text(
        "Menu Principal",
        center=(WIDTH/2, 100),
        fontsize=60,
        color=BLACK
    )

    buttons = {
        "start": Rect((WIDTH/2 - 100, 200), (200, 50)),
        "music": Rect((WIDTH/2 - 100, 300), (200, 50)),
        "exit": Rect((WIDTH/2 - 100, 400), (200, 50))
    }
    
    for btn in buttons.values():
        screen.draw.filled_rect(btn, BLUE)
    
    screen.draw.text(
        "Iniciar Jogo",
        center=buttons["start"].center,
        fontsize=40,
        color=WHITE
    )
    
    screen.draw.text(
        f"Música: {'ON' if music_on else 'OFF'}",
        center=buttons["music"].center,
        fontsize=40,
        color=WHITE
    )
    
    screen.draw.text(
        "Sair",
        center=buttons["exit"].center,
        fontsize=40,
        color=WHITE
    )
    
    return buttons


def draw_game_over():
    """Renderiza a tela de game over."""
    screen.fill(WHITE)
    screen.draw.text(
        "Game Over!",
        center=(WIDTH/2, 100),
        fontsize=60,
        color=BLACK
    )
    
    buttons = {
        "restart": Rect((WIDTH/2-100, 200), (200, 50)),
        "exit": Rect((WIDTH/2-100, 300), (200, 50))
    }
    
    for btn in buttons.values():
        screen.draw.filled_rect(btn, BLUE)
    
    screen.draw.text(
        "Reiniciar",
        center=buttons["restart"].center,
        fontsize=40,
        color=WHITE
    )
    
    screen.draw.text(
        "Sair",
        center=buttons["exit"].center,
        fontsize=40,
        color=WHITE
    )
    
    return buttons


def reset_game():
    """Reinicia o jogo com valores iniciais."""
    global player, enemies, game_over
    player = Player()
    enemies = setup_enemies()
    game_over = False


def update():
    """Função principal de atualização do pgzero."""
    global menu_active
     
    if music_on and not music.is_playing("background_music"):
        music.play("background_music")
    elif not music_on and music.is_playing("background_music"):
        music.pause()
    if game_over or menu_active:
        return
    
    update_game()


def on_mouse_down(pos):
    """Lida com cliques do mouse."""
    global menu_active, music_on, game_over
    
    if game_over:
        buttons = draw_game_over()
        if buttons["restart"].collidepoint(pos):
            reset_game()
        elif buttons["exit"].collidepoint(pos):
            exit()
    elif menu_active:
        buttons = draw_menu()
        if buttons["start"].collidepoint(pos):
            menu_active = False
        elif buttons["music"].collidepoint(pos):
            music_on = not music_on
        elif buttons["exit"].collidepoint(pos):
            exit()


def draw():
    """Função principal de renderização do pgzero."""
    if game_over:
        draw_game_over()
    elif menu_active:
        draw_menu()
    else:
        draw_game()


# Inicialização do jogo
platforms = setup_platforms()
enemies = setup_enemies()
player = Player()

pgzrun.go()
