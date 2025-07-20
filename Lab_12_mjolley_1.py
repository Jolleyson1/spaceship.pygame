"""
Side Shooter Game
Michael Jolley
This is a simple side shooter game where a ship can move up, down, left, and right also can shoot projectiles.
"""

import pygame
import sys
import random

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side Shooter")
clock = pygame.time.Clock()

# --- Constants ---
SHIP_WIDTH, SHIP_HEIGHT = 60, 40
PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 20, 8
ALIEN_WIDTH, ALIEN_HEIGHT = 40, 30
SHIP_SPEED = 5
PROJECTILE_SPEED = 10
ALIEN_SPEED = 2

# --- Colors ---
BG_COLOR = (30, 30, 40)
LEFT_SHIP_COLOR = (0, 200, 255)
RIGHT_SHIP_COLOR = (255, 100, 0)
PROJECTILE_COLOR = (255, 255, 0)
ALIEN_COLOR = (0, 255, 0)

# --- Game Variables ---
def reset_game():
    global ship_y, projectiles, aliens
    ship_y = HEIGHT // 2 - SHIP_HEIGHT // 2
    projectiles = []
    aliens = []

    # Create horizontal alien fleet
    spacing = 80
    y_pos = 100
    for i in range(6):  # number of aliens
        x = WIDTH - (i * spacing + ALIEN_WIDTH)
        y = y_pos
        aliens.append(pygame.Rect(x, y, ALIEN_WIDTH, ALIEN_HEIGHT))

ship_side = "left"
reset_game()

# --- Main Loop ---
running = True
while running:
    # --- Handle Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Fire projectile
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if ship_side == "left":
                    proj_x = SHIP_WIDTH
                    proj_vx = PROJECTILE_SPEED
                else:
                    proj_x = WIDTH - SHIP_WIDTH - PROJECTILE_WIDTH
                    proj_vx = -PROJECTILE_SPEED

                proj_y = ship_y + SHIP_HEIGHT // 2 - PROJECTILE_HEIGHT // 2
                projectiles.append(pygame.Rect(proj_x, proj_y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT))

            # Switch ship sides
            if event.key == pygame.K_TAB:
                ship_side = "right" if ship_side == "left" else "left"

    # --- Move Ship ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and ship_y > 0:
        ship_y -= SHIP_SPEED
    if keys[pygame.K_DOWN] and ship_y < HEIGHT - SHIP_HEIGHT:
        ship_y += SHIP_SPEED

    # --- Move Projectiles ---
    for proj in projectiles:
        proj.x += PROJECTILE_SPEED if ship_side == "left" else -PROJECTILE_SPEED
    projectiles = [p for p in projectiles if 0 <= p.x <= WIDTH]

    # --- Move Aliens ---
    for alien in aliens:
        alien.x -= ALIEN_SPEED

    # --- Collision Detection ---
    for proj in projectiles[:]:
        for alien in aliens[:]:
            if proj.colliderect(alien):
                projectiles.remove(proj)
                aliens.remove(alien)
                break

    # --- Alien Hits Ship or Passes Edge ---
    for alien in aliens:
        if ship_side == "left":
            ship_rect = pygame.Rect(0, ship_y, SHIP_WIDTH, SHIP_HEIGHT)
            if alien.colliderect(ship_rect) or alien.x <= 0:
                reset_game()
        else:
            ship_rect = pygame.Rect(WIDTH - SHIP_WIDTH, ship_y, SHIP_WIDTH, SHIP_HEIGHT)
            if alien.colliderect(ship_rect) or alien.x + ALIEN_WIDTH >= WIDTH:
                reset_game()

    # --- Drawing ---
    screen.fill(BG_COLOR)

    # Draw ship
    pygame.draw.rect(screen, LEFT_SHIP_COLOR if ship_side == "left" else RIGHT_SHIP_COLOR, ship_rect)

    # Draw projectiles
    for proj in projectiles:
        pygame.draw.rect(screen, PROJECTILE_COLOR, proj)

    # Draw aliens
    for alien in aliens:
        pygame.draw.rect(screen, ALIEN_COLOR, alien)

    pygame.display.flip()
    clock.tick(60)

# --- Cleanup ---
pygame.quit()
sys.exit()
