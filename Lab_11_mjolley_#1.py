"""
Side Shooter Game
Michael Jolley
This is a simple side shooter game where a ship can move up, down, left, and right also can shoot projectiles.
"""

import pygame
import sys

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side Shooter")
clock = pygame.time.Clock()

# --- Constants ---
SHIP_WIDTH, SHIP_HEIGHT = 60, 40
PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 20, 8
SHIP_SPEED = 5
PROJECTILE_SPEED = 10

# --- Colors ---
BG_COLOR = (30, 30, 40)
LEFT_SHIP_COLOR = (0, 200, 255)
RIGHT_SHIP_COLOR = (255, 100, 0)
PROJECTILE_COLOR = (255, 255, 0)

# --- Game Variables ---
ship_side = "left"  # "left" or "right"
ship_y = HEIGHT // 2 - SHIP_HEIGHT // 2
projectiles = []

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
                projectiles.append([proj_x, proj_y, proj_vx])

            # Optional: toggle ship side with TAB
            if event.key == pygame.K_TAB:
                ship_side = "right" if ship_side == "left" else "left"

    # --- Move Ship ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and ship_y > 0:
        ship_y -= SHIP_SPEED
    if keys[pygame.K_DOWN] and ship_y < HEIGHT - SHIP_HEIGHT:
        ship_y += SHIP_SPEED

    # --- Update Projectiles ---
    for proj in projectiles:
        proj[0] += proj[2]
    # Remove off-screen projectiles
    projectiles = [p for p in projectiles if 0 <= p[0] <= WIDTH]

    # --- Drawing ---
    screen.fill(BG_COLOR)

    # Draw ship
    if ship_side == "left":
        ship_rect = pygame.Rect(0, ship_y, SHIP_WIDTH, SHIP_HEIGHT)
        pygame.draw.rect(screen, LEFT_SHIP_COLOR, ship_rect)
    else:
        ship_rect = pygame.Rect(WIDTH - SHIP_WIDTH, ship_y, SHIP_WIDTH, SHIP_HEIGHT)
        pygame.draw.rect(screen, RIGHT_SHIP_COLOR, ship_rect)

    # Draw projectiles
    for proj_x, proj_y, _ in projectiles:
        proj_rect = pygame.Rect(proj_x, proj_y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
        pygame.draw.rect(screen, PROJECTILE_COLOR, proj_rect)

    pygame.display.flip()
    clock.tick(60)

# --- Cleanup ---
pygame.quit()
sys.exit()
