import pgzrun
from random import randint, choice, choices

# Configurações da janela
WIDTH = 800
HEIGHT = 600

# Estado do jogo
game_state = "menu"
music_on = True

# Configurações do herói e inimigos
TILE_SIZE = 32
hero = Actor("hero_idle", (WIDTH // 2, HEIGHT // 2))
hero.speed = 2
hero.direction = "down"
hero.animation_frame = 0
hero_animation_speed = 10
hero_animation_counter = 0

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

MAP_WIDTH = WIDTH // TILE_SIZE
MAP_HEIGHT = HEIGHT // TILE_SIZE

gamemap = []
for y in range(MAP_HEIGHT):
    row = []
    for x in range(MAP_WIDTH):
        if x == 0 or y == 0 or x == MAP_WIDTH - 1 or y == MAP_HEIGHT - 1:
            row.append(1)  # Barreiras nas bordas
        else:
            row.append(choice([2, 3, 1 if randint(0, 10) < 2 else 2]))  # Chão e paredes aleatórias
    gamemap.append(row)

def draw_map():
    """Desenha o mapa na tela."""
    for y, row in enumerate(gamemap):
        for x, tile in enumerate(row):
            if tile == 1:
                screen.blit("wall", (x * TILE_SIZE, y * TILE_SIZE))  # Tile de barreira
            elif tile == 2:
                screen.blit("floor1", (x * TILE_SIZE, y * TILE_SIZE))  # Primeiro tipo de chão
            elif tile == 3:
                screen.blit("floor2", (x * TILE_SIZE, y * TILE_SIZE))  # Segundo tipo de chão
                
def is_walkable(x, y):
    """Verifica se uma posição no mapa é caminhável."""
    if x < 0 or y < 0 or x >= MAP_WIDTH or y >= MAP_HEIGHT:
        return False
    return gamemap[y][x] != 1  # Não é caminhável se for uma barreira

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
    enemy_speed_multiplier = 1  # Reinicia o multiplicador de velocidade

def draw_menu():
    screen.clear()
    screen.draw.text("JOGO KODLAND - Kayke Sandes", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=60, color="white")
    screen.draw.text("Press ENTER to Start", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text(f"Music(M): {'On' if music_on else 'Off'}", center=(WIDTH // 2, HEIGHT // 2 + 100), fontsize=40, color="white")
    screen.draw.text("Press ESC to Exit", center=(WIDTH // 2, HEIGHT // 2 + 200), fontsize=30, color="white")
    screen.draw.text("Meu primeiro projeto com pgzero, pygame. Peço que considere isso <3", center=(WIDTH // 2, HEIGHT // 2 +250), fontsize=25, color="white")

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

def update_hero():
    global hero_animation_counter
    moving = False

    # Coordenadas do herói no mapa
    hero_tile_x = int(hero.x // TILE_SIZE)
    hero_tile_y = int(hero.y // TILE_SIZE)

    # Verifica se o herói está nas bordas da tela
    if keyboard.up and is_walkable(hero_tile_x, hero_tile_y - 1):
        hero.y -= hero.speed
        hero.direction = "up"
        moving = True
    elif keyboard.down and is_walkable(hero_tile_x, hero_tile_y + 1):
        hero.y += hero.speed
        hero.direction = "down"
        moving = True
    elif keyboard.left and is_walkable(hero_tile_x - 1, hero_tile_y):
        hero.x -= hero.speed
        hero.direction = "left"
        moving = True
    elif keyboard.right and is_walkable(hero_tile_x + 1, hero_tile_y):
        hero.x += hero.speed
        hero.direction = "right"
        moving = True

    # Atualiza a animação do herói
    if moving:
        hero_animation_counter += 1
        if hero_animation_counter >= hero_animation_speed:
            hero.animation_frame = (hero.animation_frame + 1) % 3
            hero.image = f"hero_{hero.direction}_{hero.animation_frame}"
            hero_animation_counter = 0
    else:
        hero.image = "hero_idle"

def update_enemies():
    global enemy_animation_counters, enemy_speed_multiplier, time_counter

    # Aumenta a velocidade dos inimigos a cada 20 segundos
    if time_counter % (20 * 60) == 0:  # 20 segundos (60 frames por segundo)
        enemy_speed_multiplier *= 2  # Dobra a velocidade

    for i, enemy in enumerate(enemies):
        # Movimenta o inimigo na direção atual com o multiplicador de velocidade
        if enemy.direction == "left":
            enemy.x -= enemy.speed * enemy_speed_multiplier
            if enemy.x < 0:
                enemy.direction = "right"
        elif enemy.direction == "right":
            enemy.x += enemy.speed * enemy_speed_multiplier
            if enemy.x > WIDTH:
                enemy.direction = "left"
        elif enemy.direction == "up":
            enemy.y -= enemy.speed * enemy_speed_multiplier
            if enemy.y < 0:
                enemy.direction = "down"
        elif enemy.direction == "down":
            enemy.y += enemy.speed * enemy_speed_multiplier
            if enemy.y > HEIGHT:
                enemy.direction = "up"

        # Atualiza a animação do inimigo
        enemy_animation_counters[i] += 1
        if enemy_animation_counters[i] >= enemy_animation_speed:
            enemy.animation_frame = (enemy.animation_frame + 1) % 3
            enemy.image = f"enemy_{enemy.direction}_{enemy.animation_frame}"
            enemy_animation_counters[i] = 0

        # Altera a direção aleatoriamente em intervalos regulares
        if randint(0, 100) < 2:  # 2% de chance de mudar de direção
            enemy.direction = randint(0, 3)
            if enemy.direction == 0:
                enemy.direction = "left"
            elif enemy.direction == 1:
                enemy.direction = "right"
            elif enemy.direction == 2:
                enemy.direction = "up"
            elif enemy.direction == 3:
                enemy.direction = "down"

def check_collision():
    global game_state
    for enemy in enemies:
        if hero.colliderect(enemy):
            game_state = "game_over"

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