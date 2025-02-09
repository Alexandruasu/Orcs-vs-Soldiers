import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from sprites import load_sprite
from entities import Character, Wizard  # Import Wizard here
from battle import battle
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
wizard_idle_frames = load_sprite("assets/Wizard-Idle.png", 100, 100)
wizard_walk_frames = load_sprite("assets/Wizard-Walk.png", 100, 100)
wizard_attack_frames = load_sprite("assets/Wizard-Attack01.png", 100, 100)
wizard_effect_frames = load_sprite("assets/Wizard-Attack01_Effect.png", 100, 100)

# Start screen
start_screen(screen)

# Selection screen
orc_count, soldier_count, wizard_count = selection_screen(screen)

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
wizards = [
    Wizard(700, random.randint(50, SCREEN_HEIGHT - 150), 100, 30,
           wizard_walk_frames, wizard_attack_frames, wizard_effect_frames, wizard_idle_frames)
    for _ in range(wizard_count)
]

# Game loop
running = True
winner = None
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check victory conditions
    if all(orc.is_dead for orc in orcs):
        display_victory_screen(screen, "Soldiers", SCREEN_WIDTH, SCREEN_HEIGHT)
        running = False
    elif all(soldier.is_dead for soldier in soldiers) and all(wizard.is_dead for wizard in wizards):
        display_victory_screen(screen, "Orcs", SCREEN_WIDTH, SCREEN_HEIGHT)
        running = False

    # Manage battle logic
    battle(orcs, soldiers, wizards, screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Update characters
    for orc in orcs:
        orc.update()
    for soldier in soldiers:
        soldier.update()
    for wizard in wizards:
        wizard.update()

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw the wizard projectiles
    for wizard in wizards:
        wizard.update_projectiles(screen)

    # Draw the characters
    for orc in orcs:
        orc.draw(screen)
    for soldier in soldiers:
        soldier.draw(screen)
    for wizard in wizards:
        wizard.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()