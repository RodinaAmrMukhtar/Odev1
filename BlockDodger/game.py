import random
import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Dodger")

CLOCK = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
RED = (220, 70, 70)
BLUE = (70, 140, 255)
GREEN = (70, 200, 120)
GRAY = (180, 180, 180)

FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 64)

PLAYER_W, PLAYER_H = 70, 22
PLAYER_SPEED = 8

ENEMY_W, ENEMY_H = 50, 24
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 550)

def reset_game():
    player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 60, PLAYER_W, PLAYER_H)
    enemies = []
    score = 0
    game_over = False
    start_ticks = pygame.time.get_ticks()
    return player, enemies, score, game_over, start_ticks

def draw_text(text, font, color, x, y, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    SCREEN.blit(surf, rect)

player, enemies, score, game_over, start_ticks = reset_game()

running = True
while running:
    CLOCK.tick(60)

    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0
    enemy_speed = 4 + int(elapsed_seconds // 8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_EVENT and not game_over:
            x = random.randint(0, WIDTH - ENEMY_W)
            enemies.append(pygame.Rect(x, -ENEMY_H, ENEMY_W, ENEMY_H))

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                player, enemies, score, game_over, start_ticks = reset_game()
            elif event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += PLAYER_SPEED

        player.x = max(0, min(WIDTH - PLAYER_W, player.x))

        for enemy in enemies[:]:
            enemy.y += enemy_speed

            if enemy.colliderect(player):
                game_over = True

            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                score += 1

    SCREEN.fill(BLACK)

    pygame.draw.rect(SCREEN, BLUE, player, border_radius=6)

    for enemy in enemies:
        pygame.draw.rect(SCREEN, RED, enemy, border_radius=4)

    draw_text(f"Score: {score}", FONT, WHITE, 20, 20)
    draw_text("Move: Left/Right or A/D", FONT, GRAY, 20, 55)

    if not game_over:
        draw_text(f"Speed: {enemy_speed}", FONT, GREEN, 20, 90)
    else:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        SCREEN.blit(overlay, (0, 0))
        draw_text("GAME OVER", BIG_FONT, WHITE, WIDTH // 2, HEIGHT // 2 - 40, center=True)
        draw_text(f"Final Score: {score}", FONT, WHITE, WIDTH // 2, HEIGHT // 2 + 15, center=True)
        draw_text("Press R to restart or ESC to quit", FONT, GRAY, WIDTH // 2, HEIGHT // 2 + 55, center=True)

    pygame.display.flip()

pygame.quit()
sys.exit()