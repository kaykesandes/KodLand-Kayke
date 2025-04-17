import pgzrun
from random import randint, choice

# Configurações da janela
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 32

# Estado do jogo
game_state = "menu"
music_on = True

# Configurações do herói
hero = Actor("hero_idle", (WIDTH // 2, HEIGHT // 2))
hero.speed = 2
hero.direction = "down"
hero.animation_frame = 0
hero_animation_speed = 10
hero_animation_counter = 0

# Configurações dos inimigos
enemies = []
enemy_animation_speed = 15
enemy_animation_counters = []
enemy_speed_multiplier = 1

# Variáveis do sistema de pontos e tempo
score = 0
time_counter = 0

# Música
music.set_volume(0.5)
music.play("background_music")

# Variáveis do slider de volume
slider_x = WIDTH // 2  # Posição inicial do slider
slider_y = HEIGHT // 2 + 150  # Posição vertical do slider
slider_width = 200  # Largura do slider
slider_height = 10  # Altura do slider
slider_handle_x = slider_x  # Posição inicial do "handle" do slider
slider_handle_radius = 10  # Tamanho do "handle"
volume = 0.5  # Volume inicial

# Configuração do mapa
MAP_WIDTH = WIDTH // TILE_SIZE
MAP_HEIGHT = HEIGHT // TILE_SIZE
gamemap = [[1 if x == 0 or y == 0 or x == MAP_WIDTH - 1 or y == MAP_HEIGHT - 1 else choice([2, 3]) for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

# Funções auxiliares
def draw_map():
    """Desenha o mapa na tela."""
    for y, row in enumerate(gamemap):
        for x, tile in enumerate(row):
            if tile == 1:
                screen.blit("wall", (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == 2:
                screen.blit("floor1", (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == 3:
                screen.blit("floor2", (x * TILE_SIZE, y * TILE_SIZE))

def is_walkable(x, y):
    """Verifica se uma posição no mapa é caminhável."""
    return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and gamemap[y][x] != 1


def on_mouse_down(pos):
    """Detecta cliques no slider (apenas no menu)."""
    global slider_handle_x, volume
    if game_state != "menu":
        return  # Ignora cliques fora do menu
    if (slider_handle_x - slider_handle_radius <= pos[0] <= slider_handle_x + slider_handle_radius and
            slider_y <= pos[1] <= slider_y + slider_height):
        slider_handle_x = pos[0]
        update_volume()

def on_mouse_move(pos, buttons):
    """Permite arrastar o slider (apenas no menu)."""
    global slider_handle_x, volume
    if game_state != "menu":
        return  # Ignora movimentos fora do menu
    if 1 in buttons:  # Verifica se o botão esquerdo do mouse está pressionado
        if slider_x - slider_width // 2 <= pos[0] <= slider_x + slider_width // 2:
            slider_handle_x = pos[0]
            update_volume()

def update_volume():
    """Atualiza o volume com base na posição do slider."""
    global volume
    volume = (slider_handle_x - (slider_x - slider_width // 2)) / slider_width
    music.set_volume(volume)

def reset_game():
    """Reinicia o estado do jogo."""
    global hero, enemies, hero_animation_counter, enemy_animation_counters, score, time_counter, enemy_speed_multiplier

    # Reinicia o herói
    hero.pos = (WIDTH // 2, HEIGHT // 2)
    hero.direction = "down"
    hero.animation_frame = 0
    hero.image = "hero_idle"
    hero_animation_counter = 0

    # Reinicia os inimigos
    enemies.clear()
    for _ in range(3):
        enemy = Actor("enemy_idle", (randint(0, WIDTH), randint(0, HEIGHT)))
        enemy.speed = 1
        enemy.direction = "left"
        enemy.animation_frame = 0
        enemies.append(enemy)

    enemy_animation_counters[:] = [0] * len(enemies)

    # Reinicia o sistema de pontos, tempo e velocidade
    score = 0
    time_counter = 0
    enemy_speed_multiplier = 1

def calculate_enemy_direction(enemy):
    """Calcula a direção para o inimigo se aproximar do herói."""
    enemy_tile_x = int(enemy.x // TILE_SIZE)
    enemy_tile_y = int(enemy.y // TILE_SIZE)
    hero_tile_x = int(hero.x // TILE_SIZE)
    hero_tile_y = int(hero.y // TILE_SIZE)

    dx = dy = 0
    if hero_tile_x < enemy_tile_x and is_walkable(enemy_tile_x - 1, enemy_tile_y):
        dx = -1
    elif hero_tile_x > enemy_tile_x and is_walkable(enemy_tile_x + 1, enemy_tile_y):
        dx = 1
    elif hero_tile_y < enemy_tile_y and is_walkable(enemy_tile_x, enemy_tile_y - 1):
        dy = -1
    elif hero_tile_y > enemy_tile_y and is_walkable(enemy_tile_x, enemy_tile_y + 1):
        dy = 1

    return dx, dy

def update_animation(actor, moving, actor_type, index=None):
    """Atualiza a animação de um ator (herói ou inimigo)."""
    global enemy_animation_counters

    if moving:
        if actor_type == "hero":
            global hero_animation_counter
            hero_animation_counter += 1
            if hero_animation_counter >= hero_animation_speed:
                actor.animation_frame = (actor.animation_frame + 1) % 3
                actor.image = f"{actor_type}_{actor.direction}_{actor.animation_frame}"
                hero_animation_counter = 0
        elif actor_type == "enemy":
            enemy_animation_counters[index] += 1
            if enemy_animation_counters[index] >= enemy_animation_speed:
                actor.animation_frame = (actor.animation_frame + 1) % 3
                actor.image = f"{actor_type}_{actor.direction}_{actor.animation_frame}"
                enemy_animation_counters[index] = 0
    else:
        actor.image = f"{actor_type}_idle"

def update_hero():
    """Atualiza o movimento e animação do herói."""
    moving = False
    directions = {
        "up": (keyboard.up or keyboard.w, 0, -1),
        "down": (keyboard.down or keyboard.s, 0, 1),
        "left": (keyboard.left or keyboard.a, -1, 0),
        "right": (keyboard.right or keyboard.d, 1, 0),
    }

    for direction, (key_pressed, dx, dy) in directions.items():
        if key_pressed:
            hero_tile_x = int(hero.x // TILE_SIZE) + dx
            hero_tile_y = int(hero.y // TILE_SIZE) + dy
            if is_walkable(hero_tile_x, hero_tile_y):
                hero.x += hero.speed * dx
                hero.y += hero.speed * dy
                hero.direction = direction
                moving = True
                break

    update_animation(hero, moving, "hero")

def update_enemies():
    """Atualiza o movimento e animação dos inimigos."""
    global enemy_speed_multiplier

    for i, enemy in enumerate(enemies):
        dx, dy = calculate_enemy_direction(enemy)
        if dx or dy:
            enemy.x += enemy.speed * enemy_speed_multiplier * dx
            enemy.y += enemy.speed * enemy_speed_multiplier * dy
            enemy.direction = "left" if dx < 0 else "right" if dx > 0 else "up" if dy < 0 else "down"

        update_animation(enemy, True, "enemy", i)

    if time_counter % (30 * 60) == 0:  # A cada 30 segundos
        enemy_speed_multiplier += 0.1

def check_collision():
    """Verifica colisões entre o herói e os inimigos."""
    global game_state
    for enemy in enemies:
        if hero.colliderect(enemy):
            game_state = "game_over"

def draw_menu():
    """Desenha o menu principal."""
    screen.clear()
    screen.draw.text("JOGO KODLAND - Kayke Sandes", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=60, color="white")
    screen.draw.text("Press ENTER to Start", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text("Press ESC to Exit", center=(WIDTH // 2, HEIGHT // 2 + 200), fontsize=30, color="white")
    screen.draw.text("Meu primeiro projeto com pgzero, pygame. Peço que considere isso <3", center=(WIDTH // 2, HEIGHT // 2 + 250), fontsize=25, color="white")

    # Desenha o slider de volume
    screen.draw.filled_rect(Rect((slider_x - slider_width // 2, slider_y), (slider_width, slider_height)), "gray")
    screen.draw.filled_circle((slider_handle_x, slider_y + slider_height // 2), slider_handle_radius, "white")
    screen.draw.text(f"Volume: {int(volume * 100)}%", center=(WIDTH // 2, slider_y - 20), fontsize=30, color="white")

def draw_game():
    screen.clear()
    draw_map()  # Desenha o mapa
    hero.draw()
    for enemy in enemies:
        enemy.draw()
    screen.draw.text(f"Time: {time_counter // 60}s", (10, 10), fontsize=30, color="white")
    screen.draw.text(f"Score: {score}", (10, 40), fontsize=30, color="white")

def draw_game_over():
    screen.clear()
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=60, color="red")
    screen.draw.text(f"Final Score: {score}", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text("Press ENTER to Return to Menu", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="white")

def update_game():
    global time_counter, score, hero, enemy_speed_multiplier

    time_counter += 1

    # Incrementa o score a cada segundo
    if time_counter % 60 == 0:
        score += 1

    # Aumenta a velocidade a cada 20 segundos
    if time_counter % (20 * 60) == 0:  # 20 segundos (60 frames por segundo)
        enemy_speed_multiplier *= 2  # Dobra a velocidade dos inimigos
        hero.speed += hero.speed / 3  # Aumenta a velocidade do herói em 1/3

    update_hero()
    update_enemies()
    check_collision()

def on_key_down(key):
    global game_state, music_on
    if game_state == "menu":
        if key == keys.RETURN:
            game_state = "game"
            reset_game()
        elif key == keys.M:
            music_on = not music_on
            if music_on:
                music.play("background_music")
            else:
                music.stop()
        elif key == keys.ESCAPE:
            exit()
    elif game_state == "game":
        if key == keys.ESCAPE:
            game_state = "menu"
            reset_game()
    elif game_state == "game_over":
        if key == keys.RETURN:
            game_state = "menu"
            reset_game()

def draw():
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()
    elif game_state == "game_over":
        draw_game_over()

def update():
    if game_state == "game":
        update_game()

pgzrun.go()