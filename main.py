import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from sprites import load_sprite
from entities import Character
from battle import battle  # Importăm funcția battle
from start_screen import start_screen
from victory_screen import display_victory_screen
from selection_screen import selection_screen
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Orcs vs Soldiers")
clock = pygame.time.Clock()

# Load assets
background = pygame.image.load("assets/terrain.png").convert()
orc_walk_frames = load_sprite("assets/Orc-Walk.png", 100, 100)
orc_attack_frames = load_sprite("assets/Orc-Attack01.png", 100, 100)
orc_death_frames = load_sprite("assets/Orc-Death.png", 100, 100)
soldier_walk_frames = load_sprite("assets/Soldier-Walk.png", 100, 100)
soldier_attack_frames = load_sprite("assets/Soldier-Attack01.png", 100, 100)
soldier_death_frames = load_sprite("assets/Soldier-Death.png", 100, 100)
start_screen(screen)
# Create characters
orc_count, soldier_count = selection_screen(screen)

# Create characters
orcs = [
    Character(100, random.randint(50, SCREEN_HEIGHT - 150), 100, 25,
              orc_walk_frames, orc_attack_frames, orc_death_frames)
    for _ in range(orc_count)
]
soldiers = [
    Character(600, random.randint(50, SCREEN_HEIGHT - 150), 100, 25,
              soldier_walk_frames, soldier_attack_frames, soldier_death_frames)
    for _ in range(soldier_count)
]

# Game loop
running = True
winner = None
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if all(orc.is_dead for orc in orcs):
        display_victory_screen(screen, "Soldiers", SCREEN_WIDTH, SCREEN_HEIGHT)
        running = False
    elif all(soldier.is_dead for soldier in soldiers):
        display_victory_screen(screen, "Orcs", SCREEN_WIDTH, SCREEN_HEIGHT)
        running = False


    # Manage battle logic
    battle(orcs, soldiers, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Update characters
    for orc in orcs:
        orc.update()

    for soldier in soldiers:
        soldier.update()

    # Draw everything
    screen.blit(background, (0, 0))  # Draw the terrain as background
    for orc in orcs:
        orc.draw(screen)
    for soldier in soldiers:
        soldier.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Show winner screen

screen.fill((0, 0, 0))  # Black background
font = pygame.font.SysFont(None, 72)
text = font.render(winner, True, (255, 255, 255))
screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
pygame.display.flip()
# pygame.time.wait(3000)  # Wait for 3 seconds before quitting

pygame.quit()